# Placement Portal Application (PPA) - V2

A full-stack Placement Portal Application that connects an institute placement cell, companies, and students.

The application provides role-based access for:

* Admin
* Company
* Student

It supports company and placement-drive approvals, student applications, interview scheduling, placement tracking, notifications, Redis caching, and asynchronous background jobs using Celery.

---

## 1. Technology Stack

### Backend

* Flask
* Flask-SQLAlchemy
* JWT Authentication
* SQLite
* Celery
* Redis
* Werkzeug

### Frontend

* VueJS
* Vue Router
* Axios
* Bootstrap

### Background Processing

* Celery
* Redis
* Celery Beat

---

# 2. Project Structure

```text
placement-portal/
│
├── backend/
│   ├── app/
│   ├── uploads/
│   ├── instance/
│   ├── venv/
│   ├── create_db.py
│   ├── celery_worker.py
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
│
└── frontend/
    ├── src/
    ├── public/
    ├── package.json
    └── ...
```

---

# 3. Prerequisites

Make sure the following are installed:

* Python 3
* Node.js and npm
* Docker Desktop
* Git

Docker is used to run Redis locally.

---

# 4. Backend Setup

Open a terminal and navigate to the backend:

```bash
cd backend
```

Create and activate the virtual environment if it does not already exist.

### Windows Git Bash

```bash
source venv/Scripts/activate
```

You should see:

```text
(venv)
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

---

# 5. Create the Database

The database is created programmatically.

Run:

```bash
python create_db.py
```

This creates the required SQLite database and tables and creates the pre-existing Admin account.

No manual database creation using DB Browser is required.

---

# 6. Start Redis

Make sure Docker Desktop is running.

Run:

```bash
docker run -d --name placement-redis -p 6379:6379 redis:7
```

Check that Redis is running:

```bash
docker ps
```

You should see:

```text
placement-redis
```

You can also test Redis:

```bash
docker exec -it placement-redis redis-cli ping
```

Expected output:

```text
PONG
```

### If the container already exists

You may get an error saying the container name already exists.

In that case, simply start it:

```bash
docker start placement-redis
```

Then verify:

```bash
docker ps
```

---

# 7. Start the Flask Backend

Open a backend terminal:

```bash
cd backend
source venv/Scripts/activate
```

Run:

```bash
python run.py
```

The Flask API will run on:

```text
http://127.0.0.1:5000
```

Keep this terminal running.

---

# 8. Start Celery Worker

Open a **new terminal**.

Navigate to backend:

```bash
cd backend
source venv/Scripts/activate
```

Start the Celery worker:

```bash
celery -A celery_worker.celery worker --pool=solo --loglevel=info
```

A successful worker will show:

```text
Connected to redis://localhost:6379/0
```

and:

```text
celery@<computer-name> ready.
```

Keep this terminal running.

---

# 9. Start Celery Beat

Open another **new terminal**.

Navigate to backend:

```bash
cd backend
source venv/Scripts/activate
```

Run:

```bash
celery -A celery_worker.celery beat --loglevel=info
```

Celery Beat is responsible for triggering scheduled jobs automatically.

Keep this terminal running.

---

# 10. Start the Vue Frontend

Open another terminal.

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies if required:

```bash
npm install
```

Start the Vue development server:

```bash
npm run dev
```

Open the URL shown by Vite in the terminal, usually:

```text
http://localhost:5173
```

---

# 11. Required Running Terminals

For the complete application, keep these services running:

### Terminal 1 - Redis

Docker container:

```bash
docker run -d --name placement-redis -p 6379:6379 redis:7
```

### Terminal 2 - Flask Backend

```bash
cd backend
source venv/Scripts/activate
python run.py
```

### Terminal 3 - Celery Worker

```bash
cd backend
source venv/Scripts/activate
celery -A celery_worker.celery worker --pool=solo --loglevel=info
```

### Terminal 4 - Celery Beat

```bash
cd backend
source venv/Scripts/activate
celery -A celery_worker.celery beat --loglevel=info
```

### Terminal 5 - Vue Frontend

```bash
cd frontend
npm run dev
```

---

# 12. Background Jobs

The application uses Celery and Redis for asynchronous and scheduled jobs.

## A. Daily Deadline Reminder

The application checks for approved placement drives whose application deadline is within the configured reminder window.

The reminder:

* Creates a notification in the student portal
* Sends an email reminder to the student

Celery Beat automatically triggers the task according to the configured schedule.

Task:

```text
app.tasks.reminder_tasks.send_deadline_reminders
```

---

# 13. Manually Run the Deadline Reminder

For testing, the reminder task can be triggered manually instead of waiting for Celery Beat.

Make sure:

* Redis is running
* Celery worker is running
* A student has a valid email
* An approved placement drive has an application deadline within the reminder window

Open another backend terminal:

```bash
cd backend
source venv/Scripts/activate
python
```

Then run:

```python
from app.tasks.reminder_tasks import send_deadline_reminders

result = send_deadline_reminders.delay()

print(result.get(timeout=60))
```

A successful result looks similar to:

```text
{
    'status': 'completed',
    'drives_found': 1,
    'notifications_created': 1,
    'emails_sent': 1,
    'emails_failed': 0
}
```

The student should then receive:

1. A notification inside the Student Portal
2. An email reminder

---

# 14. Monthly Activity Report

The monthly activity report is generated automatically using Celery Beat.

Task:

```text
app.tasks.report_tasks.generate_monthly_report
```

The report:

* Generates the monthly placement activity report
* Creates the report in HTML
* Includes placement activity statistics
* Sends the report to the Admin through email

The scheduled job runs on the configured monthly schedule.

---

# 15. Manually Test the Monthly Report

For testing, the monthly report task can be triggered manually.

Open a backend terminal:

```bash
cd backend
source venv/Scripts/activate
python
```

Then import the task:

```python
from app.tasks.report_tasks import generate_monthly_report
```

Trigger it:

```python
result = generate_monthly_report.delay()
```

Check the result:

```python
print(result.get(timeout=120))
```

The Celery worker should show that the task was received and completed.

The Admin email inbox should receive the generated monthly report.

---

# 16. Student Application CSV Export

Students can export their placement application history as a CSV file.

The export is an asynchronous Celery task.

Task:

```text
app.tasks.export_tasks.export_student_applications
```

The CSV contains information such as:

```text
Student ID
Company Name
Drive Title
Application Status
Application Date
```

The export is triggered from the Student Portal.

The CSV generation happens in the background using:

```text
Vue
 ↓
Flask API
 ↓
Celery
 ↓
Redis
 ↓
CSV generation
```

After completion, the student receives an alert/notification.

---

# 17. Testing CSV Export Manually

If required for testing, the Celery task can also be triggered manually.

Open Python:

```bash
cd backend
source venv/Scripts/activate
python
```

Import the task:

```python
from app.tasks.export_tasks import export_student_applications
```

Pass the required student ID according to the task definition:

```python
result = export_student_applications.delay(<student_id>)
```

Then:

```python
print(result.get(timeout=120))
```

Check the configured uploads/export directory for the generated CSV.

---

# 18. Redis Cache

Redis is also used for caching frequently accessed data.

For example, approved placement drives are cached to reduce unnecessary database queries.

You can inspect Redis using:

```bash
docker exec -it placement-redis redis-cli
```

Select the configured Redis database:

```text
SELECT 1
```

View cache keys:

```text
KEYS *
```

Example:

```text
flask_cache_approved_drives
```

Cache expiry is configured so stale data is automatically removed.

---

# 19. Authentication and Roles

The application has three roles:

```text
Admin
Company
Student
```

### Admin

The Admin is pre-created programmatically and cannot register.

Admin can:

* Manage companies
* Approve/reject companies
* Blacklist/deactivate companies
* Manage students
* Blacklist/deactivate students
* Approve/reject placement drives
* View applications
* Search students and companies
* View placement statistics

### Company

Companies can:

* Register
* Manage company profile
* Create placement drives after approval
* View applicants
* Shortlist students
* Update application status
* Schedule interviews
* Update final selection results

### Student

Students can:

* Register
* Login
* Edit profile
* Upload resume
* Search placement drives
* Check eligibility
* Apply for drives
* Track applications
* View interviews
* View placement history
* Export application history
* Receive notifications

---

# 20. Important Application Rules

The application implements several validation rules.

### Duplicate applications

A student cannot apply multiple times to the same placement drive.

This is enforced using a database-level unique constraint.

### Eligibility

Students are checked against the placement drive's eligibility requirements before applying.

Eligibility can include:

* Branch
* CGPA
* Graduation year

### Placement history

Application and selection records are retained so students can view their placement history.

---

# 21. Troubleshooting

## Redis connection refused

If you see:

```text
Error 10061 connecting to localhost:6379
```

Redis is not running.

Check:

```bash
docker ps
```

If `placement-redis` exists but is stopped:

```bash
docker start placement-redis
```

Test:

```bash
docker exec -it placement-redis redis-cli ping
```

Expected:

```text
PONG
```

Then restart the Celery worker.

---

## Celery task not appearing

Check that the Celery worker lists the task:

```text
app.tasks.reminder_tasks.send_deadline_reminders
```

and:

```text
app.tasks.export_tasks.export_student_applications
```

If a task is missing, restart the worker after checking the task import configuration.

---

## Email reminder not received

Check the Celery worker logs.

The reminder task returns:

```text
emails_sent
emails_failed
```

If:

```text
emails_failed: 1
```

check the displayed email error and verify the configured email credentials/settings.

---

# 22. Complete Startup Sequence

For a fresh demo, use this order:

### Step 1

Start Docker Desktop.

### Step 2

Start Redis:

```bash
docker start placement-redis
```

or, if the container does not exist:

```bash
docker run -d --name placement-redis -p 6379:6379 redis:7
```

### Step 3

Start Flask:

```bash
cd backend
source venv/Scripts/activate
python run.py
```

### Step 4

Start Celery Worker:

```bash
cd backend
source venv/Scripts/activate
celery -A celery_worker.celery worker --pool=solo --loglevel=info
```

### Step 5

Start Celery Beat:

```bash
cd backend
source venv/Scripts/activate
celery -A celery_worker.celery beat --loglevel=info
```

### Step 6

Start Vue:

```bash
cd frontend
npm run dev
```

### Step 7

Open the frontend URL displayed by Vite.

---

# 23. Project Features Summary

The Placement Portal Application provides:

* Role-based authentication
* Admin management
* Company registration and approval
* Placement-drive management
* Student registration
* Eligibility validation
* Placement applications
* Duplicate application prevention
* Application status tracking
* Interview scheduling
* Final selection
* Placement history
* Resume upload
* Student notifications
* Email deadline reminders
* Monthly activity reports
* CSV application export
* Redis caching
* Celery asynchronous processing
* Celery Beat scheduled jobs
* SQLite database
* Responsive Bootstrap-based UI

---


The application is designed to run completely on a local machine using SQLite, Redis, Celery, Flask, and VueJS.
