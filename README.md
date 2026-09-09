NovaHire ATS – Job Board & Mini Applicant Tracking System

A modern full-stack Job Board & Applicant Tracking System (ATS) built with Flask, featuring JWT authentication, recruiter and job seeker workflows, resume upload with ATS match scoring, and a responsive dark-themed UI.

Status: Completed (Backend + Frontend) | Deployment planned after submission.

Features

Authentication

Secure JWT-based login and registration
Role-based access (Recruiter & Job Seeker)
Password hashing with Flask-Bcrypt

Recruiter

Create job postings
View all posted jobs
Recruiter Dashboard with applicant management
Accept or Reject applications

Job Seeker

Browse available jobs
View detailed job descriptions
Apply for jobs
Upload PDF resume
Receive ATS Match Score based on resume skills

ATS Features

Resume PDF parsing
Skill extraction
Match score calculation
Resume skills preview

UI/UX

Responsive design
Dark Purple Glassmorphism theme
Modern landing page
Animated homepage statistics

Testing

Pytest test suite
Authentication tests
Job creation tests
Recruiter workflow tests
Database tests

Tech Stack

Category	Technology
Backend	Flask
Database	MySQL
ORM	SQLAlchemy
Authentication	Flask-JWT-Extended
Password Security	Flask-Bcrypt
Frontend	HTML, CSS, JavaScript
Styling	Bootstrap 5
Testing	Pytest
Version Control	Git & GitHub

Project Structure

CodeAlpha_JobBoard-ATS/
├── app/
│   ├── routes/
│   ├── templates/
│   └── static/
├── models/
├── tests/
├── uploads/
├── run.py
├── config.py
├── requirements.txt
├── Dockerfile
└── README.md

Installation

1. Clone the Repository
git clone https://github.com/fardeen02/CodeAlpha_JobBoard-ATS.git
cd CodeAlpha_JobBoard-ATS

2. Create Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure Database

Update your database credentials inside config.py.

5. Run the Application
python run.py

Open:

http://127.0.0.1:5000/

Running Tests

Execute the complete test suite:

pytest

The project includes automated tests for authentication, recruiter workflows, job management, and database functionality.

API Highlights

Endpoint	Description
POST /api/auth/register	Register user
POST /api/auth/login	Login
GET /api/jobs	List jobs
POST /api/jobs	Create job
POST /api/jobs/<id>/apply	Apply for job
POST /api/jobs/applications/<id>/resume	Upload resume
GET /api/recruiter/applicants	Recruiter dashboard

Future Improvements

Live deployment on Render
Docker containerization
Cloud resume storage (Cloudinary/AWS S3)
Email notifications
Advanced ATS keyword weighting
Interview scheduling

Author

Md Fardeen Alam

GitHub: https://github.com/fardeen02
LinkedIn: https://linkedin.com/in/fardeena14

Acknowledgements

Developed as part of the CodeAlpha Backend Development Internship while expanding it into a complete portfolio project with modern UI, recruiter workflows, and ATS functionality.