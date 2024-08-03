from unittest.mock import MagicMock
from project import load_data
from project import welcome
from project import select_table
from project import make_an_order
from project import check_bill

from restaurant.items import Item
from restaurant.officiants import Officiant
from restaurant.orders import Order
from restaurant.orders import OrderUtils
from restaurant.tables import Table


def test_load_data(mocker):
    mock_officiant = MagicMock()
    mock_officiant.id = 1
    mock_officiant.full_name = 'John Doe'

    mock_table = MagicMock()
    mock_table.number = 1

    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.name = 'Pizza'
    mock_item.price = 19
    # Arrange: set up the mock return values
    mock_officiant_read_database = mocker.patch(
        'restaurant.officiants.Officiant.read_database',
        return_value=[mock_officiant]
    )
    mock_table_read_database = mocker.patch(
        'restaurant.tables.Table.read_database',
        return_value=[mock_table]
    )
    mock_item_read_database = mocker.patch(
        'restaurant.items.Item.read_database',
        return_value=[mock_item]
    )

    # Act: call the function under test
    result = load_data()

    # Assert: check that the function returns the correct values
    assert len(result[0]) == 1
    assert result[0][0].full_name == 'John Doe'
    assert len(result[1]) == 1
    assert result[1][0].number == 1
    assert len(result[2]) == 1
    assert result[2][0].name == 'Pizza'
    assert result[2][0].price == 19

    # Verify that the read_database class methods were called once
    mock_officiant_read_database.assert_called_once()
    mock_table_read_database.assert_called_once()
    mock_item_read_database.assert_called_once()


def test_welcome(mocker):
    # Arrange: create a list of mock Officiant objects
    mock_officiants = [MagicMock(spec=Officiant) for _ in range(3)]

    # Patch random.choice to always return the first officiant in the list
    mocker.patch('random.choice', return_value=mock_officiants[0])

    # Act: call the function under test
    chosen_officiant = welcome(mock_officiants)

    # Assert: check that the chosen officiant is correct and deliver_speech was called
    assert chosen_officiant == mock_officiants[0]
    chosen_officiant.deliver_speech.assert_called_once()


def test_select_table(mocker):
    # Arrange: create a list of mock Table objects
    mock_tables = [MagicMock(spec=Table) for _ in range(3)]
    mocker.patch(
        'restaurant.tables.TableUtils.list_available_tables',
        return_value=mock_tables
    )
    mocker.patch(
        'restaurant.tables.TableUtils.get_table',
        return_value=mock_tables[0]
    )
    mock_tables[0].take = MagicMock()

    # Act: call the function under test
    selected_table = select_table(mock_tables)

    # Assert: check that the correct table was selected and take was called
    assert selected_table == mock_tables[0]
    selected_table.take.assert_called_once()


def test_make_an_order(mocker):
    # Arrange: create mock Officiant, Table, and Item objects
    mock_officiant = MagicMock(spec=Officiant)
    mock_table = MagicMock(spec=Table)
    mock_items = [MagicMock(spec=Item) for _ in range(3)]

    mocker.patch('restaurant.items.ItemUtils.show_menu')
    mocker.patch(
        'restaurant.orders.OrderUtils.ask_item_id_with_instruction',
        return_value=1
    )
    mocker.patch(
        'restaurant.orders.OrderUtils.take_order',
        side_effect=lambda order, item_id, items: order
    )
    mocker.patch(
        'restaurant.orders.OrderUtils.ask_item_id',
        side_effect=EOFError
    )

    # Act: call the function under test
    order = make_an_order(mock_officiant, mock_table, mock_items)

    # Assert: check that the order is an instance of Order
    assert isinstance(order, Order)


def test_check_bill(mocker):
    # Arrange: create a mock Order object
    mock_order = MagicMock(spec=Order)
    mocker.patch('restaurant.orders.OrderUtils.bill')
    mocker.patch('restaurant.orders.OrderUtils.print_bill')

    # Act: call the function under test
    check_bill(mock_order)

    # Assert: check that the bill method was called with the order
    OrderUtils.bill.assert_called_once_with(mock_order)
    OrderUtils.print_bill.assert_called_once_with(mock_order)
