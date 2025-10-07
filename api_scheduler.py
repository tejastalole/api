import time as t
from datetime import datetime, timedelta
import threading
import subprocess
import sys
from collections import defaultdict

# ---------- CONFIG ----------
from config import API_URL, LOG_FILE


# ---------- LOG + PRINT FUNCTION ----------
def log_and_print(message):
    """Print to console and immediately append to log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp}: {message}"
    print(line, flush=True)  # console
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
        f.flush()

# ---------- PARSE TIMESTAMPS ----------
def parse_timestamps(timestamps, suppress_print=False):
    """
    Parse a list of "HH:MM:SS" timestamps into datetime.time objects.
    If suppress_print=True, invalid timestamp warnings are suppressed.
    """
    parsed = []
    for timestamp in timestamps:
        try:
            parsed.append(datetime.strptime(timestamp, "%H:%M:%S").time())
        except ValueError:
            if not suppress_print:
                print(f"Invalid timestamp skipped: {timestamp}")
    return parsed

def group_by_time(parsed):
    grouped = defaultdict(list)
    for ts in parsed:
        grouped[ts].append(ts)
    return grouped

# ---------- WAIT ----------
def wait_until(target_time):
    now = datetime.now()
    target = now.replace(
        hour=target_time.hour,
        minute=target_time.minute,
        second=target_time.second,
        microsecond=0
    )
    if target < now:
        target += timedelta(days=1)
    time_to_wait = (target - now).total_seconds()
    if time_to_wait > 0:
        t.sleep(time_to_wait)

# ---------- CALL API ----------
def call_api():
    try:
        result = subprocess.run(["curl", "-s", API_URL], capture_output=True, text=True)
        if result.returncode == 0:
            log_and_print(f"Successfully called API at {API_URL}")
        else:
            log_and_print(f"Failed to call API (code {result.returncode}) at {API_URL}")
    except Exception as e:
        log_and_print(f"Error calling API: {e}")

# ---------- SCHEDULER ----------
def scheduler(timestamps_input):
    timestamps = parse_timestamps(timestamps_input)
    grouped_timestamps = group_by_time(timestamps)

    for ts, group in grouped_timestamps.items():
        wait_until(ts)
        threads = []
        for _ in group:
            thread = threading.Thread(target=call_api)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

# ---------- MAIN ----------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python scheduler.py "HH:MM:SS, HH:MM:SS, ..."')
        sys.exit(1)

    timestamps_input = [ts.strip() for ts in sys.argv[1].split(",") if ts.strip()]
    scheduler(timestamps_input)
