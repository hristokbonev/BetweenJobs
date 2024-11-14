import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

key = os.getenv("DB_KEY")

DATABASE_URL = "https://xjlwrdolhwpgdikznbcs.supabase.co"

supabase = create_client(DATABASE_URL, key)

