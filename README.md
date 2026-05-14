# Smart Student Planner

A cross-platform mobile application built for the LDC6004M Mobile
Application Development module at York St John University. The app helps
students plan modules, manage coursework deadlines and revise on the go.

> Repository placeholder: `https://github.com/<your-username>/smart-student-planner`
> (replace before submission).

## Features

- Account registration, sign-in and sign-out with hashed passwords.
- Dashboard listing every task for the current user.
- Add, edit, delete, complete and search tasks.
- Local JSON persistence so data survives between sessions.
- Form validation with inline error messages.
- Responsive layout designed for portrait mobile devices.
- Settings screen with a sign-out action and a preference toggle.

## Project structure

```
SmartStudentPlanner/
├── main.py                  # Kivy app entry point
├── controllers/             # Auth and task business logic
├── models/                  # User and Task data classes
├── services/                # Local JSON storage service
├── utils/                   # Theme and validation helpers
├── views/                   # Kivy screens (login, dashboard, form, settings)
├── tests/                   # Unit and integration tests
├── screenshots/             # UI evidence images
├── docs/                    # Design diagrams (wireframes, flow, architecture)
├── requirements.txt
└── README.md
```

## Architecture

The project follows a Model-View-Controller (MVC) layout. Models hold the
data shape, the storage service provides persistence, controllers carry
the business rules, and Kivy screens form the view layer. The
``StorageService`` is the single source of truth for both authentication
and task data, which keeps the codebase predictable.

## Installation

1. Install Python 3.10 or newer.
2. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/smart-student-planner.git
   cd smart-student-planner/SmartStudentPlanner
   ```
3. (Recommended) Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate         # macOS / Linux
   venv\Scripts\activate            # Windows
   ```
4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## How to run

From inside the `SmartStudentPlanner` folder:

```bash
python main.py
```

The first run creates a JSON store at
``~/.smart_student_planner/storage.json``. Register an account, sign in,
and start adding tasks.

## Running the tests

```bash
python -m unittest discover -s tests -v
```

Seventeen tests cover validation rules, registration, login, the five
task operations from the brief and the search filter.

## Tools and frameworks used

| Tool | Version | Purpose |
| --- | --- | --- |
| Python | 3.10+ | Language |
| Kivy | 2.3.x | Cross-platform GUI framework |
| unittest | stdlib | Automated tests |
| Git / GitHub | latest | Version control |

## Known limitations

- The local JSON store is single-user-per-device; multi-device sync is
  not implemented.
- Passwords are hashed with SHA-256 for portability. A production app
  should use a salted, slow hash such as bcrypt or Argon2.
- The date field is a free-text input. A future iteration could replace
  it with a calendar picker widget.
- No notifications or background reminders are produced.

## Future enhancements

- Push notifications for upcoming deadlines.
- Cloud synchronisation via a small REST API.
- Dark theme that follows the operating-system preference.
- Calendar view in addition to the list view.
- Optional integration with the university timetable feed.

## Licence

This project was created for academic purposes for the LDC6004M module.
All third-party code is credited inline and in the reflective narrative.
