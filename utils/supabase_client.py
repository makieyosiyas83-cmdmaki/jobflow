import os
from supabase import create_client

def upsert_jobs(jobs):
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    client = create_client(url, key)
    return client.table("jobs").upsert(jobs, on_conflict="external_id").execute()
