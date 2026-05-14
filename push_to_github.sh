#!/usr/bin/env bash
# Smart Student Planner - GitHub push helper (macOS / Linux).
# See push_to_github.bat for the Windows version.

set -e

# === EDIT THESE ===
GITHUB_URL="https://github.com/your-username/smart-student-planner.git"
GIT_NAME="Your Full Name"
GIT_EMAIL="your-yorksj-email@yorksj.ac.uk"
# ==================

if ! command -v git >/dev/null 2>&1; then
  echo "Git is not installed. Install with: brew install git (macOS) or sudo apt install git (Linux)"
  exit 1
fi

if [[ "$GITHUB_URL" == "https://github.com/your-username/smart-student-planner.git" ]]; then
  echo "Please edit GITHUB_URL at the top of this script before running it."
  exit 1
fi

git init -b main
git config user.name "$GIT_NAME"
git config user.email "$GIT_EMAIL"

git add .gitignore requirements.txt README.md HOW_TO_RUN.md
git commit -m "Initial project skeleton with README, requirements and gitignore"

git add utils/
git commit -m "Add theme tokens and reusable input validators"

git add models/
git commit -m "Add User and Task data classes with JSON serialisation"

git add services/
git commit -m "Add JSON storage service with atomic writes"

git add controllers/
git commit -m "Add AuthController and TaskController with full CRUD"

git add views/common.py views/__init__.py
git commit -m "Add shared view helpers (RoundedButton, Card, Snackbar)"

git add views/login_screen.py
git commit -m "Add login screen with combined sign-in and registration"

git add views/dashboard_screen.py
git commit -m "Add dashboard with task list, search and inline actions"

git add views/task_form_screen.py
git commit -m "Add task form screen reused for Add and Edit modes"

git add views/settings_screen.py
git commit -m "Add settings screen with preferences toggle and sign-out"

git add main.py
git commit -m "Wire screens into ScreenManager and bootstrap the app"

git add tests/
git commit -m "Add unit and integration tests covering validators and controllers"

git add docs/ screenshots/
git commit -m "Add design diagrams and UI screenshots for the portfolio"

git add -A
git commit -m "Polish: minor fixes and final tidy-up" --allow-empty

git remote remove origin >/dev/null 2>&1 || true
git remote add origin "$GITHUB_URL"
git push -u origin main

echo
echo "Code is live at $GITHUB_URL"
echo "Now replace the placeholder URL in README.md and Design_Documentation.docx."
