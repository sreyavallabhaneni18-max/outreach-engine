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

## Providers Chosen and Why

- **Mailgun (Email)**  
  Mailgun was chosen for email delivery due to its simple REST API and quick sandbox setup. It allows sending test emails without complex domain configuration, making it ideal for rapid development and testing.

- **Twilio (SMS)**  
  Twilio was selected for SMS because of its reliable infrastructure, clear API design, and strong documentation. It also provides built-in delivery status callbacks, which makes it easy to implement real-time message status tracking.

- **Twilio (WhatsApp Sandbox)**  
  Twilio’s WhatsApp sandbox was used to support WhatsApp messaging without requiring a production business account. Since it follows a similar API pattern to SMS, it allowed reuse of channel logic and simplified integration.

## Design Decisions and Tradeoffs

- **Monolithic Architecture (FastAPI)**  
  The system is implemented as a single service instead of multiple microservices. This reduces setup and deployment complexity for the scope of the project, while still keeping the code modular internally. In a production system, this could be split into separate services (e.g., messaging, status tracking, workers).

- **Channel Abstraction Layer**  
  Each communication channel (email, SMS, WhatsApp) is implemented as a separate module/class. This allows new providers or channels to be added with minimal changes to the core orchestration logic, improving extensibility.

- **SQLite for Persistence**  
  SQLite was chosen for simplicity and zero-setup local development. This avoids the overhead of managing a full database system. The tradeoff is limited scalability and concurrency compared to databases like PostgreSQL.

- **Webhook-Based Status Updates**  
  Delivery status updates are handled via provider webhooks instead of polling. This mirrors real-world systems and ensures more accurate, real-time updates. The tradeoff is additional setup complexity (e.g., needing ngrok for local testing).

- **Asynchronous Multi-Channel Processing**  
  Messages across selected channels are orchestrated concurrently using `asyncio.gather`, reducing overall latency

- **Simple Retry Strategy**  
  Basic retry logic is implemented with a fixed retry count and exponential delay. This keeps the system simple, but lacks more advanced retry handling such as failure classification or dead-letter queues.

- **Shared Database Session Across Tasks**  
  The same SQLAlchemy session is passed into concurrent channel tasks for simplicity. While sufficient for this scope, a more robust design would isolate sessions per task to avoid shared transaction state.

- **Minimal Frontend for Demonstration**  
  A lightweight React frontend was included to demonstrate end-to-end functionality. The focus of the project is backend design, so the UI is intentionally simple.

- **No Authentication Layer**  
  Authentication and authorization were not implemented to keep the scope focused on core messaging functionality. In a real-world system, secure access control would be essential.

## What I’d Do Differently With More Time

- **Move to a Scalable Database (PostgreSQL)**  
  Replace SQLite with PostgreSQL to support higher concurrency, better indexing, and production-grade reliability.

- **Introduce Background Processing (Queues/Workers)**  
  Use a message queue (e.g., RabbitMQ, Redis, or Celery) to handle message sending and retries outside the request lifecycle. This would improve scalability and prevent blocking API requests.

- **Add Rate Limiting and Provider Throttling Handling**  
  Handle external provider rate limits more gracefully to avoid failures during high traffic or bursts.

- **Improve Observability**  
  Add structured logging, metrics, and distributed tracing to monitor system health and debug issues more effectively.

- **Add Authentication and Authorization**  
  Secure the API with authentication (e.g., JWT) and role-based access control to make it production-ready.

- **AI-driven Workflow Extensions**  
  Introduce AI-powered components for specific tasks such as message personalization, content optimization, and delivery outcome analysis. These would be designed as separate modules to enhance the outreach process without impacting the core messaging pipeline.

- **Add Dashboard View for Message Tracking**  
  Extend the frontend to include a dashboard that fetches and displays all outreach messages along with their current statuses. This would provide better visibility into message history, delivery outcomes, and system activity, improving usability for monitoring campaigns.

- **Add Comprehensive Testing**  
  Include unit tests, integration tests, and webhook simulation tests to improve reliability and confidence in changes.

- **Containerization and Deployment**  
  Dockerize the application and set up CI/CD pipelines for easier deployment and environment consistency.

- **Improve Frontend Experience**  
  Add real-time updates (e.g., WebSockets), better error states, and improved UX () for monitoring message status.