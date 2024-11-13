import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('postgresql://postgres.xjlwrdolhwpgdikznbcs:[Telerik1234@]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres')