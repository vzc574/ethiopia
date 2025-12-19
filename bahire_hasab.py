import tkinter as tk
from constants import MONTH_NAMES, DAYS_OF_WEEK, FIXED_HOLIDAYS
from bahire_hasab import get_bahire_hasab  # your module

root = tk.Tk()
root.title("Ethiopian Months")
root.geometry("600x550")

label = tk.Label(root, text="Select a Month", font=("Arial", 14))
label.pack(pady=10)

eth = MONTH_NAMES["english"]
amh = MONTH_NAMES["amharic"]
greg = MONTH_NAMES["gregorian"]

MONTH_DAYS = [30]*12 + [5]

ethiopian_year = 2016  # Example year; you can make it dynamic

# Calculate Bahire Hasab for the year
bahire = get_bahire_hasab(ethiopian_year, lang="english")
movable_feasts = bahire['movableFeasts']

# Helper to get holidays for a given day
def get_holidays(month_index, day):
    holidays_list = []

    # Fixed holidays
    for key, info in FIXED_HOLIDAYS.items():
        if info['month'] == month_index + 1 and info['day'] == day:
            holidays_list.append(key)

    # Movable holidays
    for key, info in movable_feasts.items():
        ethiopian_date = info['ethiopian']
        if ethiopian_date['month'] == month_index + 1 and ethiopian_date['day'] == day:
            holidays_list.append(key)

    return holidays_list

# Open day window
def open_day_window(month_index):
    month_name = f"{eth[month_index]} | {amh[month_index]} | {greg[month_index] if month_index < 12 else '—'}"
    
    day_window = tk.Toplevel(root)
    day_window.title(f"Days of {month_name}")
    day_window.geometry("500x400")

    day_label = tk.Label(day_window, text=f"Selected Month: {month_name}", font=("Arial", 12))
    day_label.pack(pady=10)

    day_frame = tk.Frame(day_window)
    day_frame.pack(pady=10)

    num_days = MONTH_DAYS[month_index]
    week_names = DAYS_OF_WEEK["english"]

    for day in range(1, num_days + 1):
        day_of_week = week_names[(day - 1) % 7]
        btn_text = f"{day} | {day_of_week}"

        def on_day_click(d=day):
            holidays = get_holidays(month_index, d)
            if holidays:
                holiday_names = ', '.join([h.capitalize() for h in holidays])
                day_label.config(text=f"{month_name} - Day {d} ({day_of_week})\nHoliday: {holiday_names}")
            else:
                day_label.config(text=f"{month_name} - Day {d} ({day_of_week})\nNo holiday")

        row = (day - 1) // 7
        col = (day - 1) % 7
        btn = tk.Button(day_frame, text=btn_text, width=12, command=on_day_click)
        btn.grid(row=row, column=col, padx=2, pady=2)

# Month buttons
for i in range(len(eth)):
    greg_name = greg[i] if i < 12 else "—"
    text = f"{eth[i]} | {amh[i]} | {greg_name}"
    
    btn = tk.Button(
        root,
        text=text,
        command=lambda idx=i: open_day_window(idx)
    )
    btn.pack(fill="x", padx=20, pady=3)

root.mainloop()
