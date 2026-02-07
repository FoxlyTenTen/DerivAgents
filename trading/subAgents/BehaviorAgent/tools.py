import os
import time
import re
from trading.services.supabase_client import get_supabase

# Maps Deriv's technical codes to Human Readable Names
ASSET_MAP = {
    "1HZ100V": "Vol_100_1s",
    "R_100": "Vol_100",
    "R_75": "Vol_75",
    "R_50": "Vol_50",
    "BTCUSD": "Bitcoin",
    # Add more as you discover them
}

def normalize_symbol(raw_shortcode: str) -> str:
    """
    Turns 'ACCU_1HZ100V_13.00_...' into 'Vol_100_1s'
    """
    # Look for patterns like '1HZ100V' or 'R_100' inside the mess
    match = re.search(r'(1HZ\d+V|R_\d+|BTCUSD|ETHUSD)', raw_shortcode)
    
    if match:
        deriv_code = match.group(1)
        # Return the human name, or the code if not in map
        return ASSET_MAP.get(deriv_code, deriv_code)
    
    return "Unknown_Asset"

def get_behavior_metrics(current_asset: str = "Vol_100") -> dict:
    """
    Analyzes the user's REAL trade history from Supabase to detect 
    psychological 'Tilt' and behavioral risks.
    """
    # In a real app, you'd get the user_id from the session/auth.
    # For now, we'll use a placeholder or check env.
    user_id = os.environ.get("DEMO_USER_ID", "USER_123") 
    
    try:
        supabase = get_supabase()
        
        # 1. Fetch History from Supabase
        # Querying the 'trade_history' table we created
        response = supabase.table("trade_history") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("buy_time", desc=True) \
            .limit(50) \
            .execute()
        
        trades = response.data
        
        if not trades:
            return {
                "user_id": user_id,
                "status": "No trade history found in Supabase. Mindset: Unknown."
            }

        # 2. Perform the Behavior Math
        last_trade = trades[0]
        now = time.time()

        # --- METRIC 1: REVENGE TRADING DETECTION ---
        # Logic: If last trade was a LOSS and happened < 5 mins (300s) ago
        # Note: buy_time is Unix timestamp in our table
        seconds_since_last_trade = int(now - last_trade['buy_time'])
        is_revenge_risk = (float(last_trade['profit']) < 0) and (seconds_since_last_trade < 300)

        # --- METRIC 2: LOSING STREAK ---
        loss_streak = 0
        for trade in trades:
            if float(trade['profit']) < 0:
                loss_streak += 1
            else:
                break

        # --- METRIC 3: ASSET TOXICITY ---
        asset_stats = {}
        for trade in trades:
            raw_symbol = trade['symbol']
            clean_asset = normalize_symbol(raw_symbol) # Clean the name
            
            if clean_asset not in asset_stats:
                asset_stats[clean_asset] = {"wins": 0, "total": 0}
            
            asset_stats[clean_asset]["total"] += 1
            if float(trade['profit']) > 0:
                asset_stats[clean_asset]["wins"] += 1

        toxic_asset = None
        worst_win_rate = 1.0
        for asset, stats in asset_stats.items():
            if stats["total"] >= 5:
                win_rate = stats["wins"] / stats["total"]
                if win_rate < 0.4 and win_rate <= worst_win_rate:
                    worst_win_rate = win_rate
                    toxic_asset = asset

        # 3. Final Payload for Gemini
        return {
            "user_id": user_id,
            "current_asset_context": current_asset,
            "current_state": {
                "seconds_since_last_trade": seconds_since_last_trade,
                "last_result": "WIN" if float(last_trade['profit']) > 0 else "LOSS",
                "current_loss_streak": loss_streak,
                "is_revenge_trading_risk": is_revenge_risk
            },
            "patterns": {
                "toxic_asset": toxic_asset,
                "toxic_asset_win_rate": f"{worst_win_rate * 100:.1f}%" if toxic_asset else "N/A",
                "is_viewing_toxic_asset": (current_asset in toxic_asset if toxic_asset else False)
            }
        }

    except Exception as e:
        return {"error": f"Failed to fetch behavior metrics from Supabase: {str(e)}"}