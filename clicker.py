import tkinter as tk
import threading
import pyautogui
import keyboard
import time

class AutoClicker:
    def __init__(self):
        self.running = False
        self.delay_ms = 100
        self.button = "left"
        self.click_count = 0
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.click_count = 0
            self.thread = threading.Thread(target=self.click_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False

    def click_loop(self):
        for i in range(3, 0, -1):
            countdown_var.set(f"Starting in {i}...")
            time.sleep(1)

        countdown_var.set("")
        status_var.set("Clicking...")

        # Hide the main window
        root.withdraw()

        while self.running:
            pyautogui.click(button=self.button)
            self.click_count += 1
            click_count_var.set(f"Clicks: {self.click_count}")
            time.sleep(self.delay_ms / 1000.0)

        status_var.set("Stopped.")
        root.deiconify()  # Show main window again

clicker = AutoClicker()

def update_settings():
    try:
        clicker.delay_ms = int(delay_entry.get())
    except ValueError:
        pass  # Ignore bad input

def on_hotkey_toggle():
    if clicker.running:
        clicker.stop()
    else:
        update_settings()
        clicker.start()

def toggle_mouse_button():
    current = clicker.button
    clicker.button = "right" if current == "left" else "left"
    button_toggle.config(text=f"Mouse: {clicker.button.capitalize()}")

def on_close():
    clicker.stop()
    root.destroy()

keyboard.add_hotkey("F6", on_hotkey_toggle)

# === Main Window ===
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("300x180+100+100")
root.configure(bg="#1e1e1e")
root.protocol("WM_DELETE_WINDOW", on_close)

# === HUD Variables === (must be after root is created)
click_count_var = tk.StringVar(value="Clicks: 0")
status_var = tk.StringVar(value="Status: Idle")
countdown_var = tk.StringVar(value="")

# === GUI Layout ===
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(padx=15, pady=15)

tk.Label(frame, text="Click Delay (ms)", fg="white", bg="#1e1e1e", font=("Segoe UI", 10)).pack(anchor="w")
delay_entry = tk.Entry(frame, bg="#2e2e2e", fg="white", insertbackground="white", font=("Segoe UI", 10))
delay_entry.insert(0, "100")
delay_entry.pack(fill="x", pady=(0, 10))

button_toggle = tk.Button(
    frame, text="Mouse: Left", font=("Segoe UI", 10),
    bg="#333333", fg="white", activebackground="#444", activeforeground="white",
    command=toggle_mouse_button
)
button_toggle.pack(fill="x", pady=(0, 10))

tk.Label(frame, text="Press F6 to Start/Stop", fg="gray", bg="#1e1e1e", font=("Segoe UI", 9)).pack()

# === HUD Overlay ===
hud = tk.Toplevel(root)
hud.title("Clicker HUD")
hud.geometry("200x100+10+10")
hud.overrideredirect(True)
hud.attributes("-topmost", True)
hud.attributes("-alpha", 0.75)
hud.configure(bg="black")

tk.Label(hud, textvariable=click_count_var, fg="white", bg="black", font=("Segoe UI", 10, "bold")).pack(pady=2)
tk.Label(hud, textvariable=status_var, fg="white", bg="black", font=("Segoe UI", 10)).pack(pady=2)
tk.Label(hud, textvariable=countdown_var, fg="cyan", bg="black", font=("Segoe UI", 10)).pack(pady=2)

# === Start App ===
root.mainloop()
