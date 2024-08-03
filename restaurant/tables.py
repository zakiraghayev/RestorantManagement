import csv

from termcolor import colored
from restaurant.constsants import TABLE_SIZES

from typing import List


class Table:

    def __init__(self, number: int = 1, size: int = 4):
        self.number = number
        self.size = size
        self._available = True

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        if size not in TABLE_SIZES:
            raise ValueError(
                f"Table sizes have to be with these values: {TABLE_SIZES}")
        self._size = size

    @property
    def available(self):
        return self._available

    def take(self):
        """ Make table unavailable and print message to customer """
        self._available = False
        print(
            colored(
                f"\nTable #{self.number} is yours! Please, have a seat.",
                "light_green"
            )
        )

    def pay(self):
        """ Make table available and print message to customer you paid"""
        self._available = True
        print(
            colored(
                "\nThanks!! It is great to have you in our restaurant.",
                "light_green"
            )
        )

    @classmethod
    def read_database(cls, db_path="db/tables.csv"):
        try:
            with open(db_path, encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                return [
                    cls(
                        number=int(row['number']),
                        size=int(row['size'])
                    ) for row in reader
                ]
        except FileNotFoundError:
            print(f"The file at {db_path} was not found.")
        except KeyError as e:
            print(f"Missing expected column in CSV file: {e}")

    def __str__(self) -> str:
        return f"Table #{self.number} (s: {self.size})"

    def __repr__(self) -> str:
        return f"Table #{self.number}"


class TableUtils:
    ASK_TABLE_NUMBER = colored("Please enter table number: ", "light_green")

    @staticmethod
    def list_available_tables(tables) -> List[Table]:

        availables = list(filter(lambda t: t.available, tables))

        ids = list(map(lambda t: t.number, availables))

        print(colored(f"\nAVAILABLE TABLES: {ids}", "blue"))

        return availables

    @staticmethod
    def get_table(availables) -> Table:
        number = int(input(TableUtils.ASK_TABLE_NUMBER))
        return list(
            filter(
                lambda t: t.number == number,
                availables
            )
        )[0]
