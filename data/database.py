import os
# from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

key = os.getenv("DB_KEY")

# Construct the full DATABASE_URL
DATABASE_URL = "https://xjlwrdolhwpgdikznbcs.supabase.co"

supabase = create_client(DATABASE_URL, key)

