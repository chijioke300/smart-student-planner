# How to Run the Smart Student Planner

This is the practical mobile application portfolio for LDC6004M.
Follow the four steps below to launch the working app on your machine.

## 1. Install Python 3.10 or newer

- Windows: download from https://www.python.org/downloads/ and tick
  "Add Python to PATH" in the first installer screen.
- macOS: `brew install python` or download from the same URL.
- Linux: `sudo apt install python3 python3-pip`.

Verify the install:

```
python --version
```

## 2. Open a terminal in this folder

In Windows, hold Shift and right-click inside the `SmartStudentPlanner`
folder, then choose "Open PowerShell window here".

## 3. Install the single dependency

```
pip install kivy
```

(Optional but recommended) create a virtual environment first:

```
python -m venv venv
venv\Scripts\activate            # Windows
source venv/bin/activate         # macOS / Linux
pip install -r requirements.txt
```

## 4. Run the app

```
python main.py
```

A phone-sized window opens at 380 by 760 pixels. You will see the login
screen. Tap "Create account", register with any e-mail and password of
six or more characters, then tap "Sign in".

## What to try

| Feature | How to test it |
| --- | --- |
| Add task | Tap the orange "+ Add new task" button |
| Edit task | Tap "Edit" on any task card |
| Delete task | Tap "Delete" on any task card |
| Mark complete | Tick the checkbox next to a task |
| Search | Start typing in the search box on the dashboard |
| Settings | Tap "Settings" in the dashboard header |
| Sign out | Tap the red "Sign out" button inside Settings |

## Run the automated tests (no Kivy required)

```
python -m unittest discover -s tests -v
```

Expected output:

```
Ran 17 tests in 0.05s
OK
```

## Where is data stored?

The local JSON store lives at
`~/.smart_student_planner/storage.json` (i.e. inside your home
directory). Deleting that file resets the app.

## Trouble shooting

- "kivy not found" -> rerun `pip install kivy`.
- The window appears blank on a very old machine -> Kivy needs OpenGL
  2.0; update the graphics driver.
- Tests fail with an import error -> confirm you are running them from
  the `SmartStudentPlanner` folder, not from inside `tests/`.

## Project structure (for the marker)

```
SmartStudentPlanner/
├── main.py                  # Kivy entry point - START HERE
├── controllers/             # AuthController, TaskController
├── models/                  # User and Task data classes
├── services/                # JSON storage service
├── utils/                   # Theme and validation helpers
├── views/                   # Kivy screens (login, dashboard, form, settings)
├── tests/                   # 17 unit and integration tests
├── screenshots/             # UI evidence (PNG)
├── docs/                    # Wireframes, navigation flow, architecture
├── requirements.txt
└── README.md
```
