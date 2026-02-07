import os
import asyncio
from dotenv import load_dotenv
from trading.services.deriv_service import sync_user_trades

# Load .env
load_dotenv()

async def main():
    token = os.environ.get("DERIV_TOKEN")
    
    if not token:
        print("❌ Error: DERIV_TOKEN not found in .env file.")
        return

    print("🚀 Starting Deriv-to-Supabase Sync...")
    try:
        await sync_user_trades(token)
        print("✨ All done! Your database is now populated.")
        print("You can now run your agent in the ADK Web interface.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
