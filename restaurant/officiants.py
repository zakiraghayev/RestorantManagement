import csv
from datetime import datetime

from restaurant.constsants import RESTUARANT_NAME
from termcolor import colored


class Officiant:

    def __init__(self, id: int = 1, full_name: str = 'Officiant'):
        self.id = id
        self.full_name = full_name

    def deliver_speech(self):
        speech = f"""
        Good {self.get_day_term()}, and welcome to {RESTUARANT_NAME}!
        My name is {self.full_name}, and I’ll be taking care of you today.

        We’re delighted to have you with us. We have some lovely tables available for you.
        What would you prefer among these tables?
        """
        print(colored(speech, 'cyan'))
        return speech

    def get_day_term(self):
        # Get the current time
        current_time = datetime.now().time()

        # Define the time ranges for morning, afternoon, and evening
        morning_start = datetime.strptime("06:00", "%H:%M").time()
        afternoon_start = datetime.strptime("12:00", "%H:%M").time()
        evening_start = datetime.strptime("18:00", "%H:%M").time()

        if morning_start <= current_time < afternoon_start:
            return "morning"
        elif afternoon_start <= current_time < evening_start:
            return "afternoon"
        else:
            return "evening"

    @classmethod
    def read_database(cls, db_path="db/officiants.csv"):
        try:
            with open(db_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                return [
                    cls(
                        id=int(row['id']),
                        full_name=row['full_name']
                    ) for row in reader
                ]
        except FileNotFoundError:
            print(f"The file at {db_path} was not found.")
        except KeyError as e:
            print(f"Missing expected column in CSV file: {e}")

    def __str__(self) -> str:
        return f"Officiant #{self.id}. {self.full_name}"

    def __repr__(self) -> str:
        return f"Officiant {self.full_name}"
