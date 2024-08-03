from typing import List
from typing import Tuple
from tabulate import tabulate

from termcolor import colored
from restaurant.constsants import RESTUARANT_NAME
from restaurant.items import Item
from restaurant.officiants import Officiant
from restaurant.tables import Table

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from reportlab.lib.colors import HexColor
import random


class OrderItem:

    def __init__(self, item: Item, quantity: int = 1) -> None:
        self.item = item
        self.quantity = quantity
        self.price = self.item.price_number * quantity


class Order:

    def __init__(
            self,
            officiant: Officiant,
            table: Table,
            order_items: List[OrderItem] = []
    ) -> None:
        self.officiant = officiant
        self.table = table
        self.order_items = order_items

    def add_order_item(self, item: Item):
        order_item, created = self.get_or_create_item(item=item)
        order_item.quantity = 1 if created else (order_item.quantity+1)
        order_item.price = order_item.quantity * item.price_number
        if created:
            self.order_items.append(order_item)

    def get_or_create_item(self, item: Item) -> Tuple[OrderItem, bool]:
        try:
            return list(filter(lambda oi: oi.item == item, self.order_items))[0], False
        except IndexError:
            return OrderItem(item), True


class OrderUtils:

    @staticmethod
    def ask_item_id_with_instruction() -> str:
        text = """
        Please enter the ID(s) of the items you wish to select. 
        You can enter an ID multiple times if you want to select the same item more than once. 
        If you finish selection, please hit Command+D (Mac) or Control+D (Windows/Linux).
        Item ID: """.replace("  ", "")
        return input(colored(text, 'yellow'))

    def ask_item_id() -> str:
        return input(colored("Item ID: ", 'yellow'))

    @staticmethod
    def take_order(order: Order, item_id: str,  items: List[Item]) -> Order:
        try:
            item = list(filter(lambda i: i.id == int(item_id), items))[0]
            order.add_order_item(item=item)
            print()
            print(colored(f"{item} was added successfully.", "green"))
            print(colored(OrderUtils.list_items(order=order), "light_magenta"))
            print()
            return order
        except (IndexError, ValueError):
            return order

    @staticmethod
    def list_items(order: Order):
        headers = ["ID", "Name", "Quantity", "Price"]
        items = [
            [
                order_item.item.id,
                order_item.item.name,
                order_item.quantity,
                order_item.price
            ]
            for order_item in order.order_items
        ]
        return tabulate(items, headers=headers)

    @staticmethod
    def bill(order: Order, file_path='db/bill.pdf'):
        c = canvas.Canvas(file_path, pagesize=letter)
        c.setTitle(f"{RESTUARANT_NAME} Bill")  # Set the PDF title
        width, height = letter

        # Set the background color to a parchment-like color
        c.setFillColor(HexColor("#F5DEB3"))  # Wheat color
        c.rect(0, 0, width, height, fill=1)

        # Add some texture by drawing random lines
        c.setStrokeColor(HexColor("#DEB887"))  # Burlywood color for texture
        for _ in range(100):
            x1 = random.randint(0, int(width))
            y1 = random.randint(0, int(height))
            x2 = random.randint(0, int(width))
            y2 = random.randint(0, int(height))
            c.line(x1, y1, x2, y2)

        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(0, 0.5, 1)  # Blue color for the header
        c.drawString(
            30,
            height - 40,
            f"Bill for Table {order.table.number}"
        )
        c.drawString(
            30,
            height - 60,
            f"Officiant: {order.officiant.full_name}"
        )

        c.setFont("Helvetica-Bold", 12)
        c.setFillColorRGB(0, 0, 0)  # Black color for the table headers
        c.drawString(30, height - 100, "ID")
        c.drawString(100, height - 100, "Name")
        c.drawString(300, height - 100, "Quantity")
        c.drawString(400, height - 100, "Price")

        y = height - 120
        total_price = 0

        c.setFont("Helvetica", 12)
        c.setFillColorRGB(0, 0, 0)  # Black color for the table content

        for item in order.order_items:
            c.drawString(30, y, str(item.item.id))
            c.drawString(100, y, item.item.name)
            c.drawString(300, y, str(item.quantity))
            c.drawString(400, y, f"${item.price:.2f}")
            total_price += item.price
            y -= 20

        c.setFont("Helvetica-Bold", 12)
        c.setFillColorRGB(0.85, 0.1, 0.1)  # Red color for the total price
        c.drawString(30, y - 20, f"Total: ${total_price:.2f}")

        c.showPage()
        c.save()

    @staticmethod
    def print_bill(order: Order):
        headers = ["ID", "Name", "Quantity", "Price"]
        items = [
            [
                order_item.item.id,
                order_item.item.name,
                order_item.quantity,
                f"${order_item.price:.2f}"
            ]
            for order_item in order.order_items
        ]

        # Calculate total price
        total_price = sum(order_item.price for order_item in order.order_items)
        items.append(["", "", "Total", f"${total_price:.2f}"])

        table = tabulate(items, headers=headers)
        print(table)
        return table
