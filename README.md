#  StudentPortal – Money Management & Job Search

A complete Flask web application for students to **track their finances** and **search for jobs/internships** — built as per college project guidelines.

---

##  Features

###  Money Management
- Add income and expense transactions with categories
- View income vs. expense breakdown with progress bars
- Filter and search transaction history
- Monthly summary table (surplus / deficit)
- Delete transactions with confirmation

###  Job Search Portal
- Browse 8+ pre-seeded job listings (internship, part-time, full-time)
- Search by title, company, or keyword
- Filter by job type and location
- View full job details
- Apply with a cover letter
- Track all your applications (pending / reviewed / accepted / rejected)
- Withdraw applications

###  Authentication
- User registration with password strength meter
- Secure login / logout
- Passwords hashed with Werkzeug

---

##  Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Backend   | Python 3, Flask                     |
| Frontend  | HTML5 semantic tags, Bootstrap 5    |
| JS        | JavaScript + jQuery 3.7             |
| Database  | SQLite (via Python `sqlite3`)        |
| Icons     | Bootstrap Icons                     |

---

## Project Structure

```
student_portal/
├── app.py                   # Flask application (routes, DB, auth)
├── requirements.txt         # Python dependencies
├── student_portal.db        # SQLite database (auto-created on first run)
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   └── js/
│       └── main.js          # jQuery validations & UI behaviour
└── templates/
    ├── base.html            # Base layout with navbar
    ├── index.html           # Landing page
    ├── dashboard.html       # Main dashboard
    ├── auth/
    │   ├── login.html
    │   └── register.html
    ├── money/
    │   ├── dashboard.html
    │   ├── add_transaction.html
    │   └── history.html
    └── jobs/
        ├── listings.html
        ├── job_detail.html
        ├── apply.html
        └── my_applications.html
```

---

##  Setup & Run Instructions

### Step 1 — Prerequisites
Make sure you have **Python 3.8+** installed.
```bash
python --version
```

### Step 2 — Clone / Download the project
```bash
git clone https://github.com/YOUR_USERNAME/student-portal.git
cd student-portal
```

Or just unzip the downloaded folder and open a terminal inside it.

### Step 3 — Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Run the application
```bash
python app.py
```

### Step 6 — Open in browser
```
http://127.0.0.1:5000
```

The SQLite database (`student_portal.db`) and all tables are created **automatically** on first run. Sample job listings are also seeded automatically.

---

##  Test the App

1. Go to `http://127.0.0.1:5000`
2. Click **Get Started Free** → Register a new account
3. Login with your credentials
4. Try adding income/expense transactions under **Money**
5. Browse and apply to jobs under **Jobs**
6. Check your application status under **My Applications**

---

##  Screenshots

> Add screenshots here after running the app locally.

---

## Deployment (Optional)

### Deploy to Render (free)
1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `python app.py`
6. Deploy!

---

##  Git Usage

```bash
git init
git add .
git commit -m "Initial commit: Student Portal with money management and job search"
git remote add origin https://github.com/YOUR_USERNAME/student-portal.git
git push -u origin main
```

---

##  Technologies Used

- **Flask 3.0** — Web framework
- **Werkzeug** — Password hashing
- **SQLite** — Lightweight database (no setup required)
- **Bootstrap 5.3** — Responsive UI components
- **Bootstrap Icons** — Icon library
- **jQuery 3.7** — DOM manipulation and form validation
- **Jinja2** — HTML templating (built into Flask)
