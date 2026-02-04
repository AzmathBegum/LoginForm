import streamlit as st
import mysql.connector
from mysql.connector import Error
import re
import time
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="User Authentication",
    page_icon="🔐",
    layout="centered"
)

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT"))

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# ---------------- DB FUNCTIONS ---------------- #

import tempfile

def get_db_connection():
    try:
        ca_cert = os.getenv("DB_CA_CERT")

        if not ca_cert:
            st.error("❌ CA certificate not found in secrets")
            return None

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(ca_cert.encode())
            ca_path = f.name

        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            ssl_ca=ca_path,
            ssl_verify_cert=False,   # 🔥 THIS IS THE KEY FIX
            connection_timeout=15
        )

    except Error as e:
        st.error(f"❌ Database Connection Error: {e}")
        return None



def create_users_table():
    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


def register_user(username, email, password):
    if not username or not email or not password:
        st.warning("⚠️ All fields are required")
        return False

    if len(password) < 6:
        st.warning("⚠️ Password must be at least 6 characters")
        return False

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        st.warning("⚠️ Invalid email format")
        return False

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.IntegrityError:
        st.error("❌ Username or email already exists")
        return False


def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

# ---------------- UI ---------------- #

def main():
    create_users_table()

    st.title("🔐 Secure Login System")

    if st.session_state.logged_in:
        st.success(f"✅ Welcome, {st.session_state.username}")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
        return

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")

        if login_btn:
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

    with tab2:
        with st.form("register_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            register_btn = st.form_submit_button("Register")

        if register_btn:
            if register_user(username, email, password):
                st.success("✅ Account created. You can login now.")

    st.markdown("---")
    st.caption("Built with Streamlit & MySQL (Aiven)")

if __name__ == "__main__":
    main()
