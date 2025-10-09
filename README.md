# API Scheduler in Python

A lightweight and efficient **API call scheduler** written in Python that executes API requests at specific times of the day. Supports multiple timestamps, parallel execution, and automatic logging of results.

---

##  Features

*  Schedule API calls at custom times (HH:MM:SS format).
*  Automatically groups identical timestamps to execute API calls **in parallel**.
*  Uses **multithreading** for simultaneous API requests.
*  Logs every API call (success or failure) with timestamps in a log file.
*  Automatically waits until the next scheduled time.
*  Handles invalid timestamps gracefully.

---

##  Project Structure

```
api-scheduler/
│
├── api_scheduler.py        # Main scheduler script
├── config.py           # Configuration file (API URL and log path)
├── test.log             # Log file (auto-created)
├── README.md           # Project documentation
└── test_api_scheduler.py    # Basic unit test



```

---

##  Setup Instructions


### 1. Create a `config.py` File

In the project folder, create a file named `config.py` and add the following:

```python
API_URL = "https://ifconfig.co"
LOG_FILE = "test.log"
```

### 2. Install Requirements

No external libraries are needed — only Python’s built-in modules are used.

> Works with **Python 3.0+**

---

##  How It Works

1. You pass one or more timestamps (HH:MM:SS) as input.
2. The scheduler parses them and waits until the next timestamp.
3. When time matches, it executes the **API call using `curl`**.
4. If multiple timestamps occur at the same second → all calls are made in **parallel threads**.
5. Each call is logged in the specified log file.

---

##  Usage

###  Run from Command Line

```bash
python api_scheduler.py "12:30:00, 14:15:30, 22:00:00"
```

### Example Output

```
2025-10-08 12:30:00: Successfully called API at https://ifconfig.co
2025-10-08 14:15:30: Successfully called API at https://ifconfig.co
2025-10-08 22:00:00: Successfully called API at https://ifconfig.co
```

Logs are automatically saved in `test.log`.

---

##  Example Workflow

| Step | Action                                                     |
| ---- | ---------------------------------------------------------- |
| 1    | User inputs timestamps like `12:00:00, 12:00:00, 13:00:00` |
| 2    | Script groups identical timestamps                         |
| 3    | Waits until 12:00:00                                       |
| 4    | Executes both 12:00:00 calls **in parallel**               |
| 5    | Waits for next (13:00:00)                                  |
| 6    | Logs all results                                           |

---

##  Example Log Output

```
2025-10-08 12:00:00: Successfully called API at https://ifconfig.co
2025-10-08 12:00:00: Successfully called API at https://ifconfig.co
2025-10-08 13:00:00: Successfully called API at https://ifconfig.co
```

---

##  Error Handling

* Invalid timestamps → skipped with a warning.
* API call failure → logged with exit code.
* Script crashes → prevented with try/except blocks.

---

