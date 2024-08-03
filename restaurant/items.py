import csv
from typing import List

from tabulate import tabulate
from termcolor import colored


class Item:

    def __init__(self, id: int = 1, name: str = 'Small Regular Pizza', price: float = 19):
        self.id = id
        self.name = name
        self.price = price

        self._attributes = [self.id, self.name, self.price]
        self._index = 0

    @property
    def price_number(self):
        return float(self._price)

    @property
    def price(self):
        return f"${self._price}"

    @price.setter
    def price(self, price):
        if price < 0:
            raise ValueError("Price can not be negative")
        self._price = price

    @classmethod
    def read_database(cls, db_path="db/items.csv"):
        try:
            with open(db_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                return [
                    cls(
                        id=int(row['id']),
                        name=row['name'],
                        price=float(row['price'])
                    ) for row in reader
                ]
        except FileNotFoundError:
            print(f"The file at {db_path} was not found.")
        except KeyError as e:
            print(f"Missing expected column in CSV file: {e}")

    def __str__(self) -> str:
        return f"Item #{self.id}. {self.name} {self.price}"

    def __repr__(self) -> str:
        return f"Item #{self.id}. {self.name}"

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._attributes):
            result = self._attributes[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration


class ItemUtils:

    @staticmethod
    def show_menu(items: List[Item]):
        print("\n\n ####### Here is our menu. #######\n")
        print(
            colored(
                tabulate(
                    items,
                    headers=["ID", "Name", "Price"]
                ),
                "light_cyan"
            )
        )
