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
            # 1. Load and Resize the image
            self.bg_raw = Image.open(bg_image_path)
            self.bg_resized = self.bg_raw.resize((600, 750), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_resized)

            # 2. Create the Background Label
            self.bg_label = tk.Label(self.root, image=self.bg_photo)

            # 3. Place it at the very back (0,0) covering the whole window
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # --- IMPORTANT: MAKE SURE YOUR OTHER FRAMES USE A BACKGROUND COLOR ---
        # Otherwise, they might have a default grey box around them.
        # Example: self.menu_frame = tk.Frame(self.root, bg="white")
        self.year_frame = tk.Frame(self.root)
        self.year_frame.pack(pady=20)
        tk.Label(self.year_frame, text="Ethiopian Year:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        self.year_entry = tk.Entry(self.year_frame, width=10, font=("Arial", 12))
        self.year_entry.insert(0, "2016")
        self.year_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.root, text="Select a Month", font=("Arial", 14, "bold")).pack(pady=10)

        # Month Buttons
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(fill="both", expand=True, padx=50)

        # Gregorian months for the label
        greg_months = MONTH_NAMES.get("gregorian", [])

        for i, (eng, amh) in enumerate(zip(MONTH_NAMES["english"], MONTH_NAMES["amharic"])):
            # Check if there is a matching Gregorian month name
            g_name = f" ({greg_months[i]})" if i < len(greg_months) else ""
            btn_text = f"{eng} | {amh}{g_name}"

            tk.Button(self.menu_frame, text=btn_text, font=("Arial", 10),
                      command=lambda idx=i: self.open_month_window(idx)).pack(fill="x", pady=2)

    def open_holiday_detail(self, holiday_key):
        """Displays Holiday Detail Window with Image and Description."""
        detail_win = tk.Toplevel(self.root)
        detail_win.title(f"Detail: {holiday_key}")
        # Smaller, cleaner window size
        detail_win.geometry("500x750")
        detail_win.configure(bg="blue")

        data = HOLIDAY_INFO.get(holiday_key.lower(), {})
        if not data:
            messagebox.showinfo("Info", "No data found.")
            return

        # Titles
        tk.Label(detail_win, text=data['name'].get('english', ''), font=("Arial", 16, "bold"), bg="yellow").pack(
            pady=(15, 0))
        tk.Label(detail_win, text=data['name'].get('amharic', ''), font=("Nyala", 22), bg="white", fg="#b22222").pack(
            pady=5)

        # --- IMAGE LOADING ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        rel_path = data.get('image', '')
        image_path = os.path.join(script_dir, rel_path)

        if rel_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)

                # --- FIX: SMART RESIZING ---
                # This ensures the image is never bigger than 400x500
                # but stays perfectly proportional (not stretched).
                max_display_size = (400, 500)
                img.thumbnail(max_display_size, Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(detail_win, image=photo, bg="yellow")
                img_label.image = photo  # Keep reference
                img_label.pack(pady=10)
            except Exception as e:
                tk.Label(detail_win, text=f"Error loading image: {e}", fg="red", bg="white").pack()
        else:
            # Fallback for other holidays
            tk.Label(detail_win, text="[ Image coming soon ]", bg="#f9f9f9", fg="gray",
                     width=30, height=8, font=("Arial", 10, "italic")).pack(pady=10)

        # Descriptions
        tk.Label(detail_win, text=data['description'].get('amharic', ''), font=("Nyala", 14),
                 bg="red", wraplength=450, justify="center").pack(pady=10)
        tk.Label(detail_win, text=data['description'].get('english', ''), font=("Arial", 11, "italic"),
                 bg="red", wraplength=450, fg="#444", justify="center").pack(pady=10)

        tk.Button(detail_win, text="Close", command=detail_win.destroy, bg="yellow", fg="brown", width=15).pack(pady=20)

    def open_month_window(self, month_idx):
        try:
            year = int(self.year_entry.get())
        except:
            year = 2016

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
                            bg="green" if h_keys else "SystemButtonFace",
                            command=lambda k=h_keys: self.open_holiday_detail(k[0]) if k else None)
            btn.grid(row=(idx // 7) + 1, column=idx % 7, padx=2, pady=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = EthiopianCalendarApp(root)
    root.mainloop()