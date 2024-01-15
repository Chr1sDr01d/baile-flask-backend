# Baile Flask Backend

## Overview

The Baile Flask Backend serves as the server-side component for the Baile smart home management system. It handles API requests from the frontend and communicates with various smart device APIs, providing a central point of control and data processing.

## Features

- **API Integration:** Connects with smart home devices like Govee, Samsung TV, and Blink cameras.
- **Data Processing:** Processes data received from devices and sends actionable commands.
- **Secure and Scalable:** Built with Flask, offering robustness and scalability.

## Getting Started

### Prerequisites

- Python 3
- Flask
- Requests library

### Installation

1. Clone the repository:

```shell
git clone https://github.com/Chr1sDr01d/baile-flask-backend.git
```
2. Navigate to the project directory:

```shell
cd baile-flask-backend
```
3. Install dependencies:
```shell
pip install -r requirements.txt
```


### Running the Application

1. To start the server, run:

```shell
flask run
```

This will start the Flask server on `http://localhost:5000`.

## Configuration

- Set up required environment variables for API keys and device configurations.
- Ensure proper networking configuration for communication between the backend and frontend.

## API Endpoints

- Document the available API endpoints and their expected inputs/outputs.
- Example:
```json
GET /api/device-status
POST /api/send-command
```


## Contributing

Contributions to the Baile Flask Backend are welcome. Please follow the project's contributing guidelines for pull requests and code standards.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- Flask
- Python
- Requests Library
