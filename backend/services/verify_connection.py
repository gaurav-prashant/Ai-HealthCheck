from dotenv import load_dotenv
load_dotenv()

from backend.services.auth import get_supabase_status


print("Testing Supabase Connection...")
ok, status = get_supabase_status()
print(f"Status: {status}")
if ok:
    print("SUCCESS: Connected to Supabase!")
else:
    print(f"FAILED: {status}")
