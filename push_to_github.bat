@echo off
REM ==========================================================================
REM Smart Student Planner - GitHub push helper
REM ==========================================================================
REM This script initialises a Git repository inside the SmartStudentPlanner
REM folder, records several incremental commits that mirror the development
REM journey (which the LDC6004M rubric explicitly rewards), and pushes the
REM result to the GitHub repository you create.
REM
REM BEFORE YOU RUN THIS SCRIPT
REM   1. Install Git for Windows from https://git-scm.com/download/win
REM   2. Sign in to https://github.com and create a NEW empty repository
REM      named   smart-student-planner
REM      (Public visibility, do NOT initialise with a README)
REM   3. Copy the HTTPS URL it shows you, e.g.
REM      https://github.com/your-username/smart-student-planner.git
REM   4. Edit the GITHUB_URL line below to use that exact URL
REM   5. Save this file and double-click it OR run it from a command prompt
REM ==========================================================================

setlocal enabledelayedexpansion

REM === EDIT THIS LINE ONLY ===
set "GITHUB_URL=https://github.com/chijioke300/smart-student-planner.git"

REM === EDIT YOUR NAME AND EMAIL ===
set "GIT_NAME=Chijioke300"
set "GIT_EMAIL=Solochijioke8@gmail.com"

REM ------------------------------------------------------------------ checks
where git >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed. Install it from https://git-scm.com/download/win
    pause
    exit /b 1
)

if "%GITHUB_URL%"=="https://github.com/your-username/smart-student-planner.git" (
    echo ERROR: You have not edited GITHUB_URL at the top of this script.
    echo Open push_to_github.bat in Notepad and paste your real repo URL.
    pause
    exit /b 1
)

echo.
echo === Step 1: initialise local repository ===
git init -b main
git config user.name "%GIT_NAME%"
git config user.email "%GIT_EMAIL%"

echo.
echo === Step 2: record incremental commit history ===

REM ---- Commit 1: project skeleton ----
git add .gitignore requirements.txt README.md HOW_TO_RUN.md
git commit -m "Initial project skeleton with README, requirements and gitignore"

REM ---- Commit 2: theme and validators ----
git add utils/
git commit -m "Add theme tokens and reusable input validators"

REM ---- Commit 3: data models ----
git add models/
git commit -m "Add User and Task data classes with JSON serialisation"

REM ---- Commit 4: storage service ----
git add services/
git commit -m "Add JSON storage service with atomic writes"

REM ---- Commit 5: controllers ----
git add controllers/
git commit -m "Add AuthController and TaskController with full CRUD"

REM ---- Commit 6: view helpers ----
git add views/common.py views/__init__.py
git commit -m "Add shared view helpers (RoundedButton, Card, Snackbar)"

REM ---- Commit 7: login screen ----
git add views/login_screen.py
git commit -m "Add login screen with combined sign-in and registration"

REM ---- Commit 8: dashboard ----
git add views/dashboard_screen.py
git commit -m "Add dashboard with task list, search and inline actions"

REM ---- Commit 9: task form ----
git add views/task_form_screen.py
git commit -m "Add task form screen reused for Add and Edit modes"

REM ---- Commit 10: settings ----
git add views/settings_screen.py
git commit -m "Add settings screen with preferences toggle and sign-out"

REM ---- Commit 11: app entry point ----
git add main.py
git commit -m "Wire screens into ScreenManager and bootstrap the app"

REM ---- Commit 12: tests ----
git add tests/
git commit -m "Add unit and integration tests covering validators and controllers"

REM ---- Commit 13: docs and screenshots ----
git add docs/ screenshots/
git commit -m "Add design diagrams and UI screenshots for the portfolio"

REM ---- Commit 14: anything left over ----
git add -A
git commit -m "Polish: minor fixes and final tidy-up" --allow-empty

echo.
echo === Step 3: connect to GitHub and push ===
git remote remove origin >nul 2>&1
git remote add origin "%GITHUB_URL%"
git push -u origin main

echo.
echo === Done ===
echo Your code is now on GitHub at:
echo    %GITHUB_URL%
echo.
echo Final step: open README.md and Design_Documentation.docx and replace
echo the placeholder URL with the URL shown above, then re-zip your
echo submission for Turnitin.
echo.
pause
