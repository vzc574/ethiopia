import tkinter as tk
from constants import MONTH_NAMES, DAYS_OF_WEEK, FIXED_HOLIDAYS, HOLIDAY_INFO
from conversions import to_gc
from bahire_hasab import get_bahire_hasab
root = tk.Tk()
root.title("Ethiopian Calendar Tool")
root.geometry("600x650")

# --- Year Input Selection ---
year_frame = tk.Frame(root)
year_frame.pack(pady=10)

tk.Label(year_frame, text="Enter Ethiopian Year:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
year_entry = tk.Entry(year_frame, width=8, font=("Arial", 11))
year_entry.insert(0, "2016")  
year_entry.pack(side=tk.LEFT)

# --- Data Setup ---
eth = MONTH_NAMES["english"]
amh = MONTH_NAMES["amharic"]
MONTH_DAYS = [30]*12 + [5]

def get_holiday_names(month_index, day, movable_feasts):
    """Utility to get holiday names for display, including fixed and movable holidays."""
    found_names = []
    target_month = month_index + 1

    # Fixed holidays
    for key, info in FIXED_HOLIDAYS.items():
        if info['month'] == target_month and info['day'] == day:
            names = HOLIDAY_INFO.get(key, {}).get('name', {})
            eng = names.get('english', key.capitalize())
            amharic = names.get('amharic', "")
            found_names.append(f"{eng} ({amharic})")

    # Movable holidays
    for key, info in movable_feasts.items():
        ethiopian_date = info['ethiopian']
        if ethiopian_date['month'] == target_month and ethiopian_date['day'] == day:
            names = HOLIDAY_INFO.get(key, {}).get('name', {})
            eng = names.get('english', key.capitalize())
            amharic = names.get('amharic', "")
            found_names.append(f"{eng} ({amharic})")

    return found_names

def open_day_window(month_index):
    try:
        current_year = int(year_entry.get())
    except ValueError:
        current_year = 2016

    # Calculate Bahire Hasab for the year to get movable feasts
    bahire = get_bahire_hasab(current_year, lang="english")
    movable_feasts = bahire['movableFeasts']

    month_name_eth = eth[month_index]
    day_window = tk.Toplevel(root)
    day_window.title(f"{month_name_eth} - {current_year}")
    day_window.geometry("600x550")

    display_label = tk.Label(day_window, text="Select a highlighted day to see the holiday!",
                             font=("Arial", 11, "italic"), pady=10)
    display_label.pack()

    day_frame = tk.Frame(day_window)
    day_frame.pack(pady=10)

    num_days = MONTH_DAYS[month_index]
    week_names = DAYS_OF_WEEK["english"]

    for day in range(1, num_days + 1):
        day_of_week = week_names[(day - 1) % 7]

        # Check if today is a holiday to set button color (now includes movable holidays)
        holidays_today = get_holiday_names(month_index, day, movable_feasts)
        bg_color = "#ffcccc" if holidays_today else "SystemButtonFace" # Light red if holiday
        fg_color = "red" if holidays_today else "black"

        def make_command(d=day, dow=day_of_week, h=holidays_today):
            def on_day_click():
                greg_date = to_gc(current_year, month_index + 1, d)
                greg_str = greg_date.strftime("%B %d, %Y")

                info_text = (f"Ethiopian: {month_name_eth} {d}, {current_year} ({dow})\n"
                             f"Gregorian: {greg_str}")

                if h:
                    h_text = "\n\nHoliday: " + ", ".join(h)
                    display_label.config(text=info_text + h_text, fg="red")
                else:
                    display_label.config(text=info_text + "\n\nNo holiday", fg="black")
            return on_day_click

        row = (day - 1) // 7
        col = (day - 1) % 7

        btn = tk.Button(day_frame, text=f"{day}", width=8,
                        bg=bg_color, fg=fg_color,
                        command=make_command())
        btn.grid(row=row, column=col, padx=2, pady=2)

# --- Main Menu Month Buttons ---
tk.Label(root, text="Select an Ethiopian Month", font=("Arial", 14, "bold")).pack(pady=5)

for i in range(len(eth)):
    btn = tk.Button(root, text=f"{eth[i]} | {amh[i]}", font=("Arial", 10),
                   command=lambda idx=i: open_day_window(idx))
    btn.pack(fill="x", padx=40, pady=2)

root.mainloop()