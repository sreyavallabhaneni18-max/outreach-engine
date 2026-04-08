# Outreach Engine Frontend

## Intent

The Outreach Engine Frontend is a React-based web application built with Vite that provides a user interface for managing and monitoring outreach campaigns. It allows users to compose and send messages via various channels (email, SMS, WhatsApp) and track the delivery status of these messages in real-time. This frontend interacts with the backend API to handle outreach operations, making it easy to manage communication campaigns efficiently.

The application is designed to be intuitive and responsive, using modern web technologies to ensure a smooth user experience.

## Installation

To set up the frontend locally, ensure you have Node.js (version 16 or higher) installed on your system.

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the dependencies:
   ```
   npm install
   ```

This will install all necessary packages, including React, Vite, Tailwind CSS, and development tools like ESLint.

## Setup

After installation, you can start the development server:

1. Run the development server:
   ```
   npm run dev
   ```

   This will start the Vite development server, typically on `http://localhost:5173`. The app supports Hot Module Replacement (HMR) for a seamless development experience.

2. For production builds:
   ```
   npm run build
   ```

   This creates an optimized build in the `dist` folder.

3. To preview the production build locally:
   ```
   npm run preview
   ```

4. Linting:
   ```
   npm run lint
   ```

   This runs ESLint to check for code quality issues.

### Backend Integration

This frontend requires the Outreach Engine Backend to be running. Ensure the backend is set up and running (refer to the backend README for instructions). The frontend communicates with the backend API, typically running on `http://localhost:8000` by default.

Update the API endpoints in `src/services/outreachApi.js` if the backend is running on a different port or host.

## Project Structure

```
frontend/
├── public/                 # Static assets served directly
├── src/
│   ├── assets/             # Additional assets (images, fonts, etc.)
│   ├── components/         # Reusable React components
│   │   ├── DeliveryStatusCard.jsx  # Component for displaying message delivery status
│   │   ├── Loader.jsx              # Loading spinner component
│   │   └── OutreachForm.jsx        # Form for composing and sending outreach messages
│   ├── services/           # API service functions
│   │   └── outreachApi.js  # Functions for interacting with the backend API
│   ├── utils/              # Utility functions
│   │   └── validators.js   # Validation helpers for forms
│   ├── App.jsx             # Main application component
│   ├── App.css             # Application-specific styles
│   ├── index.css           # Global styles and Tailwind imports
│   └── main.jsx            # Application entry point
├── eslint.config.js        # ESLint configuration
├── index.html              # Main HTML template
├── package.json            # Project dependencies and scripts
├── vite.config.js          # Vite configuration with React and Tailwind plugins
└── README.md               # This file
```

### Key Components

- **App.jsx**: The root component that sets up routing and overall layout.
- **OutreachForm.jsx**: Handles user input for creating new outreach messages.
- **DeliveryStatusCard.jsx**: Displays the status of sent messages.
- **Loader.jsx**: A simple loading indicator used throughout the app.
- **outreachApi.js**: Contains functions to make HTTP requests to the backend for sending messages and fetching status updates.

### Styling

The application uses Tailwind CSS for styling, providing utility-first CSS classes for rapid UI development. Custom styles are defined in `App.css` and `index.css`.

### Configuration

- **Vite Config**: Configured with React plugin for JSX support, Tailwind CSS plugin for styling, and path aliases (`@` for `src/`).
- **ESLint**: Set up with React-specific rules for code quality.

## Technologies Used

- **React**: For building the user interface.
- **Vite**: For fast development and building.
- **Tailwind CSS**: For styling.
- **ESLint**: For code linting.

## Contributing

When contributing to this project, ensure that:

- All new components are placed in the `src/components/` directory.
- API calls are abstracted in `src/services/`.
- Utility functions go in `src/utils/`.
- Run `npm run lint` before committing to maintain code quality.

## Troubleshooting

- If the development server doesn't start, ensure Node.js is installed and ports 5173 (frontend) and 8000 (backend) are available.
- For styling issues, check that Tailwind CSS is properly configured in `vite.config.js`.
- If API calls fail, verify the backend is running and the endpoints in `outreachApi.js` match the backend configuration.
