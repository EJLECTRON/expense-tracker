# expence-tracker

A simple expense tracking application that helps users manage their spending by categorizing expenses, filtering data, and generating reports. This project uses Python and MySQL as the database backend with SQLAlchemy as the ORM.

---

## **Features**

### **1. Category Management**
- Add, edit, delete, and view categories.
- Ensure unique category names to avoid duplicates.

### **2. Expense Management**
- Add, edit, delete, and view expenses.
- Store metadata such as:
  - **Date**: The date of the expense.
  - **Description**: A brief explanation of the expense.
  - **Category**: Links to predefined categories for better organization.

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
