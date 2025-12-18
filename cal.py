print("CAL.PY IS RUNNING")
import tkinter as tk
from tkinter import messagebox, ttk
from conversions import to_gc, to_ec
from bahire_hasab import get_bahire_hasab


# =========================
# Conversion Functions
# =========================
print("CAL.PY IS RUNNING")

def convert_eth_to_greg():
    try:
        year = int(eth_year_entry.get())
        month = int(eth_month_entry.get())
        day = int(eth_day_entry.get())

        gregorian_date = to_gc(year, month, day)

        eth_result_label.config(text=f"Ethiopian: {month}/{day}/{year}")
        greg_result_label.config(
            text=f"Gregorian: {gregorian_date.month}/{gregorian_date.day}/{gregorian_date.year}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def convert_greg_to_eth():
    try:
        year = int(greg_year_entry.get())
        month = int(greg_month_entry.get())
        day = int(greg_day_entry.get())

        eth = to_ec(year, month, day)

        greg_result_label2.config(text=f"Gregorian: {month}/{day}/{year}")
        eth_result_label2.config(
            text=f"Ethiopian: {eth['month']}/{eth['day']}/{eth['year']}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# =========================
# Bahire Hasab Function
# =========================

def calculate_bahire_hasab():
    try:
        year = int(bh_year_entry.get())
        bh = get_bahire_hasab(year)

        # Clear table
        for row in bh_table.get_children():
            bh_table.delete(row)

        # Insert main info as rows
        bh_table.insert("", tk.END, values=("Metqi", bh["metqi"], "", ""))
        bh_table.insert("", tk.END, values=("Nineveh", bh["nineveh"], "", ""))
        bh_table.insert(
            "",
            tk.END,
            values=(
                "Evangelist",
                bh["evangelist"]["name"],
                "",
                f"Remainder: {bh['evangelist']['remainder']}",
            ),
        )

        # Movable Feasts
        for feast in bh["movableFeasts"].values():
            eth = feast["ethiopian"]
            greg = feast["gregorian"]

            bh_table.insert(
                "",
                tk.END,
                values=(
                    feast["name"],
                    f"{eth['month']}/{eth['day']}/{eth['year']}",
                    f"{greg.month}/{greg.day}/{greg.year}",
                    "Movable Feast",
                ),
            )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# =========================
# GUI SETUP
# =========================

root = tk.Tk()
root.title("Ethiopian Calendar & Bahire Hasab")
root.geometry("1200x800")
root.update_idletasks()
root.deiconify()
root.lift()
root.attributes("-topmost", True)
root.after(500, lambda: root.attributes("-topmost", False))

# =========================
# Ethiopian → Gregorian
# =========================

tk.Label(root, text="Ethiopian to Gregorian", font=("Arial", 14, "bold")).grid(
    row=0, column=0, columnspan=2, pady=10
)

tk.Label(root, text="Year").grid(row=1, column=0)
eth_year_entry = tk.Entry(root)
eth_year_entry.grid(row=1, column=1)

tk.Label(root, text="Month").grid(row=2, column=0)
eth_month_entry = tk.Entry(root)
eth_month_entry.grid(row=2, column=1)

tk.Label(root, text="Day").grid(row=3, column=0)
eth_day_entry = tk.Entry(root)
eth_day_entry.grid(row=3, column=1)

tk.Button(root, text="Convert", command=convert_eth_to_greg).grid(
    row=4, column=0, columnspan=2, pady=5
)

eth_result_label = tk.Label(root, text="")
eth_result_label.grid(row=5, column=0, columnspan=2)

greg_result_label = tk.Label(root, text="", font=("Arial", 10, "bold"))
greg_result_label.grid(row=6, column=0, columnspan=2)

# =========================
# Gregorian → Ethiopian
# =========================

tk.Label(root, text="Gregorian to Ethiopian", font=("Arial", 14, "bold")).grid(
    row=0, column=3, columnspan=2, pady=10
)

tk.Label(root, text="Year").grid(row=1, column=3)
greg_year_entry = tk.Entry(root)
greg_year_entry.grid(row=1, column=4)

tk.Label(root, text="Month").grid(row=2, column=3)
greg_month_entry = tk.Entry(root)
greg_month_entry.grid(row=2, column=4)

tk.Label(root, text="Day").grid(row=3, column=3)
greg_day_entry = tk.Entry(root)
greg_day_entry.grid(row=3, column=4)

tk.Button(root, text="Convert", command=convert_greg_to_eth).grid(
    row=4, column=3, columnspan=2, pady=5
)

greg_result_label2 = tk.Label(root, text="")
greg_result_label2.grid(row=5, column=3, columnspan=2)

eth_result_label2 = tk.Label(root, text="", font=("Arial", 10, "bold"))
eth_result_label2.grid(row=6, column=3, columnspan=2)

# =========================
# Bahire Hasab Table
# =========================

tk.Label(root, text="Bahire Hasab Calculator", font=("Arial", 14, "bold")).grid(
    row=8, column=0, columnspan=5, pady=10
)

tk.Label(root, text="Ethiopian Year").grid(row=9, column=0)
bh_year_entry = tk.Entry(root)
bh_year_entry.grid(row=9, column=1)

tk.Button(root, text="Calculate", command=calculate_bahire_hasab).grid(
    row=9, column=2, padx=10
)

columns = ("name", "ethiopian", "gregorian", "description")

bh_table = ttk.Treeview(root, columns=columns, show="headings", height=15)

bh_table.heading("name", text="Name")
bh_table.heading("ethiopian", text="Ethiopian Date")
bh_table.heading("gregorian", text="Gregorian Date")
bh_table.heading("description", text="Description")

bh_table.column("name", width=200)
bh_table.column("ethiopian", width=150)
bh_table.column("gregorian", width=150)
bh_table.column("description", width=300)

bh_table.grid(row=10, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

scrollbar = ttk.Scrollbar(root, orient="vertical", command=bh_table.yview)
bh_table.configure(yscroll=scrollbar.set)
scrollbar.grid(row=10, column=5, sticky="ns")

root.mainloop()
