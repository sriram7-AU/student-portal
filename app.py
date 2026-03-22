from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'student_portal_secret_key_2024'

DATABASE = 'student_portal.db'

# ─────────────────────────────────────────────
# Database Helpers
# ─────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            email    TEXT    UNIQUE NOT NULL,
            password TEXT    NOT NULL,
            role     TEXT    DEFAULT 'student'
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            type        TEXT    NOT NULL,
            category    TEXT    NOT NULL,
            amount      REAL    NOT NULL,
            description TEXT,
            date        TEXT    NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS jobs (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            title        TEXT NOT NULL,
            company      TEXT NOT NULL,
            location     TEXT NOT NULL,
            type         TEXT NOT NULL,
            salary       TEXT,
            description  TEXT,
            requirements TEXT,
            posted_date  TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS applications (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            job_id       INTEGER NOT NULL,
            cover_letter TEXT,
            status       TEXT DEFAULT 'pending',
            applied_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (job_id)  REFERENCES jobs(id),
            UNIQUE(user_id, job_id)
        );
    ''')

    # Seed sample jobs if table is empty
    cursor.execute("SELECT COUNT(*) as cnt FROM jobs")
    if cursor.fetchone()['cnt'] == 0:
        sample_jobs = [
            ('Frontend Developer Intern', 'TechCorp India', 'Hyderabad', 'internship',
             '₹15,000/month',
             'We are looking for a passionate Frontend Developer Intern to join our dynamic team. You will work on real-world projects using React and modern web technologies.',
             'HTML, CSS, JavaScript, React basics', datetime.now().strftime('%Y-%m-%d')),

            ('Data Analyst Part-Time', 'Analytics Hub', 'Remote', 'part-time',
             '₹20,000/month',
             'Join our analytics team to analyze business data and generate reports. Flexible working hours suitable for students.',
             'Python, Excel, SQL basics, Tableau', datetime.now().strftime('%Y-%m-%d')),

            ('Content Writer', 'EduBlog Media', 'Bangalore', 'part-time',
             '₹10,000/month',
             'Write engaging educational content for our blog. Work from home with flexible deadlines.',
             'Good English writing skills, SEO basics', datetime.now().strftime('%Y-%m-%d')),

            ('Software Developer Trainee', 'Infosys BPO', 'Pune', 'full-time',
             '₹3.5 LPA',
             'Full-time trainee position for fresh graduates. 6-month training program followed by placement in a project team.',
             'Java or Python, OOP concepts, DBMS', datetime.now().strftime('%Y-%m-%d')),

            ('UI/UX Design Intern', 'DesignStudio', 'Chennai', 'internship',
             '₹12,000/month',
             'Design intuitive user interfaces for mobile and web applications. Work with senior designers and developers.',
             'Figma, Adobe XD, basic design principles', datetime.now().strftime('%Y-%m-%date')),

            ('Customer Support Executive', 'CloudServe Tech', 'Remote', 'part-time',
             '₹8,000/month',
             'Handle customer queries and provide support via chat and email. Ideal for students looking for weekend/evening work.',
             'Good communication, patience, MS Office', datetime.now().strftime('%Y-%m-%d')),

            ('Machine Learning Intern', 'AI Solutions Pvt Ltd', 'Hyderabad', 'internship',
             '₹18,000/month',
             'Work on ML model development and deployment projects. Mentorship from senior ML engineers.',
             'Python, NumPy, Pandas, basic ML knowledge', datetime.now().strftime('%Y-%m-%d')),

            ('Full Stack Developer', 'StartupNest', 'Bangalore', 'full-time',
             '₹5 LPA',
             'Build and maintain web applications using MERN stack. Startup culture with growth opportunities.',
             'Node.js, React, MongoDB, REST APIs', datetime.now().strftime('%Y-%m-%d')),
        ]
        cursor.executemany('''
            INSERT INTO jobs (title, company, location, type, salary, description, requirements, posted_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_jobs)

    conn.commit()
    conn.close()

# ─────────────────────────────────────────────
# Auth Decorator
# ─────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ─────────────────────────────────────────────
# Auth Routes
# ─────────────────────────────────────────────

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        if not all([name, email, password, confirm]):
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('auth/register.html')

        conn = get_db()
        existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            conn.close()
            flash('Email already registered.', 'danger')
            return render_template('auth/register.html')

        hashed = generate_password_hash(password)
        conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed))
        conn.commit()
        conn.close()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id']   = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ─────────────────────────────────────────────
# Main Dashboard
# ─────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    uid  = session['user_id']

    # Money summary
    income   = conn.execute("SELECT COALESCE(SUM(amount),0) as total FROM transactions WHERE user_id=? AND type='income'", (uid,)).fetchone()['total']
    expenses = conn.execute("SELECT COALESCE(SUM(amount),0) as total FROM transactions WHERE user_id=? AND type='expense'", (uid,)).fetchone()['total']
    balance  = income - expenses

    recent_txns = conn.execute(
        "SELECT * FROM transactions WHERE user_id=? ORDER BY date DESC, id DESC LIMIT 5",
        (uid,)
    ).fetchall()

    # Jobs summary
    total_jobs  = conn.execute("SELECT COUNT(*) as cnt FROM jobs").fetchone()['cnt']
    my_apps     = conn.execute("SELECT COUNT(*) as cnt FROM applications WHERE user_id=?", (uid,)).fetchone()['cnt']
    recent_jobs = conn.execute("SELECT * FROM jobs ORDER BY id DESC LIMIT 3").fetchall()

    conn.close()
    return render_template('dashboard.html',
                           income=income, expenses=expenses, balance=balance,
                           recent_txns=recent_txns, total_jobs=total_jobs,
                           my_apps=my_apps, recent_jobs=recent_jobs)

# ─────────────────────────────────────────────
# Money Management Routes
# ─────────────────────────────────────────────

@app.route('/money')
@login_required
def money_dashboard():
    conn = get_db()
    uid  = session['user_id']

    income   = conn.execute("SELECT COALESCE(SUM(amount),0) as total FROM transactions WHERE user_id=? AND type='income'", (uid,)).fetchone()['total']
    expenses = conn.execute("SELECT COALESCE(SUM(amount),0) as total FROM transactions WHERE user_id=? AND type='expense'", (uid,)).fetchone()['total']
    balance  = income - expenses

    # Category breakdown for expenses
    expense_cats = conn.execute(
        "SELECT category, SUM(amount) as total FROM transactions WHERE user_id=? AND type='expense' GROUP BY category ORDER BY total DESC",
        (uid,)
    ).fetchall()

    # Category breakdown for income
    income_cats = conn.execute(
        "SELECT category, SUM(amount) as total FROM transactions WHERE user_id=? AND type='income' GROUP BY category ORDER BY total DESC",
        (uid,)
    ).fetchall()

    # Monthly summary (last 6 months)
    monthly = conn.execute('''
        SELECT strftime('%Y-%m', date) as month,
               SUM(CASE WHEN type='income'  THEN amount ELSE 0 END) as income,
               SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) as expenses
        FROM transactions WHERE user_id=?
        GROUP BY month ORDER BY month DESC LIMIT 6
    ''', (uid,)).fetchall()

    conn.close()
    return render_template('money/dashboard.html',
                           income=income, expenses=expenses, balance=balance,
                           expense_cats=expense_cats, income_cats=income_cats,
                           monthly=monthly)


@app.route('/money/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        txn_type    = request.form.get('type')
        category    = request.form.get('category', '').strip()
        amount      = request.form.get('amount', '').strip()
        description = request.form.get('description', '').strip()
        date        = request.form.get('date', '').strip()

        if not all([txn_type, category, amount, date]):
            flash('Please fill all required fields.', 'danger')
            return render_template('money/add_transaction.html')

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash('Enter a valid positive amount.', 'danger')
            return render_template('money/add_transaction.html')

        conn = get_db()
        conn.execute(
            'INSERT INTO transactions (user_id, type, category, amount, description, date) VALUES (?, ?, ?, ?, ?, ?)',
            (session['user_id'], txn_type, category, amount, description, date)
        )
        conn.commit()
        conn.close()

        flash(f'{"Income" if txn_type == "income" else "Expense"} of ₹{amount:.2f} added successfully!', 'success')
        return redirect(url_for('money_dashboard'))

    return render_template('money/add_transaction.html', today=datetime.now().strftime('%Y-%m-%d'))


@app.route('/money/history')
@login_required
def transaction_history():
    conn = get_db()
    uid  = session['user_id']

    filter_type = request.args.get('type', 'all')
    filter_cat  = request.args.get('category', '')
    search      = request.args.get('search', '')

    query  = "SELECT * FROM transactions WHERE user_id=?"
    params = [uid]

    if filter_type in ('income', 'expense'):
        query  += " AND type=?"
        params.append(filter_type)

    if filter_cat:
        query  += " AND category=?"
        params.append(filter_cat)

    if search:
        query  += " AND (description LIKE ? OR category LIKE ?)"
        params += [f'%{search}%', f'%{search}%']

    query += " ORDER BY date DESC, id DESC"

    transactions = conn.execute(query, params).fetchall()
    categories   = conn.execute(
        "SELECT DISTINCT category FROM transactions WHERE user_id=? ORDER BY category",
        (uid,)
    ).fetchall()
    conn.close()

    return render_template('money/history.html',
                           transactions=transactions, categories=categories,
                           filter_type=filter_type, filter_cat=filter_cat, search=search)


@app.route('/money/delete/<int:txn_id>', methods=['POST'])
@login_required
def delete_transaction(txn_id):
    conn = get_db()
    txn  = conn.execute('SELECT * FROM transactions WHERE id=? AND user_id=?',
                        (txn_id, session['user_id'])).fetchone()
    if txn:
        conn.execute('DELETE FROM transactions WHERE id=?', (txn_id,))
        conn.commit()
        flash('Transaction deleted.', 'success')
    else:
        flash('Transaction not found.', 'danger')
    conn.close()
    return redirect(url_for('transaction_history'))

# ─────────────────────────────────────────────
# Job Search Routes
# ─────────────────────────────────────────────

@app.route('/jobs')
@login_required
def job_listings():
    conn = get_db()
    uid  = session['user_id']

    search       = request.args.get('search', '')
    filter_type  = request.args.get('type', '')
    filter_loc   = request.args.get('location', '')

    query  = "SELECT * FROM jobs WHERE 1=1"
    params = []

    if search:
        query  += " AND (title LIKE ? OR company LIKE ? OR description LIKE ?)"
        params += [f'%{search}%', f'%{search}%', f'%{search}%']

    if filter_type:
        query  += " AND type=?"
        params.append(filter_type)

    if filter_loc:
        query  += " AND location LIKE ?"
        params.append(f'%{filter_loc}%')

    query += " ORDER BY id DESC"
    jobs = conn.execute(query, params).fetchall()

    # Check which jobs the user already applied to
    applied_ids = set(
        row['job_id'] for row in
        conn.execute("SELECT job_id FROM applications WHERE user_id=?", (uid,)).fetchall()
    )

    locations = conn.execute("SELECT DISTINCT location FROM jobs ORDER BY location").fetchall()
    conn.close()

    return render_template('jobs/listings.html',
                           jobs=jobs, applied_ids=applied_ids,
                           locations=locations, search=search,
                           filter_type=filter_type, filter_loc=filter_loc)


@app.route('/jobs/<int:job_id>')
@login_required
def job_detail(job_id):
    conn = get_db()
    uid  = session['user_id']
    job  = conn.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
    if not job:
        flash('Job not found.', 'danger')
        conn.close()
        return redirect(url_for('job_listings'))

    already_applied = conn.execute(
        'SELECT id FROM applications WHERE user_id=? AND job_id=?', (uid, job_id)
    ).fetchone()
    conn.close()

    return render_template('jobs/job_detail.html', job=job, already_applied=already_applied)


@app.route('/jobs/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required
def apply_job(job_id):
    conn = get_db()
    uid  = session['user_id']
    job  = conn.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()

    if not job:
        flash('Job not found.', 'danger')
        conn.close()
        return redirect(url_for('job_listings'))

    already_applied = conn.execute(
        'SELECT id FROM applications WHERE user_id=? AND job_id=?', (uid, job_id)
    ).fetchone()

    if already_applied:
        flash('You have already applied for this job.', 'warning')
        conn.close()
        return redirect(url_for('my_applications'))

    if request.method == 'POST':
        cover_letter = request.form.get('cover_letter', '').strip()
        if not cover_letter:
            flash('Cover letter is required.', 'danger')
            conn.close()
            return render_template('jobs/apply.html', job=job)

        try:
            conn.execute(
                'INSERT INTO applications (user_id, job_id, cover_letter, applied_date) VALUES (?, ?, ?, ?)',
                (uid, job_id, cover_letter, datetime.now().strftime('%Y-%m-%d'))
            )
            conn.commit()
            flash(f'Successfully applied for "{job["title"]}" at {job["company"]}!', 'success')
            conn.close()
            return redirect(url_for('my_applications'))
        except Exception as e:
            conn.close()
            flash('An error occurred. Please try again.', 'danger')

    conn.close()
    return render_template('jobs/apply.html', job=job)


@app.route('/jobs/applications')
@login_required
def my_applications():
    conn = get_db()
    uid  = session['user_id']

    apps = conn.execute('''
        SELECT a.*, j.title, j.company, j.location, j.type, j.salary
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        WHERE a.user_id = ?
        ORDER BY a.applied_date DESC
    ''', (uid,)).fetchall()

    status_counts = {
        'pending':  0,
        'reviewed': 0,
        'accepted': 0,
        'rejected': 0
    }
    for app in apps:
        s = app['status']
        if s in status_counts:
            status_counts[s] += 1

    conn.close()
    return render_template('jobs/my_applications.html', apps=apps, status_counts=status_counts)


@app.route('/jobs/withdraw/<int:app_id>', methods=['POST'])
@login_required
def withdraw_application(app_id):
    conn = get_db()
    app_row = conn.execute(
        'SELECT * FROM applications WHERE id=? AND user_id=?',
        (app_id, session['user_id'])
    ).fetchone()
    if app_row:
        conn.execute('DELETE FROM applications WHERE id=?', (app_id,))
        conn.commit()
        flash('Application withdrawn successfully.', 'success')
    else:
        flash('Application not found.', 'danger')
    conn.close()
    return redirect(url_for('my_applications'))

# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
