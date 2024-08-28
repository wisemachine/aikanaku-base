import csv
from django.core.management.base import BaseCommand
from data.models import DataInformation

def convert_size_to_gb(size_str):
    """Convert size string to a float representing size in GB."""
    if 'Gb' in size_str:
        return float(size_str.replace('Gb', '').strip())
    # Add more conversion logic if needed
    raise ValueError(f"Unsupported size format: {size_str}")

class Command(BaseCommand):
    help = 'Import data from CSV file into DataInformation model'

    def handle(self, *args, **kwargs):
        # Define the path to your CSV file
        csv_file_path = 'data/data_information.csv'  # Update the path if needed

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        # Convert the size from the CSV format to a float in GB
                        size_in_gb = convert_size_to_gb(row['size'])

                        data_info, created = DataInformation.objects.get_or_create(
                            name=row['project_name'],
                            storage_location=f"{row['storage']} - {row['location']}",  # Concatenate storage and location
                            access_list=row['access_list'],
                            size=size_in_gb,
                            cost=row['cost'],
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Successfully added {data_info.name}"))
                        else:
                            self.stdout.write(self.style.WARNING(f"{data_info.name} already exists"))
                    except ValueError as ve:
                        self.stdout.write(self.style.ERROR(f"Error processing row: {str(ve)}"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {csv_file_path} does not exist"))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f"Missing column in CSV: {str(e)}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
