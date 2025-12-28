from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

# --- Internal Imports (Assuming these files exist in your directory) ---
from bahire_hasab import get_bahire_hasab
from conversions import to_gc
from constants import *

app = FastAPI(title="Ethiopian Calendar API (Full Bahire Hasab)")

# --- 1. ENABLE CORS ---
# This allows your HTML/JS frontend to make requests to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. MOUNT STATIC FILES ---
# This allows the browser to load images from your "assest" folder
# Example: http://127.0.0.1:8000/assest/meskel.png
if not os.path.exists("assest"):
    os.makedirs("assest")
app.mount("/assest", StaticFiles(directory="assest"), name="assest")

# Pydantic models for input
class EthiopianDate(BaseModel):
    year: int
    month: int
    day: int

class MonthRequest(BaseModel):
    year: int
    month_idx: int  # 0-based index for month (0 = Meskerem)

# Endpoint: Convert Ethiopian date to Gregorian and weekday
@app.post("/convert")
async def convert_date(date_in: EthiopianDate):
    try:
        gc_date = to_gc(date_in.year, date_in.month, date_in.day)
        bahir = get_bahire_hasab(date_in.year)
        weekday = DAYS_OF_WEEK["english"][gc_date.weekday()]
        return {
            "ethiopian": f"{date_in.day} {MONTH_NAMES['english'][date_in.month-1]} {date_in.year}",
            "gregorian": gc_date.strftime("%B %d, %Y"), # Matches Tkinter date format
            "weekday": weekday,
            "movableFeasts": bahir.get("movableFeasts", {})
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint: Get month grid with holidays
@app.post("/month")
async def get_month(req: MonthRequest):
    try:
        year = req.year
        month_idx = req.month_idx
        # Leap year logic for Pagume (Month 13)
        num_days = 30 if month_idx < 12 else (6 if (year % 4 == 3) else 5)
        
        # Bahire Hasab data
        bahir = get_bahire_hasab(year)
        movable = bahir.get('movableFeasts', {})

        # Map holidays to days
        hols_map = {}
        for k, info in FIXED_HOLIDAYS.items():
            if info['month'] == month_idx + 1:
                hols_map.setdefault(info['day'], []).append(k)
        for k, info in movable.items():
            if info.get('ethiopian', {}).get('month') == month_idx + 1:
                hols_map.setdefault(info['ethiopian']['day'], []).append(k)

        # Calculate weekday alignment (Start column)
        first_day_gc = to_gc(year, month_idx + 1, 1)
        start_col = (first_day_gc.weekday() + 1) % 7

        # Build month grid
        month_grid = []
        for day in range(1, num_days + 1):
            idx = (day - 1) + start_col
            holidays = hols_map.get(day, [])
            month_grid.append({
                "day": day,
                "weekday": DAYS_OF_WEEK["english"][idx % 7],
                "holidays": holidays
            })

        return {
            "month_name": MONTH_NAMES['english'][month_idx], 
            "year": year, 
            "grid": month_grid,
            "start_col": start_col # Added for easier frontend alignment
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint: Get holiday details (Matches open_holiday_detail)
@app.get("/holiday/{holiday_key}")
async def holiday_detail(holiday_key: str):
    key = holiday_key.lower()
    data = HOLIDAY_INFO.get(key, {})
    if not data:
        raise HTTPException(status_code=404, detail="Holiday not found")
    return data

# Optional health check
@app.get("/")
async def root():
    return {"message": "Ethiopian Calendar API running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)