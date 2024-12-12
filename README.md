BetweenJobs

Description

BetweenJobs is a platform designed to connect job seekers with potential employers. It provides a seamless experience for users to create profiles, search for jobs, and apply for positions. Employers can post job listings, search for candidates, and manage applications.

Table of Contents

Installation

Prerequisites

Steps

Usage

Running the Application

Running Tests

Features

Configuration

Environment Variables

Customizing Styles

API Documentation

Contributing

License

Acknowledgments

Installation

Prerequisites

Node.js (v14.x or later)

npm (v6.x or later)

Python (v3.8 or later)

PostgreSQL (v12 or later)

Steps

Clone the repository:

git clone https://github.com/yourusername/BetweenJobs.git
cd BetweenJobs

Install backend dependencies:

pip install -r requirements.txt

Install frontend dependencies:

npm install

Set up the database:

createdb betweenjobs

Apply database migrations:

python manage.py migrate

Start the development server:

npm start

Usage

Running the Application

To start the application, run:

npm start

This will start both the backend and frontend servers. The application will be accessible at http://localhost:3000.

Running Tests

To run the tests, use:

npm test

Features

User Authentication:

Sign up, login, logout

Password reset

User Profiles:

Create and update profiles

Upload profile pictures

Job Listings:

Search and filter job listings

Apply for jobs

Employer Dashboard:

Post job listings

Manage applications

Notifications:

Email notifications for job applications

Configuration

Environment Variables

Create a .env file in the root directory and add the following environment variables:

DATABASE_URL=<your-database-url>
SECRET_KEY=<your-secret-key>
EMAIL_HOST=<your-email-host>
EMAIL_PORT=<your-email-port>
EMAIL_USER=<your-email-username>
EMAIL_PASS=<your-email-password>

Customizing Styles

To customize the styles, edit the SCSS files located in the scss directory. The main stylesheet is style.scss.

API Documentation

The API documentation is available at http://localhost:8000/api/docs. It provides detailed information about the available endpoints, request parameters, and response formats.

Contributing

We welcome contributions from the community! To contribute, follow these steps:

Fork the repository.

Create a new branch:

git checkout -b feature/your-feature-name

Make your changes.

Commit your changes:

git commit -m "Add your commit message here"

Push to the branch:

git push origin feature/your-feature-name

Open a pull request.

License

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments

Colorlib for the template design.

IcoMoon for the icon set.

Quill for the rich text editor.

