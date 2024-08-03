import random

from restaurant.constsants import GOOD_BYE, THANK_YOU
from restaurant.orders import Order
from restaurant.orders import OrderUtils


from restaurant.tables import Table
from restaurant.tables import TableUtils

from restaurant.items import Item
from restaurant.items import ItemUtils

from restaurant.officiants import Officiant

from typing import List


def main():
    # Load data from csv files
    officiants, tables, items = load_data()

    officiant = welcome(officiants=officiants)
    table = select_table(tables=tables)
    order = make_an_order(officiant=officiant, table=table, items=items)

    check_bill(order)


def load_data() -> dict:
    return (
        Officiant.read_database(),
        Table.read_database(),
        Item.read_database(),
    )


def welcome(officiants: List[Officiant]) -> Officiant:
    """
    1. Choose random officiant from the list
    2. Deliver the welcome speech to customer
    3. return the officiant
    """
    officiant = random.choice(officiants)
    officiant.deliver_speech()
    return officiant


def select_table(tables: List[Table]) -> Table:
    """
    1. List availble table numbers
    2. Ask to input table number
    3. print success message to customer
    4. return table
    """

    while True:
        try:
            availables = TableUtils.list_available_tables(tables)
            table = TableUtils.get_table(availables)
            table.take()
            return table

        except (ValueError, IndexError):
            pass

        except EOFError:
            print(GOOD_BYE)
            break


def make_an_order(officiant: Officiant, table: Table, items: List[Item]) -> Order:
    """
    1. List menu items
    2. ask, 'Please, select menu items based on numbers'
    3. repeat (2) until customer hits cmd+D or ctrl+D'
    4. return order
    """
    ItemUtils.show_menu(items=items)
    item_id = OrderUtils.ask_item_id_with_instruction()
    order = Order(officiant, table, [])

    order = OrderUtils.take_order(
        order=order, item_id=item_id, items=items
    )

    while True:
        try:
            item_id = OrderUtils.ask_item_id()
            order = OrderUtils.take_order(
                order=order, item_id=item_id, items=items
            )
        except EOFError:
            print(THANK_YOU)
            return order


def check_bill(order):
    """
    It will save the bill as pdf
    """
    OrderUtils.bill(order)
    OrderUtils.print_bill(order)


if __name__ == "__main__":
    main()
