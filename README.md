# Air Ticket Booking System

A lightweight web-based air ticket management system built with **Flask**, **SQLite**, and **HTML/CSS**, supporting flight management, passenger booking, cancellation, and real-time information display.

## ✈️ Features

- **Flight Management**: Add, edit, and manage flight information including flight ID, model, destination, and available seats.
- **Booking System**: Operators can book tickets for passengers with automatic seat assignment and duplicate checks.
- **Cancellation Support**: Tickets can be marked as cancelled with historical data preserved.
- **Role-Based Access**:
  - **Admin**: Manage flight and operator info.
  - **Operator**: Book, cancel, and view tickets.
- **Information Dashboard**: Summarized tables of all flights and bookings with intuitive UI and cancellation indicators.
- **Data Persistence**: Uses embedded **SQLite** database for local, serverless deployment.
- **Secure Login**: Simple role-based login with encrypted credential storage.

## 🛠 Tech Stack

| Layer        | Technology       |
|--------------|------------------|
| Backend      | Python + Flask   |
| Database     | SQLite           |
| Frontend     | HTML, CSS, Jinja2 Templates |
| Environment  | Windows, Chrome browser |
| IDE          | VS Code          |

## 📂 Project Structure

```

air\_ticket\_system-cope/
├── app.py                # Main application routes
├── db\_utils.py           # Database interaction logic
├── passwords.json        # Stores admin/operator credentials (hashed)
├── templates/            # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── admin.html
│   ├── operator.html
│   ├── book\_ticket.html
│   ├── cancel\_ticket.html
│   ├── edit\_flights.html
│   ├── edit\_operator.html
│   ├── all\_info.html
│   └── view\_flights.html
├── static/               # (Optional) CSS / image files
└── database.db           # SQLite data file (auto-created)

````

## 🚀 How to Run

> Requires Python 3.8+ and Flask

1. Clone this repository  
   ```bash
   git clone https://github.com/YuyangZhu7/air_ticket_system-cope.git
   cd air_ticket_system-cope
````

2. Create a virtual environment (optional but recommended)

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies

   ```bash
   pip install flask
   ```

4. Run the app

   ```bash
   python app.py
   ```

5. Open in browser:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

## ✅ Default Roles (for testing)

> Stored in `passwords.json`

* **Admin**

  * Username: `admin`
  * Password: `admin`
* **Operator**

  * Username: `operator`
  * Password: `operator`

> ⚠️ Change passwords before deployment.

## 📌 Notes

* System auto-creates tables and default credentials if they don’t exist.
* Flight and passenger data are stored in `database.db`.
* Cancelling a ticket preserves the record with a visual deletion mark (strikethrough).
* Frontend rendering uses Jinja2 templates.

## 📄 License

This project is for academic demonstration purposes only.



