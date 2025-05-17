import os
import re
import time
import requests
import pprint
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from map.models import Lecturer, CustomUser
from django.db import connection

BASE_URL = "https://mmuexpert.mmu.edu.my/FCI"
HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}
DELAY = 1  # seconds

def clean_profile_url(url):
    return url.replace('/../', '/') if '/../' in url else url

def get_all_staff_links():
    try:
        print(f"Fetching staff directory from {BASE_URL}...")
        response = requests.get(BASE_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        staff_links = []
        container = soup.select_one(
            'body > div > div > div > div > div > div > div.row > div > div > div.row.form-inline')
        if not container:
            print("Staff container not found!")
            return []

        cards = container.select('center > div')
        print(f"Found {len(cards)} staff cards")

        for card in cards:
            profile_link = card.select_one('div > div > div > span > p > a')
            if profile_link and profile_link.has_attr('href'):
                full_text = card.get_text(separator="|", strip=True)
                parts = [p.strip() for p in full_text.split('|') if p.strip()]

                name, position = '', ''
                for i, part in enumerate(parts):
                    if any(title in part for title in ['DR.', 'PROF.', 'ASSOC. PROF.', 'TS.', 'MR.', 'MRS.', 'MS.']):
                        name = re.sub(r'\s+[A-Z]$', '', part)
                        name = re.sub(r'\s+', ' ', name)
                        if i + 1 < len(parts) and parts[i + 1] != "View Profile":
                            position = parts[i + 1]
                        break

                if name:
                    profile_path = clean_profile_url(profile_link['href'])
                    full_url = urljoin(BASE_URL, profile_path)
                    staff_links.append({
                        'name': name,
                        'position': position,
                        'profile_url': full_url
                    })
        return staff_links

    except Exception as e:
        print(f"Error fetching staff directory: {e}")
        return []


def clean_room_number(room: str) -> str:
    """
    Clean and standardize room numbers to the BR1XXX format.
    This function handles multiple room formats like 'BR1XXX', 'FCI BR1XXX', 'CQBR1XXX', etc.
    """
    room = room.upper().strip()  # Normalize the room string
    # Extract the room number pattern (e.g., BR2015, CQBR2015, FCI BR2015)
    match = re.search(r'BR\s*(\d{4})|CQBR\s*(\d{4})|FCI\s*BR\s*(\d{4})', room)
    if match:
        # Extract the room number (e.g., 2015)
        room_number = match.group(1) or match.group(2) or match.group(3)
        return f"BR{room_number}"  # Return standardized format like BR2015
    return ''  # Return empty string if no valid room number is found


def extract_profile_details(url, directory_data):
    try:
        time.sleep(DELAY)
        print(f"\nScraping: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        data = {
            'name': directory_data['name'],
            'position': directory_data['position'],
            'faculty': '',
            'room_number': '',
            'phone': '',
            'email': '',
            'profile_url': url,
            'profile_pic_file': None
        }

        # Extract text fields...
        cell = soup.select_one('div.col-md-9 table tbody tr td:nth-child(2)')
        if cell:
            faculty_text = cell.get_text(separator='|').split('|')
            if len(faculty_text) > 2:
                data['faculty'] = faculty_text[2].strip()

            room_el = cell.select_one('span:nth-child(7)')
            if room_el:
                room_text = room_el.get_text(strip=True)
                data['room_number'] = room_text.split(',')[0].strip()

            text_content = cell.get_text()
            phone_match = re.search(r'(\+?\d{2,3}-\d{7,8}|\d{10,11})', text_content)
            if phone_match:
                data['phone'] = phone_match.group(1)

            email_match = re.search(r'[\w\.-]+@mmu\.edu\.my', text_content)
            if email_match:
                data['email'] = email_match.group(0)

        # Fallback parsing
        full_text = soup.get_text(separator='\n')
        for line in [l.strip() for l in full_text.split('\n') if l.strip()]:
            if not data['faculty'] and 'faculty' in line.lower():
                data['faculty'] = line
            elif not data['room_number'] and re.search(r'(room|br|fci)\s*\d+', line.lower()):
                data['room_number'] = line.split(',')[0].strip()
            elif not data['phone'] and re.search(r'\d{2,3}-\d{7,8}', line):
                data['phone'] = re.search(r'\d{2,3}-\d{7,8}', line).group()
            elif not data['email'] and '@mmu.edu.my' in line:
                data['email'] = re.search(r'[\w\.-]+@mmu\.edu\.my', line).group()

        data['room_number'] = clean_room_number(data['room_number'])

        # Image extraction
        img_tag = soup.select_one('div.col-md-9 img')
        if img_tag and img_tag.has_attr('src'):
            img_src = img_tag['src'].strip()
            img_url = urljoin(url, img_src)
            img_response = requests.get(img_url, headers=HEADERS, timeout=10)
            img_response.raise_for_status()
            img_content = img_response.content
            img_name = os.path.basename(img_src)
            data['profile_pic_file'] = ContentFile(img_content, name=img_name)

        return data

    except Exception as e:
        print(f"Error scraping profile {url}: {e}")
        return None


class Command(BaseCommand):
    help = 'Updates Lecturer data from MMU Expert website'

    def handle(self, *args, **kwargs):
        # Clear all existing lecturers and their images
        for lecturer in Lecturer.objects.all():
            if lecturer.profile_pic:
                path = lecturer.profile_pic.path
                if os.path.isfile(path):
                    os.remove(path)
                    self.stdout.write(self.style.WARNING(f"Deleted image: {path}"))

        # Delete lecturer's data
        Lecturer.objects.all().delete()
        self.stdout.write(self.style.WARNING("Lecturer database and images cleared."))

        # Delete lecturer user accounts and reset ID sequence
        CustomUser.objects.filter(role='lecturer').delete()
        self.stdout.write(self.style.WARNING("All lecturer CustomUser accounts deleted."))

        # Start of data collection and account creation
        staff_directory_data = get_all_staff_links()
        if not staff_directory_data:
            self.stdout.write(self.style.ERROR("No staff profiles found. Exiting."))
            return

        for i, directory_data in enumerate(staff_directory_data, 1):
            self.stdout.write(self.style.NOTICE(
                f"\nProcessing {i}/{len(staff_directory_data)}: {directory_data['name']}"
            ))
            profile_data = extract_profile_details(directory_data['profile_url'], directory_data)

            if profile_data:
                self.stdout.write(self.style.NOTICE("Extracted data:"))
                self.stdout.write(pprint.pformat(profile_data))

                room_number = profile_data.get('room_number') or None
                email = profile_data.get('email')

                # Remove image file temporarily
                profile_pic_file = profile_data.pop('profile_pic_file', None)

                # Save or update the lecturer (excluding image for now)
                lecturer, created = Lecturer.objects.update_or_create(
                    name=profile_data['name'],
                    defaults={
                        **profile_data,
                        'room_number': room_number
                    }
                )

                # Save profile picture
                if profile_pic_file:
                    lecturer.profile_pic.save(profile_pic_file.name, profile_pic_file, save=True)

                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Created: {lecturer.name} | Room: {room_number or 'N/A'}"
                    ))
                else:
                    self.stdout.write(self.style.SUCCESS(
                        f"Updated: {lecturer.name} | Room: {room_number or 'N/A'}"
                    ))

                # Create CustomUser account for lecturer if email available
                if email:
                    try:
                        user, user_created = CustomUser.objects.get_or_create(
                            email=email,
                            defaults={
                                'username': f'lecturer{lecturer.id}',
                                'role': 'lecturer',
                            }
                        )
                        if user_created:
                            user.set_password('lecturerpass')  # change to a secure password policy later
                            user.save()
                            self.stdout.write(self.style.SUCCESS(
                                f"Created user for: {lecturer.name} | {user.username}"
                            ))
                        else:
                            self.stdout.write(self.style.WARNING(
                                f"User already exists for: {lecturer.name}"
                            ))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f"Failed to create user for {lecturer.name}: {e}"
                        ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"No email for {lecturer.name}, user account not created."
                    ))

        self.stdout.write(self.style.SUCCESS("Lecturer database update completed."))
