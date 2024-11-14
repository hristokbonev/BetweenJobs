from supabase import Client
import os

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv('SUPABASE_URL')
DATABASE_KEY = os.getenv('SUPABASE_KEY')

def create_client():
    return Client(DATABASE_URL, DATABASE_KEY)