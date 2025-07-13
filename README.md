# Finance Dashboard

Finance Dashboard is a web application for tracking income and expenses over time. It provides users with a streamlined user interface for adding transactions, viewing them, and understanding spending patterns through charts.

## Table of Contents

1. [Features](#features)
2. [Setup and Installation](#setup-and-installation)
3. [Running the Application](#running-the-application)
4. [Usage](#usage)
5. [Technologies Used](#technologies-used)

## Features

- User authentication for secure access using Flask-Login
- Add, edit, and delete transactions with categories
- Real-time analytics with charts for income, expenses, and category breakdowns
- Responsive dashboard

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Shivamsky0808/Finance_Dasboard.git
   cd Finance_Dasboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

- Run the application with:
  ```bash
  python app.py
  ```

- Access the application by navigating to `http://127.0.0.1:5001` in your web browser.

## Usage

- **Login/Register:** Sign up to start logging your transactions.
- **Dashboard:** Get an overview of your total income, expenses, and net savings.
- **Add Transaction:** Log new income or expense entries.
- **View Transactions:** Browse and manage your financial entries.
- **Analytics:** View interactive charts representing your financial activity.

## Technologies Used

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend:** Bootstrap, Chart.js, JavaScript
- **Database:** SQLite (default)

