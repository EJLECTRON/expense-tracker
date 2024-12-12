# expense-tracker

A simple expense tracking application that helps users manage their spending by categorizing expenses, filtering data, and generating reports. This project uses Python and MySQL as the database backend with SQLAlchemy as the ORM.

# **Features**


### **1. Category Management**
- Add, edit, delete, and view categories.


### **2. Expense Management**

  ## Essential Metadata
  
  The following metadata fields are required for every    transaction in the expense tracker:
  
  - **Transaction ID**
    - A unique identifier for each transaction.
    - Examples: `12345`, `abcde-67890`.
  
  - **Amount**
    - The monetary value of the transaction.
    - Examples: `50.75`, `-20.00` (negative for refunds or credits).
  
  - **Date and Time**
    - The exact timestamp when the transaction occurred.
    - Examples: `2024-11-21 14:30:00`, `2024-11-20 09:15:00`.
  
  - **Category**
    - The category assigned to the transaction to group similar expenses.
    - Examples: `Groceries`, `Entertainment`, `Utilities`.
  
  - **Description**
    - A short note or explanation about the transaction.
    - Examples: `"Weekly groceries at the supermarket"`, `"Netflix subscription for November"`.
  
  These fields form the backbone of the expense tracking functionality and ensure all transactions can be recorded, filtered, and analyzed effectively.


# Coming soon...

  *Optional Metadata*

  *The following metadata fields are optional but can enhance the functionality of your expense tracker:*
  
  *- **Payment Method***
    *- The method used to pay for the transaction.*
    *- Examples: `Credit Card`, `Cash`, `PayPal`, `Bank Transfer`.*
  
  *- **Merchant or Payee***
    *- The name of the merchant, store, or individual involved in the transaction.*
    *- Examples: `Amazon`, `Walmart`, `John Doe`.*
  
  *- **Location***
    *- The physical or online location where the transaction occurred.*
    *- Examples: `New York`, `Online`.*
  
  *- **Recurring Flag***
    *- Indicates whether the transaction is part of a recurring expense.*
    *- Examples: `True` for subscriptions, `False` otherwise.*
  
  *- **Budget Association***
    *- Links the transaction to a specific budget.*
    *- Examples: `Groceries Budget`, `Entertainment Budget`.*
  
  *- **Tags***
    *- Additional tags for flexible categorization.*
    *- Examples: `#holiday`, `#business`, `#organic`.*

---

  *## Advanced Metadata*
  
  *These fields are intended for advanced use cases or specific features, such as generating reports, handling currency conversions, or business-related tracking:*
  
  *- **Currency***
    *- The currency in which the transaction was made.*
    *- Examples: `USD`, `EUR`.*
  
  *- **Exchange Rate***
    *- The exchange rate used for currency conversion.*
    *- Examples: `1.13` for USD to EUR.*
  
  *- **Receipt or Attachment***
    *- A link to an uploaded receipt, invoice, or related document.*
    *- Examples: A URL to an image or PDF file.*
  
  *- **Expense Type***
    *- Specifies whether the expense is `Fixed` or `Variable`.*
    *- Examples: `Fixed` for rent, `Variable` for groceries.*
  
  *- **Transaction Status***
    *- The status of the transaction.*
    *- Examples: `Completed`, `Pending`, `Failed`.*


### **3. Expense Summaries**
- Filter expenses by:
  - **Category**: View all expenses under a specific category.
  - **Date Range**: Analyze expenses for a specific period.
- Generate summaries, such as total expenses per category.

### **4. Reports**
- **CSV Export**: Export expense data to a CSV file for external use.
- **Visual Breakdown**: Provide a graphical representation of expenses by category using pie charts or bar graphs.

---

## **Getting Started**

### **Prerequisites**
1. Python (3.8 or later)
2. MySQL database
3. Python packages (install via `pip`):
   - `SQLAlchemy`
   - `mysql-connector-python`
   - Optional: `matplotlib` (for visual reports)

---

### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker```


# CATEGORIES Table

This document provides an overview of the `CATEGORIES` table structure, including the columns, data types, and constraints.

## Table Structure

The `CATEGORIES` table is used to store different categories for the application. Below is the structure of the table:

| Column Name | Data Type    | Constraints                        | Description                           |
|-------------|--------------|-------------------------------------|---------------------------------------|
| `ID`        | `INT`        | `AUTO_INCREMENT`, `UNIQUE`, `PRIMARY KEY` | Unique identifier for each category. |
| `NAME`      | `VARCHAR(50)`| `NOT NULL`, `UNIQUE`, `DEFAULT 'MISCELLANEOUS'` | Name of the category.                |

### Columns

1. **ID**
   - Type: `INT`
   - Constraints:
     - `AUTO_INCREMENT`: Automatically increments for each new row.
     - `UNIQUE`: Ensures each value is unique.
     - `PRIMARY KEY`: Serves as the unique identifier for the table.
   - Description: Represents the unique ID for each category.

2. **NAME**
   - Type: `VARCHAR(50)`
   - Constraints:
     - `NOT NULL`: This column cannot be left empty.
     - `UNIQUE`: Ensures no duplicate category names are added.
     - `DEFAULT 'MISCELLANEOUS'`: If no value is provided, defaults to "MISCELLANEOUS".
   - Description: Represents the name of the category.

## Example Query to Create the Table

```sql
CREATE TABLE IF NOT EXISTS CATEGORIES (
    ID INT AUTO_INCREMENT UNIQUE PRIMARY KEY,
    NAME VARCHAR(50) NOT NULL UNIQUE DEFAULT "MISCELLANEOUS"
);```



# EXPENSES Table

The `EXPENSES` table is used to record and manage expense transactions in the system. Below is the structure and description of each column in the table.

## Table Structure

```sql
CREATE TABLE IF NOT EXISTS EXPENSES (
    ID INT AUTO_INCREMENT UNIQUE PRIMARY KEY,
    AMOUNT INT(6) NOT NULL,
    TIME_OF_TRANSACTION DATETIME NOT NULL,
    CATEGORY_NAME VARCHAR(50) NOT NULL,
    DESCRIPTION VARCHAR(511),
    FOREIGN KEY (CATEGORY_NAME) REFERENCES CATEGORIES(NAME) ON UPDATE CASCADE
);
```

## Columns

| Column Name         | Data Type          | Constraints                        | Description                                          |
|---------------------|--------------------|------------------------------------|------------------------------------------------------|
| `ID`                | `INT AUTO_INCREMENT` | `UNIQUE`, `PRIMARY KEY`            | Unique identifier for each expense record.          |
| `AMOUNT`            | `INT(6)`           | `NOT NULL`                         | The amount of the expense in numeric format.         |
| `TIME_OF_TRANSACTION` | `DATETIME`         | `NOT NULL`                         | The date and time when the transaction occurred.     |
| `CATEGORY_NAME`     | `VARCHAR(50)`      | `NOT NULL`, `FOREIGN KEY`          | The category of the expense, linked to `CATEGORIES.NAME`. |
| `DESCRIPTION`       | `VARCHAR(511)`     | Optional                           | Additional details or notes about the expense.       |

## Relationships
- The `CATEGORY_NAME` column is a foreign key referencing the `NAME` column in the `CATEGORIES` table.
  - **ON UPDATE CASCADE**: Any updates to the `NAME` column in the `CATEGORIES` table will be cascaded to this table.

## Notes
- Ensure the `CATEGORIES` table is created and populated with data before adding entries to the `EXPENSES` table.
- The `DESCRIPTION` column is optional and can be left empty if no additional details are needed.
