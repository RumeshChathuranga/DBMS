# 🚀 Quick Start - HRGSMS

## Prerequisites Check
- ✅ All dependencies installed
- ✅ Database setup completed
- ✅ Environment files configured

## Starting the Application

### 1. Start Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

python run.py
```

### 2. Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

## Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Default Login
- **Username**: `admin`
- **Password**: `admin123`

## Quick Commands

### Backend
```bash
# Start backend
cd backend && source venv/bin/activate && python run.py

# Check if backend is running
curl http://localhost:8000/health
```

### Frontend
```bash
# Start frontend
cd frontend && npm run dev

# Build for production
cd frontend && npm run build
```

### Troubleshooting
```bash
# Check if ports are free
netstat -an | findstr :8000  # Backend port
netstat -an | findstr :5173  # Frontend port

# Kill processes if needed
taskkill /f /im python.exe   # Windows
pkill -f python              # Linux/macOS
```

That's it! Your HRGSMS application should be running and accessible.



git

Step 1: Clone the original repository

If you haven’t already cloned it, do this:

git clone https://github.com/original-user/original-repo.git
cd original-repo


This will create a folder original-repo with all the code.

cd original-repo moves you into that folder.

Step 2: Make your changes

Open the project in your code editor.

Edit files as you want.

Stage and commit your changes:

git add .
git commit -m "My changes"


git add . → stages all your changes.

git commit -m "..." → saves them in a commit.

Step 3: Create a new repository on GitHub

Go to GitHub
 and log in.

Click New repository.

Name it (e.g., my-version-of-repo).

Don’t initialize with a README (since you already have code locally).

Click Create repository.

Step 4: Point your local repo to your new GitHub repo

Change the origin remote to your own repo:

git remote set-url origin https://github.com/your-username/my-version-of-repo.git






Check the remote to confirm:

git remote -v


It should show your GitHub repo URL for origin.

Step 5: Push your changes

Push your local branch (main) to GitHub:

git push -u origin main


The -u sets the upstream so next time you can just do git push.

✅ Your edits are now on your own GitHub repository.

If you want, I can also give a shortcut version of all these steps as a single command sequence, so you can do it in one go without mistakes.

Do you want me to do that?

You said:
i have already added the modifications and i have my own local we running. i need to add it to my git . give me step byy step
ChatGPT said:

Perfect! Since you already have your local repo with modifications, we can push it to your own GitHub repository step by step.

Step 1: Create a new repository on GitHub

Go to GitHub
 and log in.

Click + → New repository.

Give it a name (e.g., my-project).

Do NOT initialize with a README (you already have code locally).

Click Create repository.

After creation, GitHub will show you a URL for your repo, e.g.:

https://github.com/your-username/my-project.git

Step 2: Check your current remote

In your local project folder, run:

git remote -v


This shows which remote your local repo points to.

If it points to the original repo, we’ll change it to your GitHub repo.

Step 3: Set your GitHub repo as the origin

Replace your-username and my-project with your repository info:

git remote set-url origin https://github.com/your-username/my-project.git








Verify the change:

git remote -v


It should now show your GitHub repo URL for origin.

Step 4: Stage and commit your changes (if not done yet)
git add .
git commit -m "My modifications"


git add . → stages all modified files

git commit -m "..." → creates a commit

Step 5: Push to your GitHub repository
git push -u origin main


Replace main with your branch name if it’s different.

The -u sets the upstream, so future pushes can be done with just git push.

✅ Your local repo with modifications is now on your GitHub!

If you want, I can also give you a super short 5-command version to push any local repo to GitHub quickly.

Do you want me to do that?