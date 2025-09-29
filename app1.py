import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, StackingRegressor, AdaBoostRegressor
from sklearn.tree import ExtraTreeRegressor
from sklearn.metrics import r2_score
import psycopg2

# -------------------------------
# DATABASE SETUP (PostgreSQL)
# -------------------------------
DATABASE_URL = "postgresql://stressdb_y8l1_user:nkUESsYvS6ESRcUCquMOTazBZjCa6GQ4@dpg-d3ae75fdiees73d6lkhg-a/stressdb_y8l1"

# Internal URL does not require SSL
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
# -------------------------------
# FLASK APP SETUP
# -------------------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# -------------------------------
# ADMIN CREDENTIALS
# -------------------------------
admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

# -------------------------------
# GLOBAL VARIABLES FOR MODEL
# -------------------------------
x_train = x_test = y_train = y_test = None

# -------------------------------
# ROUTES
# -------------------------------
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/home')
def home():
    return render_template("userhome.html")

# -------------------------------
# ADMIN LOGIN & PANEL
# -------------------------------
# -------------------------------
# ADMIN LOGIN
# -------------------------------
# -------------------------------
# ADMIN LOGIN
# -------------------------------
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """
    Admin login route.
    Admin credentials are defined by environment variables (or default values).
    """
    msg = ''
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()
        
        if email == admin_email and password == admin_password:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            msg = '❌ Invalid email or password!'
    
    return render_template('admin_login.html', msg=msg)


# -------------------------------
# ADMIN PANEL
# -------------------------------
@app.route('/admin_panel')
def admin_panel():
    """
    Admin dashboard.
    Admin can view allowed emails and registered users.
    """
    if not session.get('admin_logged_in'):
        flash('⚠️ Please log in as admin to access the admin panel.', 'danger')
        return redirect(url_for('admin_login'))

    try:
        cur.execute("SELECT * FROM allowed_emails")
        allowed_emails = cur.fetchall()

        cur.execute("SELECT Id, Name, Email FROM users")
        registered_users = cur.fetchall()
    except Exception as e:
        print("Database error:", e)
        allowed_emails = []
        registered_users = []

    return render_template('admin_panel.html', allowed_emails=allowed_emails, registered_users=registered_users)


# -------------------------------
# ADMIN LOGOUT
# -------------------------------
@app.route('/admin_logout')
def admin_logout():
    """
    Logs out admin and clears session.
    """
    session.pop('admin_logged_in', None)
    flash("🚪 Logged out successfully.", "info")
    return redirect(url_for('admin_login'))


# -------------------------------
# ADD ALLOWED EMAIL (ADMIN ONLY)
# -------------------------------
@app.route('/admin/add_email', methods=['POST'])
def add_email():
    """
    Admin can add any email to allowed_emails table.
    No restrictions; duplicates are ignored via ON CONFLICT.
    """
    email = request.form['email'].strip().lower()
    try:
        cur.execute(
            "INSERT INTO allowed_emails (email) VALUES (%s) ON CONFLICT (email) DO NOTHING",
            (email,)
        )
        conn.commit()
        flash("✅ Email added successfully", "success")
    except Exception as e:
        conn.rollback()
        flash(f"❌ Failed to add email: {str(e)}", "danger")
    
    return redirect(url_for('admin_panel'))


# -------------------------------
# DELETE ALLOWED EMAIL (ADMIN ONLY)
# -------------------------------
@app.route('/admin/delete_email/<int:id>')
def delete_email(id):
    """
    Admin can delete any email from allowed_emails table.
    """
    try:
        cur.execute("DELETE FROM allowed_emails WHERE id=%s", (id,))
        conn.commit()
        flash("✅ Allowed email deleted successfully", "success")
    except Exception as e:
        conn.rollback()
        flash(f"❌ Failed to delete allowed email: {str(e)}", "danger")
    
    return redirect(url_for('admin_panel'))


# -------------------------------
# DELETE REGISTERED USER (ADMIN ONLY)
# -------------------------------
@app.route('/admin/delete_user/<int:id>')
def delete_user(id):
    """
    Admin can delete any registered user.
    """
    try:
        cur.execute("DELETE FROM users WHERE Id=%s", (id,))
        conn.commit()
        flash("✅ Registered user deleted successfully", "success")
    except Exception as e:
        conn.rollback()
        flash(f"❌ Failed to delete user: {str(e)}", "danger")
    
    return redirect(url_for('admin_panel'))



# -------------------------------
# USER LOGIN & REGISTRATION
# -------------------------------
@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    User login route.
    Authenticates users based on email and password stored in the database.
    """
    if request.method == 'POST':
        # -------------------------
        # 1️⃣ Get form inputs and normalize
        # -------------------------
        useremail = request.form['useremail'].strip().lower()
        userpassword = request.form['userpassword'].strip()

        # -------------------------
        # 2️⃣ Query database for user
        # -------------------------
        cur.execute(
            "SELECT * FROM users WHERE Email=%s AND Password=%s",
            (useremail, userpassword)
        )
        user = cur.fetchone()  # fetchone() returns a single row or None

        # -------------------------
        # 3️⃣ Check if user exists
        # -------------------------
        if not user:
            flash("❌ Invalid email or password. Please try again.", "danger")
            return redirect(url_for('login'))

        # -------------------------
        # 4️⃣ Set session variables and redirect to user home
        # -------------------------
        session['email'] = useremail
        session['name'] = user[1]  # Name column
        session['pno'] = str(user[5])  # Mobile number column
        flash(f"✅ Welcome, {user[1]}!", "success")
        return render_template("userhome.html", myname=session['name'])

    # Render login page for GET requests
    return render_template('login.html')



@app.route('/registration', methods=["POST", "GET"])
def registration():
    # Allowed email domains for user registration
    allowed_domains = ['@techcorp.com', '@itcompany.com', '@cybertech.org', '@datasci.in', '@qaeng.com']

    if request.method == 'POST':
        # Get form inputs
        username = request.form['username'].strip()
        useremail = request.form['useremail'].strip().lower()
        userpassword = request.form['userpassword'].strip()
        conpassword = request.form['conpassword'].strip()
        Age = request.form['Age'].strip()
        contact = request.form['contact'].strip()

        # -------------------------
        # 1️⃣ Check if email domain is allowed
        # -------------------------
        if not any(useremail.endswith(domain) for domain in allowed_domains):
            flash("❌ Registration allowed only for IT employees with approved email domains.", "danger")
            return redirect("/registration")

        # -------------------------
        # 2️⃣ Check password confirmation
        # -------------------------
        if userpassword != conpassword:
            flash("⚠️ Passwords do not match.", "warning")
            return redirect("/registration")

        # -------------------------
        # 3️⃣ Check if user already exists
        # -------------------------
        cursor.execute("SELECT * FROM users WHERE Email=%s", (useremail,))
        existing = cursor.fetchone()
        if existing:
            flash("⚠️ User already registered. Try logging in.", "warning")
            return redirect("/registration")

        # -------------------------
        # 4️⃣ Register new user
        # -------------------------
        try:
            cursor.execute(
                "INSERT INTO users(Name, Email, Password, Age, Mob) VALUES (%s, %s, %s, %s, %s)",
                (username, useremail, userpassword, Age, contact)
            )
            conn.commit()
            flash("✅ Registered successfully", "success")
            return redirect("/login")
        except Exception as e:
            conn.rollback()
            flash(f"❌ Registration failed: {str(e)}", "danger")
            return redirect("/registration")

    return render_template('registration.html')


        try:
            cursor.execute(
                "INSERT INTO users(Name, Email, Password, Age, Mob) VALUES (%s, %s, %s, %s, %s)",
                (username, useremail, userpassword, Age, contact)
            )
            conn.commit()
            flash("✅ Registered successfully", "success")
            return redirect("/login")
        except Exception as e:
            conn.rollback()
            flash(f"❌ Registration failed: {str(e)}", "danger")
            return redirect("/registration")

    return render_template('registration.html')


# -------------------------------
# DATASET LOAD & PREPROCESS
# -------------------------------
DATASET_URL = "https://YOUR_RENDER_FILE_URL/stress_detection_IT_professionals_dataset.csv"

@app.route('/viewdata')
def viewdata():
    df = pd.read_csv(DATASET_URL)
    return render_template("viewdata.html", columns=df.columns.values, rows=df.values.tolist())

@app.route('/preprocess')
def preprocess():
    global x_train, x_test, y_train, y_test
    df = pd.read_csv(DATASET_URL)
    x = df.drop('Stress_Level', axis=1)
    y = df['Stress_Level']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
    flash("✅ Data preprocessed successfully!", "success")
    return redirect(url_for('home'))

# -------------------------------
# MODEL TRAINING
# -------------------------------
@app.route('/model', methods=["POST", "GET"])
def model():
    global x_train, x_test, y_train, y_test
    try:
        _ = x_train.shape
    except NameError:
        flash("⚠️ Please run Preprocess first!", "warning")
        return redirect(url_for('home'))

    if request.method == "POST":
        algo = int(request.form['algo'])
        if algo == 1:
            model = RandomForestRegressor()
        elif algo == 2:
            model = AdaBoostRegressor()
        elif algo == 3:
            model = ExtraTreeRegressor()
        elif algo == 4:
            base_model = [('rf', RandomForestRegressor()), ('dt', ExtraTreeRegressor())]
            model = StackingRegressor(estimators=base_model, final_estimator=AdaBoostRegressor())
        else:
            flash("⚠️ Invalid algorithm selection.", "danger")
            return redirect(url_for('home'))

        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        score = r2_score(y_test, y_pred) * 100
        flash(f"Model trained! Accuracy: {score:.2f}%", "success")
    return redirect(url_for('home'))

# -------------------------------
# PREDICTION
# -------------------------------
@app.route('/prediction', methods=["POST","GET"])
def prediction():
    if request.method == 'POST':
        try:
            f1 = float(request.form['Heart_Rate'])
            f2 = float(request.form['Skin_Conductivity'])
            f3 = float(request.form['Hours_Worked'])
            f4 = float(request.form['Emails_Sent'])
            f5 = float(request.form['Meetings_Attended'])
            date = request.form['date']
            email = session.get('email')
            features = [f1, f2, f3, f4, f5]
        except (ValueError, KeyError):
            flash("⚠️ Invalid input.", "danger")
            return redirect(url_for('prediction'))

        model = RandomForestRegressor()
        model.fit(x_train, y_train)
        result = model.predict([features])[0]

        cur.execute("""INSERT INTO stress_prediction 
                       (email, heart_rate, skin_conductivity, hours_worked, emails_sent, meetings_attended, prediction, date)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (email, f1, f2, f3, f4, f5, float(result), date))
        conn.commit()

        stress_value = float(result)
        if stress_value < 20:
            suggestion = "Low Stress: Maintain healthy routine, sleep well, exercise."
            counseling_links = None
        elif stress_value < 30:
            suggestion = "Moderate Stress: Take breaks, practice meditation, avoid multitasking."
            counseling_links = None
        else:
            suggestion = "High Stress: Seek counseling, reduce workload, rest."
            counseling_links = [
                {"name": "NIMHANS", "url": "https://www.nimhans.ac.in/"},
                {"name": "iCall by TISS", "url": "https://icallhelpline.org/"},
                {"name": "YourDOST", "url": "https://yourdost.com/"},
            ]
        return render_template("prediction.html", msg=f"Stress Level: {stress_value:.2f}%", suggestion=suggestion, counseling_links=counseling_links)

    return render_template("prediction.html")

# -------------------------------
# DASHBOARD
# -------------------------------
@app.route('/dashboard')
def dashboard():
    email = session.get('email')
    filter_type = request.args.get('filter', 'all')

    if filter_type == 'week':
        from datetime import datetime, timedelta
        today = datetime.today()
        week_ago = today - timedelta(days=7)
        cur.execute("""SELECT date, prediction FROM stress_prediction 
                       WHERE email=%s AND date >= %s ORDER BY date""", (email, week_ago.strftime('%Y-%m-%d')))
    else:
        cur.execute("""SELECT date, prediction FROM stress_prediction 
                       WHERE email=%s ORDER BY date""", (email,))
    data = cur.fetchall()
    dates = [str(row[0]) for row in data]
    stress_levels = [row[1] for row in data]
    return render_template('dashboard.html', dates=dates, stress_levels=stress_levels, current_filter=filter_type)

# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
