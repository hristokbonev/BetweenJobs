import os
from dotenv import load_dotenv
from supabase import Client

load_dotenv()

DATABASE_URL = os.getenv('SUPABASE_URL')
DATABASE_KEY = os.getenv('SUPABASE_KEY')

def create_client():
    return Client(DATABASE_URL, DATABASE_KEY)