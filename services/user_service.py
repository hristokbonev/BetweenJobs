from data.database import supabase as db
from data.models.user import Users
from typing import List
from datetime import datetime
import base64


def view_users() -> List[Users]:
    response = db.table("Users").select("id, username, first_name, last_name, is_admin, date_of_birth, email").execute()

    if not response:
        raise ValueError("Error fetching users:")

    all_users = [Users.from_query_str(**user_data) for user_data in response.data]

    return all_users


def create_user(username, password, first_name, last_name, birthdate, email):
    # Convert birthdate to an ISO 8601 string format if it's a datetime object
    birthdate_str = birthdate.isoformat() if isinstance(birthdate, datetime) else birthdate

    # Hash the password securely
    hashed_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')

    data = {
        "username": username,
        "password": hashed_password,
        "first_name": first_name,
        "last_name": last_name,
        "date_of_birth": birthdate_str,
        "email": email
    }


    response = db.table("Users").upsert(data).execute()
    if not response or not response.data:
        raise ValueError("Cannot create user. Please check input details")

    # Retrieve and return the created user data
    created_user_data = response.data[0] if response.data else None
    return Users(**created_user_data)
