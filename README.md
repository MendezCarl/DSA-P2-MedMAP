# Setting up Development Environment and Guide
This guide is to help new and current developers in getting started on contributing to MedMAP.

## Frontend Setup
```bash
cd frontend
npm install
```

## Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

# Naming Conventions

## Functions and Variables: Camel case
* Function name and variable should speak for it self
* ex: let counter = x


For git branch names we will be using kebab case.

Git Branches naming: location-feature/task-misc(if needed)
ex: backend-counterFunction

# Git
## Git advice
* Don't ever work on the main branch.
* When merging branch to main always pull main first.
* When writing a commit message be descripitived of what you did. Include what was done and where and what is left to do.
* Delete branches when feature/task is done and merged to main.