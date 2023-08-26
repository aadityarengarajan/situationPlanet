import time
import os
import sys
import smtplib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import messagebox

# Set your email configuration
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_email@example.com'
SMTP_PASSWORD = 'your_email_password'
SENDER_EMAIL = 'your_email@example.com'
RECIPIENT_EMAIL = 'recipient@example.com'

# Path to the log file you want to monitor
LOG_FILE_PATH = 'path_to_your_log_file.log'

class LogFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == LOG_FILE_PATH and event.event_type == 'modified':
            with open(LOG_FILE_PATH, 'r') as f:
                f.seek(0, os.SEEK_END)
                while True:
                    line = f.readline()
                    if not line:
                        break
                    process_log_entry(line)

def process_log_entry(entry):
    # Add your logic here to determine whether to show a dialogue box or send an email
    # For demonstration purposes, let's just show a dialogue box for any new entry
    show_dialogue_box(entry)

def show_dialogue_box(entry):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("New Log Entry", f"A new log entry has been added:\n\n{entry}")
    root.destroy()

def send_email(subject, message):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)

            email_text = f"Subject: {subject}\n\n{message}"
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, email_text)
    except Exception as e:
        print("Error sending email:", e)

if __name__ == "__main__":
    event_handler = LogFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(LOG_FILE_PATH), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
