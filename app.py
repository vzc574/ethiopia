from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# --- Internal Imports ---
from constants import (
    MONTH_NAMES, DAYS_OF_WEEK, FIXED_HOLIDAYS, HOLIDAY_INFO,
    MOVABLE_HOLIDAYS
)
from conversions import to_gc
from bahire_hasab import get_bahire_hasab

# 1. Initialize the App FIRST
app = FastAPI()

# 2. Ensure the assets directory exists and mount it
# This allows your frontend to access images at http://127.0.0.1:8000/assest/filename.png
if not os.path.exists("assest"):
    os.makedirs("assest")
app.mount("/assest", StaticFiles(directory="assest"), name="assest")

# 3. Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/month/{year}/{month_idx}")
def get_month_grid(year: int, month_idx: int):
    try:
        # Leap year logic for Pagume (Month 13) matching main_calendar.py
        num_days = 30 if month_idx < 12 else (6 if (year % 4 == 3) else 5)
        
        bahir = get_bahire_hasab(year, lang="english")
        movable = bahir.get('movableFeasts', {})

        hols_map = {}
        for k, info in FIXED_HOLIDAYS.items():
            if info['month'] == month_idx + 1:
                hols_map.setdefault(info['day'], []).append(k)
        
        for k, info in movable.items():
            if info.get('ethiopian', {}).get('month') == month_idx + 1:
                hols_map.setdefault(info['ethiopian']['day'], []).append(k)

        first_day_gc = to_gc(year, month_idx + 1, 1)
        start_col = (first_day_gc.weekday() + 1) % 7

        return {
            "month_name": MONTH_NAMES['english'][month_idx],
            "num_days": num_days,
            "start_col": start_col,
            "holidays": hols_map,
            "evangelist": bahir['evangelist']['name']
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/detail/{holiday_key}")
def get_holiday_detail(holiday_key: str):
    # Matches HOLIDAY_INFO lookup for names, descriptions, and image paths
    data = HOLIDAY_INFO.get(holiday_key.lower(), {})
    if not data:
        raise HTTPException(status_code=404, detail="No data found.")
    return data

@app.get("/convert")
def run_conversion(year: int, month: int, day: int):
    try:
        gc_date = to_gc(year, month, day)
        return {"formatted": gc_date.strftime('%B %d, %Y')}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Input")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)