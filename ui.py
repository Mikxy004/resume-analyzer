# ui.py – Tkinter Desktop App
import tkinter as tk
from tkinter import  filedialog, messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import requests
import time
import os

resume_text = None

last_result = {}

def show_splash():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.configure(bg="white")

    width, height = 420, 220
    screen_w = splash.winfo_screenwidth()
    screen_h = splash.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    splash.geometry(f"{width}x{height}+{x}+{y}")

    title = tk.Label(
        splash,
        text="AR-NALYZER",
        font=("Segoe UI", 20, "bold"),
        bg="white"
    )
    title.pack(pady=50)

    subtitle = tk.Label(
        splash,
        text="AI-Powered Resume Intelligence",
        font=("Segoe UI", 11),
        fg="gray",
        bg="white"
    )
    subtitle.pack()

    splash.update()
    time.sleep(2)
    splash.destroy()


def upload_and_analyze():
    global resume_text

    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")]
    )

    if not file_path:
        return

    try:

        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                files=files,
                timeout=30
            )

        if response.status_code != 200:
            messagebox.showerror(
                "API Error",
                f"API returned {response.status_code}"
            )
            return

        data = response.json()

        resume_text = data.get("resume_text", "")
        score_label.config(
            text=f"Resume Score: {data.get('score', '--')}"
        )

        result_box.delete("1.0", tk.END)
        result_box.insert(
            tk.END,
            data.get("analysis", "No analysis returned")
        )

    except Exception as e:
       messagebox.showerror("Error", str(e))


def show_full_resume():
    global resume_text

    if not resume_text:
       messagebox.showerror("Error", "No resume loaded")
       return

    text_window = tk.Toplevel(root)
    text_window.title("Full Resume")

    text_area = tk.Text(text_window, wrap="word")
    text_area.pack(expand=True, fill="both")

    text_area.insert("1.0", resume_text)


def animate_thinking():
    for _ in range(6):
        for dots in ["", ".", "..", "..."]:
            status_label.config(text=f"🤖 Thinking{dots}")
            time.sleep(3)


# --- UI Layout ---

root = tk.Tk()
root.withdraw()
show_splash()
root.deiconify()
root.iconphoto(False, tk.PhotoImage(file="assets/ar-nalyzer.png"))
root.title("AR-NALYZER - Resume Analyzer")
root.geometry("900x650")
root.configure(bg="#f7f9fc")

# Global storage
resume_text = None
output_text = None


header = tk.Label(
    root,
    text="Smart Resume Analysis Using Artificial Intelligence",
    font=("Segoe UI", 22, "bold"),
    bg="#f7f9fc"
)
header.pack(pady=15)

upload_button = tk.Button(
   root,
   text="Upload Resume",
   command=upload_and_analyze
)
upload_button.pack(pady=5)

score_label = tk.Label(
   root,
   text="Resume Score: --",
   font=("Segoe UI", 11, "bold"),
   bg="#f7f9fc"
)
score_label.pack(pady=5)

score_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=400,
    mode="determinate",
    maximum=100
)
score_bar.pack(pady=5)

status_label = tk.Label(
    root,
    text="Waiting for resume...",
    font=("Segoe UI", 10),
    fg="gray",
    bg="#f7f9fc"
)
status_label.pack(pady=5)

result_box = ScrolledText(
    root,
    width=90,
    height=20,
    font=("Consolas", 10),
    bg="white",
    relief="flat"
)
result_box.pack(padx=20, pady=15)

show_button = tk.Button(
    root,
    text="Show Full Resume",
    command=show_full_resume
)
show_button.pack(pady=10)

root.mainloop()
