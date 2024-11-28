# expense-tracker

A simple expense tracking application that helps users manage their spending by categorizing expenses, filtering data, and generating reports. This project uses Python and MySQL as the database backend with SQLAlchemy as the ORM.

# **Features**


### **1. Category Management**
- Add, edit, delete, and view categories.
- Ensure unique category names to avoid duplicates.


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


  ## Optional Metadata

  The following metadata fields are optional but can enhance the functionality of your expense tracker:
  
  - **Payment Method**
    - The method used to pay for the transaction.
    - Examples: `Credit Card`, `Cash`, `PayPal`, `Bank Transfer`.
  
  - **Merchant or Payee**
    - The name of the merchant, store, or individual involved in the transaction.
    - Examples: `Amazon`, `Walmart`, `John Doe`.
  
  - **Location**
    - The physical or online location where the transaction occurred.
    - Examples: `New York`, `Online`.
  
  - **Recurring Flag**
    - Indicates whether the transaction is part of a recurring expense.
    - Examples: `True` for subscriptions, `False` otherwise.
  
  - **Budget Association**
    - Links the transaction to a specific budget.
    - Examples: `Groceries Budget`, `Entertainment Budget`.
  
  - **Tags**
    - Additional tags for flexible categorization.
    - Examples: `#holiday`, `#business`, `#organic`.

---

  ## Advanced Metadata
  
  These fields are intended for advanced use cases or specific features, such as generating reports, handling currency conversions, or business-related tracking:
  
  - **Currency**
    - The currency in which the transaction was made.
    - Examples: `USD`, `EUR`.
  
  - **Exchange Rate**
    - The exchange rate used for currency conversion.
    - Examples: `1.13` for USD to EUR.
  
  - **Receipt or Attachment**
    - A link to an uploaded receipt, invoice, or related document.
    - Examples: A URL to an image or PDF file.
  
  - **Expense Type**
    - Specifies whether the expense is `Fixed` or `Variable`.
    - Examples: `Fixed` for rent, `Variable` for groceries.
  
  - **Transaction Status**
    - The status of the transaction.
    - Examples: `Completed`, `Pending`, `Failed`.


### **3. Expense Summaries**
- Filter expenses by:
  - **Category**: View all expenses under a specific category.
  - **Date Range**: Analyze expenses for a specific period.
- Generate summaries, such as total expenses per category.

### **4. Reports**
- **CSV Export**: Export expense data to a CSV file for external use.
- **Visual Breakdown (Optional)**: Provide a graphical representation of expenses by category using pie charts or bar graphs.

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
   cd expense-tracker
