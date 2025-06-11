# Income Expense Calculation Application (Freelancer Data Tracking)

## 🚀 About the Project

This project is a simple financial tracking application that allows you to monitor your daily income and expenses using a Streamlit web interface. The entered income and expenses are stored in a MySQL database and can be optionally visualized with summary charts.

## ✨ Features

* **Income/Expense Entry:** Input income and expense amounts for a specific date.
* **Net Income Calculation:** The application calculates the net income (income - expense) for the chosen date and stores it in the database.
* **Data Update:** When a new net income is entered for an existing date, it updates the current record by adding to it (upsert operation).
* **Record Deletion:** Delete all income/expense records for a selected date from the database.
* **View Records by Date:** Display the net income record for a specific selected date.
* **View All Records:** List all net income records from the database in a tabular format.
* **Data Visualization:** Generate a bar chart showing daily total net incomes.
* **User-Friendly Interface:** Easy and interactive web interface powered by Streamlit.

## 🛠️ Technologies Used

* **Python 3.x**
* **Streamlit:** For building the web interface.
* **MySQL:** As the database backend.
* **`mysql-connector-python`:** For Python-MySQL connectivity.
* **Pandas:** For data manipulation and DataFrame creation.
* **Matplotlib:** For data visualization (charts).
* **NumPy:** (Possibly used indirectly as a dependency of Pandas).

## 🚀 Setup and Running

### Prerequisites

* **Python 3.x** installed.
* **MySQL Server** installed and running.

### Step 1: Install Python Dependencies

Open a terminal in your project directory and run the following command:

```bash
pip install streamlit mysql-connector-python pandas matplotlib numpy
