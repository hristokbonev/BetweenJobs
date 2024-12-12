# BetweenJobs

## Description
BetweenJobs is a platform designed to connect job seekers with potential employers. It provides a seamless experience for users to create profiles, search for jobs, and apply for positions. Employers can post job listings, search for candidates, and manage applications.

## Table of Contents
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)
- [Features](#features)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Customizing Styles](#customizing-styles)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation

### Prerequisites
- Node.js (v14.x or later)
- npm (v6.x or later)
- Python (v3.8 or later)
- PostgreSQL (v12 or later)

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/BetweenJobs.git
    cd BetweenJobs
    ```

2. Install backend dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Install frontend dependencies:
    ```bash
    npm install
    ```

4. Set up the database:
    ```bash
    createdb betweenjobs
    ```

5. Apply database migrations:
    ```bash
    python manage.py migrate
    ```

6. Start the development server:
    ```bash
    npm start
    ```

## Usage

### Running the Application
To start the application, run:
```bash
npm start
```
This will start both the backend and frontend servers. The application will be accessible at [http://localhost:3000](http://localhost:3000).

### Running Tests
To run the tests, use:
```bash
npm test
```

## Features
- **User Authentication**:
  - Sign up, login, logout
  - Password reset
- **User Profiles**:
  - Create and update profiles
  - Upload profile pictures
- **Job Listings**:
  - Search and filter job listings
  - Apply for jobs
- **Employer Dashboard**:
  - Post job listings
  - Manage applications
- **Notifications**:
  - Email notifications for job applications

## Configuration

### Environment Variables
Create a `.env` file in the root directory and add the following environment variables:
```
DATABASE_URL=<your-database-url>
SECRET_KEY=<your-secret-key>
EMAIL_HOST=<your-email-host>
EMAIL_PORT=<your-email-port>
EMAIL_USER=<your-email-username>
EMAIL_PASS=<your-email-password>
```

### Customizing Styles
To customize the styles, edit the SCSS files located in the `scss` directory. The main stylesheet is `style.scss`.

## API Documentation
The API documentation is available at [http://localhost:8000/api/docs](http://localhost:8000/api/docs). It provides detailed information about the available endpoints, request parameters, and response formats.

## Contributing
We welcome contributions from the community! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. Make your changes.
4. Commit your changes:
    ```bash
    git commit -m "Add your commit message here"
    ```
5. Push to the branch:
    ```bash
    git push origin feature/your-feature-name
    ```
6. Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- **Colorlib** for the template design.
- **IcoMoon** for the icon set.
- **Quill** for the rich text editor.

