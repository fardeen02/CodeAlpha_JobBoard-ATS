**NovaHire ATS – Job Board & Mini Applicant Tracking System**

_A modern full-stack Job Board & Applicant Tracking System (ATS) built with Flask, featuring JWT authentication, recruiter and job seeker workflows, resume upload with ATS match scoring, and a responsive dark-themed UI._

**Status: Completed (Backend + Frontend) | _Deployment planned after submission._**

**Screenshots**

1. _Home Page_
   <img width="1366" height="638" alt="Screenshot (462)" src="https://github.com/user-attachments/assets/c02f615a-3eec-4ea6-8268-bdde063a4bb2" />

2. _Login Page_
    <img width="1366" height="641" alt="Screenshot (459)" src="https://github.com/user-attachments/assets/ad3f2b83-baac-4768-ba9c-9984f0a8e929" />

3. _Job Explore_
 <img width="1366" height="637" alt="Screenshot (464)" src="https://github.com/user-attachments/assets/3bbd5efc-48a5-4ef7-aa86-d6fa2dc475c2" />

4. _Job Detail and Apply_
  <img width="1366" height="638" alt="Screenshot (465)" src="https://github.com/user-attachments/assets/a1cec077-ea69-4071-b794-005642500f57" />

5. _Recruiter Dashboard_
<img width="1366" height="642" alt="Screenshot (463)" src="https://github.com/user-attachments/assets/f6ac9ced-b7ba-4508-95bb-7d479ab8488c" />

**Features**

_**Authentication**_

- Secure JWT-based login and registration
- Role-based access (Recruiter & Job Seeker)
- Password hashing with Flask-Bcrypt

_**Recruiter**_

- Create job postings
- View all posted jobs
- Recruiter Dashboard with applicant management
- Accept or Reject applications

_**Job Seeker**_

- Browse available jobs
- View detailed job descriptions
- Apply for jobs
- Upload PDF resume
- Receive ATS Match Score based on resume skills

_**ATS Features**_

- Resume PDF parsing
- Skill extraction
- Match score calculation
- Resume skills preview

_**UI/UX**_

- Responsive design
- Dark Purple Glassmorphism theme
- Modern landing page
- Animated homepage statistics

_**Testing**_

- Pytest test suite
- Authentication tests
- Job creation tests
- Recruiter workflow tests
- Database tests

**Tech Stack**

- Category	Technology
- Backend	Flask
- Database	MySQL
- ORM	SQLAlchemy
- Authentication	Flask-JWT-Extended
- Password Security	Flask-Bcrypt
- Frontend	HTML, CSS, JavaScript
- Styling	Bootstrap 5
- Testing	Pytest
- Version Control	Git & GitHub

**Project Structure**

CodeAlpha_JobBoard-ATS/
- app/
     - routes/
     - templates/
     - static/
- models/
- tests/
- uploads/
- run.py
- config.py
- requirements.txt
- Dockerfile
- README.md

**Installation**

1. Clone the Repository
git clone https://github.com/fardeen02/CodeAlpha_JobBoard-ATS.git
cd CodeAlpha_JobBoard-ATS

2. Create Virtual Environment

**Windows**

- python -m venv venv
- venv\Scripts\activate

3. Install Dependencies
- pip install -r requirements.txt

4. Configure Database
- Update your database credentials inside config.py.

5. Run the Application
- python run.py
- Open: http://127.0.0.1:5000/
 Running Tests
- Execute the complete test suite:
- pytest
The project includes automated tests for authentication, recruiter workflows, job management, and database functionality.

_**API Highlights**_

**Endpoint -	Description**
- POST /api/auth/register	- Register user

- POST /api/auth/login -	Login
- GET /api/jobs - List jobs
- POST /api/jobs - Create job
- POST /api/jobs/<id>/apply - 	Apply for job
- POST /api/jobs/applications/<id>/resume	 - Upload resume
- GET /api/recruiter/applicants	- Recruiter dashboard

_**Future Improvements**_

-	Live deployment on Render
-	Docker containerization
-	Cloud resume storage (Cloudinary/AWS S3)
-	Email notifications
-	Advanced ATS keyword weighting
-	Interview scheduling

_**Author**_

**Md Fardeen Alam**

**GitHub:** https://github.com/fardeen02

**LinkedIn:** https://linkedin.com/in/fardeena14

_**Acknowledgements**_

- Developed as part of the CodeAlpha Backend Development Internship while expanding it into a complete portfolio project with modern UI, recruiter workflows, and ATS functionality.
