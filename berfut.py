import tkinter as tk

root = tk.Tk()
root.title("Loop Example")
root.geometry("300x250")

for i in range(5):
    btn = tk.Button(root, text=f"Button {i+1}")
    btn.pack(pady=5)

root.mainloop()
