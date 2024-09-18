# Create the README.md file with the provided content

readme_content = """
# Osztalype.nz 1.0 Beta

## Description

**Osztalype.nz** is a simple class accounting app built using **React** for the frontend and **Flask** for the backend, with **MySQL** as the database. Each student in a class is required to pay an amount every month. This application allows managing payments (add/take money), tracking transactions, and managing the list of students. Each class has a separate subdomain, and the system is built to handle multiple classes independently, each with its own database.

---

## Features

- **PIN-Based Authentication**: The app uses a PIN-based login instead of username/password for access.
- **Multi-Class Support**: Supports multiple classes, each managed as a separate subdomain (e.g., `domain.com/classa`, `domain.com/classb`).
- **Add Money**: Easily add money to a student’s account.
- **Take Money**: Record a withdrawal with a reason (e.g., for field trips).
- **Account Movements**: View all transactions (payments and withdrawals) in a detailed table, with a balance for each student.
- **Manage Students**: Add, modify, or delete students from the class. The deletion is a "soft delete", meaning the student's data remains in the system but is hidden from view.
- **Mobile & PC Responsive Design**: Designed for both mobile and PC, with adaptive layouts and UI.

---

## Tech Stack

### Frontend:
- **React**
- **React Router Dom** for navigation
- **Axios** for API requests
- **CSS** for styling

### Backend:
- **Flask**
- **Flask-CORS** for handling cross-origin resource sharing
- **MySQL** as the database
- **dotenv** for environment configuration

### Database:
- **MySQL**
    - Each class has a separate database.
    - The application handles the creation of a database when a new class is created.

---

## Installation

### Prerequisites:
- **Node.js**
- **Python 3.x**
- **Docker** (for MySQL)

### Backend Setup:

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repository/osztalypenz.git
   cd osztalypenz/backend
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the MySQL database using Docker:
   ```bash
   docker-compose up -d
   ```

5. Create a `.env` file with your database credentials:
   ```
   DB_USER=root
   DB_PASSWORD=yourpassword
   DB_HOST=localhost
   DB_PORT=3306
   ```

6. Run the backend:
   ```bash
   python3 app.py
   ```

### Frontend Setup:

1. Navigate to the frontend directory:
   ```bash
   cd osztalypenz/osztalypenz-app
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the frontend:
   ```bash
   npm start
   ```

The app should now be running at [http://localhost:3000](http://localhost:3000).

---

## Usage

1. **Login**: After starting the application, you will be prompted to enter a PIN to access the dashboard.
2. **Add Money**: Go to "Befizetés", select a student, and add the required amount.
3. **Take Money**: Go to "Kivét", enter the amount and reason for the withdrawal.
4. **View Movements**: View the list of transactions under "Pénzmozgások", with a detailed breakdown of payments and withdrawals.
5. **Manage Students**: In the "Tanulók" section, you can add, modify, or soft-delete a student.

---

## API Endpoints

### Auth:
- `POST /auth/pin-login`: Authenticate using a PIN code.

### Account Movements:
- `GET /:className/account-movements`: Get all transactions for a class.

### Add Money:
- `POST /:className/add-money`: Add money to a student's account.

### Take Money:
- `POST /:className/take-money`: Withdraw money for a specific reason.

### Manage Children:
- `GET /:className/children`: List all children (excluding soft-deleted ones).
- `POST /:className/children`: Add a new child.
- `PUT /:className/children/:id`: Modify a child’s name.
- `DELETE /:className/children/:id`: Soft delete a child.

### Class Creation:
- `POST /create-class`: Create a new class and initialize a new database.

---

## Known Issues

- Ensure the MySQL container is running before starting the backend.
- When adding money, the amount and student name reset after successful operation to avoid duplicate entries.

---

## Future Enhancements

- Add functionality for setting monthly payments.
- Improve the transaction filtering by date range.
- Integrate more detailed statistics and reporting for each class.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributors

- Your Name (your-email@example.com)
