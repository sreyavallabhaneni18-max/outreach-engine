# Outreach Engine

A comprehensive outreach engine that enables sending messages to candidates via multiple channels including Email, SMS, and WhatsApp. The system consists of a React-based frontend for user interaction and a FastAPI backend for handling API requests, message routing, and status tracking.

## Project Structure

- **frontend/**: React application built with Vite and Tailwind CSS for the user interface.
- **backend/**: FastAPI application with SQLAlchemy for database management and message processing.

## Setup

### Prerequisites

- Node.js (version 16 or higher)
- Python 3.8+
- Git

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd outreach-engine
   ```

2. Set up the backend:
   - Navigate to the backend directory: `cd backend`
   - Create a virtual environment: `python -m venv venv`
   - Activate the virtual environment: `source venv/bin/activate` (on macOS/Linux)
   - Install dependencies: `pip install -r requirements.txt`
   - Create a `.env` file in the backend directory with necessary environment variables (e.g., API keys for Mailgun, Twilio, etc.)
   - For detailed backend setup, see [backend/README.md](backend/README.md)

3. Set up the frontend:
   - Navigate to the frontend directory: `cd ../frontend`
   - Install dependencies: `npm install`
   - For detailed frontend setup, see [frontend/README.md](frontend/README.md)

### Database Setup

The backend uses SQLite as the database, stored in `backend/outreach.db`. The database tables are automatically created when the backend application starts, using SQLAlchemy's declarative base. No manual database setup is required beyond ensuring the backend has write permissions to create the database file.

### Running the Application

1. Start the backend:
   - From the backend directory: `uvicorn app.main:app --reload`
   - The API will be available at `http://localhost:8000`

2. Start the frontend:
   - From the frontend directory: `npm run dev`
   - The UI will be available at `http://localhost:5173`

Ensure both services are running simultaneously for full functionality.

## Features

- Multi-channel messaging (Email, SMS, WhatsApp)
- Real-time delivery status tracking
- Webhook support for status updates
- Responsive web interface
- RESTful API for integrations

## Contributing

Please refer to the individual README files in the frontend and backend directories for specific contribution guidelines.

## License

[Add license information here]
