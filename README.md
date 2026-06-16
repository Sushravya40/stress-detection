# Stress Detection in IT Professionals 🧠💻

A Machine Learning-powered web application built with Python and Flask that predicts and monitors the stress levels of IT professionals based on their daily work habits and physiological data.

## 🚀 Features

* **Machine Learning Prediction:** Uses multiple algorithms (Random Forest, Extra Trees, AdaBoost, Stacking, and Decision Tree) to accurately predict stress levels.
* **Personalized Dashboard:** Users can track their stress history over time (weekly/all-time) using interactive data visualizations.
* **Smart Suggestions:** Provides tailored mental health advice and links to professional counseling services depending on the calculated stress severity.
* **Admin Panel:** Administrators can securely manage registered users and whitelist approved employee email domains.
* **Secure Authentication:** User login and registration system with session management.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Machine Learning:** Scikit-Learn, Pandas, NumPy
* **Frontend:** HTML, CSS, Jinja2 Templates
* **Database:** MySQL

## 📊 Dataset & Inputs

The prediction model takes into account the following parameters:
1. Heart Rate (bpm)
2. Skin Conductivity
3. Hours Worked
4. Emails Sent
5. Meetings Attended

## ⚙️ Local Setup Instructions

### 1. Prerequisites
* Python 3.8+
* MySQL Server

### 2. Database Configuration
1. Open MySQL and create a database named `Stress1`:
   ```sql
   CREATE DATABASE Stress1;
   ```
2. Import the provided `databse.sql` file into your `Stress1` database to set up the necessary tables (user accounts, predictions, admin emails).
3. In `app1.py`, ensure your database credentials (username and password) match your local MySQL setup (Default username is `root` with an empty password).

### 3. Application Setup
1. Clone this repository to your local machine.
2. Navigate to the project directory:
   ```bash
   cd stress-detection
   ```
3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app1.py
   ```
5. Open your web browser and go to `http://127.0.0.1:5000`.

## 🛡️ Admin Access
To access the admin panel and manage allowed corporate email domains:
* **Email:** admin@example.com
* **Password:** admin123
*(Note: Change these credentials in `app1.py` before deploying to production)*

---

## 📸 Screenshots

*(Add your screenshots here. You can drag and drop images directly into GitHub to upload them!)*

---

## 🔮 Future Enhancements

* **Wearable Integration:** Direct sync with smartwatches for live heart rate and skin conductivity data.
* **AI Chatbot:** A companion chatbot to offer immediate cognitive behavioral therapy exercises.
* **Organization Analytics:** Aggregated anonymous reports for HR departments to monitor overall company health.