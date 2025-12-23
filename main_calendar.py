import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# --- Imports (Ensure these files are in the same folder) ---
from constants import (
    MONTH_NAMES, DAYS_OF_WEEK, FIXED_HOLIDAYS, HOLIDAY_INFO,
    MOVABLE_HOLIDAYS
)
from conversions import to_gc
from bahire_hasab import get_bahire_hasab


class EthiopianCalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ethiopian Calendar Tool")
        self.root.geometry("600x750")

        # --- BACKGROUND IMAGE SECTION ---
        bg_image_path = "assest/ortho.png"
        if os.path.exists(bg_image_path):
            self.bg_raw = Image.open(bg_image_path)
            self.bg_resized = self.bg_raw.resize((600, 750), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_resized)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # --- YEAR INPUT ---
        self.year_frame = tk.Frame(self.root)
        self.year_frame.pack(pady=20)
        tk.Label(self.year_frame, text="Ethiopian Year:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        self.year_entry = tk.Entry(self.year_frame, width=10, font=("Arial", 12))
        self.year_entry.insert(0, "2016")
        self.year_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.root, text="Select a Month", font=("Arial", 14, "bold")).pack(pady=10)

        # --- MONTH BUTTONS ---
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(fill="both", expand=True, padx=50)

        greg_months = MONTH_NAMES.get("gregorian", [])

        for i, (eng, amh) in enumerate(zip(MONTH_NAMES["english"], MONTH_NAMES["amharic"])):
            g_name = f" ({greg_months[i]})" if i < len(greg_months) else ""
            btn_text = f"{eng} | {amh}{g_name}"

            tk.Button(self.menu_frame, text=btn_text, font=("Arial", 11),
                      command=lambda idx=i: self.open_month_window(idx)).pack(fill="x", pady=2)

        # --- CONVERTER SECTION (Added to Free Space) ---
        self.conv_frame = tk.Frame(self.root, padx=10, pady=10, relief="groove", bd=2)
        self.conv_frame.pack(side="bottom", fill="x", padx=50, pady=20)

        tk.Label(self.conv_frame, text="E.C. to G.C. Converter", font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=4, pady=5)
        tk.Label(self.conv_frame, text="Day:").grid(row=1, column=0)
        self.conv_day = tk.Entry(self.conv_frame, width=5)
        self.conv_day.grid(row=1, column=1, padx=5)
        tk.Label(self.conv_frame, text="Month (1-13):").grid(row=1, column=2)
        self.conv_month = tk.Entry(self.conv_frame, width=5)
        self.conv_month.grid(row=1, column=3, padx=5)

        self.conv_result = tk.Label(self.conv_frame, text="Result: ---", font=("Arial", 10, "italic"), fg="blue")
        self.conv_result.grid(row=2, column=0, columnspan=3, pady=10)

        # THIS LINE UPDATED FOR COLOR:
        tk.Button(self.conv_frame, text="Convert", bg="green", fg="white", 
                  command=self.run_conversion).grid(row=2, column=3, pady=10)
    def run_conversion(self):
        """Logic for the date converter using imported to_gc."""
        try:
            day = int(self.conv_day.get())
            month = int(self.conv_month.get())
            year = int(self.year_entry.get())
            gc_date = to_gc(year, month, day)
            self.conv_result.config(text=f"GC: {gc_date.strftime('%B %d, %Y')}", fg="green")
        except Exception:
            self.conv_result.config(text="Invalid Input", fg="red")

    def open_holiday_detail(self, holiday_key):
        detail_win = tk.Toplevel(self.root)
        detail_win.title(f"Detail: {holiday_key}")
        detail_win.geometry("500x750")

        data = HOLIDAY_INFO.get(holiday_key.lower(), {})
        if not data:
            messagebox.showinfo("Info", "No data found.")
            return

        tk.Label(detail_win, text=data['name'].get('english', ''), font=("Arial", 16, "bold")).pack(pady=(15, 0))
        tk.Label(detail_win, text=data['name'].get('amharic', ''), font=("Nyala", 22), fg="#b22222").pack(pady=5)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        rel_path = data.get('image', '')
        image_path = os.path.join(script_dir, rel_path)

        if rel_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img.thumbnail((400, 500), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(detail_win, image=photo)
                img_label.image = photo
                img_label.pack(pady=10)
            except Exception as e:
                tk.Label(detail_win, text=f"Error loading image: {e}", fg="red").pack()
        else:
            tk.Label(detail_win, text="[ Image Not Found ]", fg="green", width=30, height=8).pack(pady=10)

        tk.Label(detail_win, text=data['description'].get('amharic', ''), font=("Nyala", 14), wraplength=450, justify="center").pack(pady=10)
        tk.Label(detail_win, text=data['description'].get('english', ''), font=("Arial", 11, "italic"), wraplength=450, fg="red", justify="center").pack(pady=10)

        tk.Button(detail_win, text="Close", command=detail_win.destroy, width=15).pack(pady=20)

    def open_month_window(self, month_idx):
        try:
            year = int(self.year_entry.get())
        except:
            year = 2018

        num_days = 30 if month_idx < 12 else (6 if (year % 4 == 3) else 5)
        bahir = get_bahire_hasab(year, lang="english")
        movable = bahir.get('movableFeasts', {})

        hols_map = {}
        for k, info in FIXED_HOLIDAYS.items():
            if info['month'] == month_idx + 1: hols_map.setdefault(info['day'], []).append(k)
        for k, info in movable.items():
            if info.get('ethiopian', {}).get('month') == month_idx + 1:
                hols_map.setdefault(info['ethiopian']['day'], []).append(k)

        first_day_gc = to_gc(year, month_idx + 1, 1)
        start_col = (first_day_gc.weekday() + 1) % 7

        win = tk.Toplevel(self.root)
        win.title(f"{MONTH_NAMES['english'][month_idx]} {year}")
        grid = tk.Frame(win)
        grid.pack(pady=20, padx=20)

        for i, day_name in enumerate(DAYS_OF_WEEK["english"]):
            tk.Label(grid, text=day_name[:3], font=("Arial", 10, "bold")).grid(row=0, column=i)

        for day in range(1, num_days + 1):
            idx = (day - 1) + start_col
            h_keys = hols_map.get(day, [])

            btn = tk.Button(grid, text=str(day), width=8, height=2,
                            fg="red" if h_keys else "black",
                            bg="blue" if h_keys else "orange",
                            command=lambda k=h_keys: self.open_holiday_detail(k[0]) if k else None)
            btn.grid(row=(idx // 7) + 1, column=idx % 7, padx=2, pady=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = EthiopianCalendarApp(root)
    root.mainloop()