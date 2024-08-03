
# Restaurant Management System

### Video Demo
- [Watch the demo](https://www.youtube.com/watch?v=yONbD1I2Oy0&ab_channel=Contact)

## Introduction
This project is a simple restaurant management system written in Python. It simulates the process of managing orders, tables, items, and officiants in a restaurant setting. The system allows users to load data from CSV files, welcome customers, assign officiants, select tables, and make orders from available items.

## Features
- **Load Data**: Load data from CSV files for officiants, tables, and items.
- **Customer Interaction**: Welcome customers and assign an officiant.
- **Table Management**: Select a table for the customer.
- **Order Processing**: Make an order from available items.
- **Billing**: Generate bills and print them.

## File Descriptions

### `restaurant/__init__.py`
This file initializes the restaurant package.

### `restaurant/constsants.py`
Contains constant values used across the project. This includes fixed values.

### `restaurant/items.py`
Defines the `Item` class which represents an item on the menu. This class includes methods for item initialization, loading from CSV, and price calculations.

### `restaurant/officiants.py`
Defines the `Officiant` class which represents an officiant in the restaurant. This class includes methods for officiant initialization, loading from CSV.

### `restaurant/orders.py`
Defines the `Order` class which manages customer orders. This class includes methods for adding items to the order, calculating the total bill, and printing the bill.

### `restaurant/tables.py`
Defines the `Table` class which represents a table in the restaurant. This class includes methods for table initialization, loading from CSV, and managing occupancy.

### `restaurant/project.py`
The main driver script that utilizes all the classes and manages the restaurant workflow. This script includes functions for loading data, handling customer interactions, and processing orders.

### `README.md`
This file provides an overview of the project, its features, and details about each file.

### `requirements.txt`
Lists the dependencies required to run the project. The dependencies are:
- `rich==13.7.1`
- `tabulate`
- `reportlab`
- `pytest`
- `pytest-mock`

### `test_project.py`
Contains unit tests for the project. It uses `pytest` to run the tests and `pytest-mock` for mocking objects.

## Design Choices
### Loading Data
The project loads data from CSV files to ensure easy updates and modifications. This design choice allows for a flexible and scalable system, as new items, tables, or officiants can be added by simply updating the respective CSV files.

### Customer Interaction
A user-friendly interface is implemented using the `rich` library to provide a visually appealing and interactive experience for users. This library allows for colorful and well-structured console outputs.

### Order Processing
The system handles orders efficiently by creating instances of the `Order` class. Each order can have multiple items, and the total bill is calculated dynamically. The `tabulate` library is used to display order details in a tabular format.

### Billing
Bills are generated using the `reportlab` library, which allows for professional and printable PDF bills. This choice ensures that the billing process is both user-friendly and functional for real-world applications.

## Running the Project
To run the project, follow these steps:
1. Install the dependencies using `pip install -r requirements.txt`.
2. Run the main script using `python project.py`.

## Conclusion
This project demonstrates a comprehensive approach to building a restaurant management system using Python. It incorporates best practices in software development, including modular design, efficient data handling, and a focus on user experience. The system is designed to be extendable and can be adapted for more complex restaurant management needs.
