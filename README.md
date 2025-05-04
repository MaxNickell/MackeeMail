# MackeeMail

MackeeMail is a Flask-based messaging web application that allows users to communicate through private messages and a public message board.

## Features

- User authentication (registration, login, logout)
- Private messaging between users
- Public message board
- Message deletion functionality
- Secure password storage using hashing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MackeeMail.git
cd MackeeMail
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

## Database Setup

The application can use either SQLite (development) or PostgreSQL (production), controlled by the `ENV` variable in `app.py`:

- `ENV = 'dev'`: Uses SQLite (default for local development)
- `ENV = 'prod'`: Uses PostgreSQL (for production deployment)

### Creating the Database

To initialize the database tables:
```bash
python3 create_db.py
```

### Clearing the Database

If you need to clear all data and reset the database:
```bash
python3 clear_db.py
```

## Running the Application

1. Make sure your virtual environment is activated:
```bash
source venv/bin/activate
```

2. Run the application:
```bash
python3 app.py
```

The application will be accessible at:
- http://127.0.0.1:5001/ (locally)
- http://your-ip-address:5001/ (on your network)

## Project Structure

- `app.py`: Main application file with all routes and models
- `create_db.py`: Script to initialize the database tables
- `clear_db.py`: Script to clear all data from the database
- `templates/`: HTML templates for the web interface
  - `base.html`: Main layout template
  - `home.html`: Private messaging interface
  - `login.html`: User login form
  - `signup.html`: User registration form
  - `messageboard.html`: Public message board interface
- `static/`: Static files (JavaScript, CSS)
  - `index.js`: JavaScript for message deletion functionality

## Environment Switching

To switch between development and production environments:

1. Edit the `ENV` variable in `app.py`:
   - For development (SQLite): `ENV = 'dev'`
   - For production (PostgreSQL): `ENV = 'prod'`

2. In production, update the PostgreSQL connection string in `app.py`.
