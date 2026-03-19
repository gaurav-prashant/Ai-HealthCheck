# ============================================================
# auth.py — Authentication with Supabase
# ============================================================

import os
from supabase import create_client, Client
import streamlit as st

# Environment Variables for Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# Initialize Client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    supabase = None

def save_user(username, password, email, name):
    if not supabase:
        st.error("Supabase not configured. Add SUPABASE_URL and SUPABASE_KEY to your .env file.")
        return False
    try:
        # Sign up the user in Supabase auth
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "username": username,
                    "name": name
                }
            }
        })
        if res and res.user:
            return True
        return False
    except Exception as e:
        # Supabase Python client raises an Exception if sign up fails
        if "already registered" in str(e).lower() or "User already registered" in str(e):
            st.error("Email is already registered!")
        else:
            st.error(f"Sign up failed: {e}")
        return False

def verify_user(email, password):
    """Logs the user in with Supabase Auth using email and password."""
    if not supabase:
        st.error("Supabase not configured. Add SUPABASE_URL and SUPABASE_KEY to your .env file.")
        return False
    try:
        # Sign in with email and password
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        # If response contains a user, login was successful
        if res and res.user:
            return True
        return False
    except Exception as e:
        # Login failed
        return False

def get_user_name(email):
    """Retrieve user metadata if available."""
    if not supabase:
        return email
    try:
        # Tries to get the current session of the logged in user
        session = supabase.auth.get_session()
        if session and session.user:
            return session.user.user_metadata.get("name", email)
        return email
    except:
        return email