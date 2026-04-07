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
    """Signs up a new user in Supabase Auth.
    Returns: (bool, str) - (Success Status, Error Message)
    """
    if not supabase:
        return False, "Supabase configuration is missing or invalid. Check your .env for SUPABASE_URL and SUPABASE_KEY."
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
            # Also store in public.profiles table
            try:
                supabase.table("profiles").insert({
                    "id": res.user.id,
                    "username": username,
                    "name": name,
                    "email": email
                }).execute()
            except Exception as profile_err:
                # Log the error but don't fail the whole registration
                # as the Auth user is already created.
                print(f"Profile storage failed: {profile_err}")
            
            return True, ""
        return False, "Sign up failed: Unknown error."
    except Exception as e:
        # Supabase Python client raises an Exception if sign up fails
        err_str = str(e).lower()
        if "already registered" in err_str:
            return False, "This email is already registered!"
        elif "invalid api key" in err_str or "apikey is not valid" in err_str:
            return False, "The Supabase API Key (.env) is invalid. It should be a long JWT string starting with 'eyJ'."
        return False, f"Sign up failed: {e}"

def verify_user(email, password):
    """Logs the user in with Supabase Auth using email and password.
    Returns: (bool, str) - (Success Status, Error Message)
    """
    if not supabase:
        return False, "Supabase configuration is missing or invalid. Check your .env for SUPABASE_URL and SUPABASE_KEY."
    try:
        # Sign in with email and password
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        # If response contains a user, login was successful
        if res and res.user:
            return True, ""
        return False, "Login failed: Unknown error."
    except Exception as e:
        # Login failed (typically invalid credentials or network issue)
        err_str = str(e).lower()
        if "invalid login credentials" in err_str:
            return False, "Invalid email or password."
        elif "email not confirmed" in err_str:
            return False, "Email not confirmed! Please check your inbox or disable 'Confirm email' in Supabase Authentication settings."
        elif "invalid api key" in err_str or "apikey is not valid" in err_str:
            return False, "The Supabase API Key (.env) is invalid. It should be a long JWT string starting with 'eyJ'."
        return False, f"Login failed: {e}"

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
    except Exception:
        return email

def get_supabase_status():
    """Checks if Supabase client is initialized and reachable."""
    if not supabase:
        return False, "Config Missing"
    try:
        # Try to select from profiles. If table is missing, it's a setup issue.
        # If API key is wrong, it's a connection issue.
        supabase.table("profiles").select("id").limit(1).execute()
        return True, "Connected"
    except Exception as e:
        err_str = str(e).lower()
        if "profiles" in err_str and "not found" in err_str:
            # Table is missing, but connection/API key is likely OK
            return True, "Table Missing (Run setup.sql)"
        elif "apikey" in err_str or "invalid api key" in err_str:
            return False, "Invalid API Key"
        print(f"Supabase connection error: {e}")
        return False, "Connection Error"

# ── CHAT HISTORY ──
def save_chat_message(email: str, role: str, message: str):
    """Save a single chat message to Supabase chat_history table."""
    if not supabase:
        return
    try:
        supabase.table("chat_history").insert({
            "user_email": email,
            "role": role,
            "message": message
        }).execute()
    except Exception as e:
        print(f"Chat save error: {e}")

@st.cache_data(ttl=60)
def load_chat_history(email: str, limit: int = 100) -> list:
    """Load the last N chat messages for a user from Supabase."""
    if not supabase:
        return []
    try:
        res = supabase.table("chat_history") \
            .select("role, message") \
            .eq("user_email", email) \
            .order("created_at", desc=False) \
            .limit(limit) \
            .execute()
        return [(row["role"], row["message"]) for row in (res.data or [])]
    except Exception as e:
        print(f"Chat load error: {e}")
        return []

def clear_chat_history(email: str):
    """Delete all chat history for a user from Supabase."""
    if not supabase:
        return
    try:
        supabase.table("chat_history").delete().eq("user_email", email).execute()
    except Exception as e:
        print(f"Chat clear error: {e}")