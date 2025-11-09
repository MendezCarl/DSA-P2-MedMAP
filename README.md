# What is MedMap
MedMap is a service to help individual find the right medical facility for their needs. It does this by using publicly avaliable data from the US government and OpenStreetMap.

# Setting up Development Environment and Guide
This guide is to help new and current developers in getting started on contributing to MedMAP.

## Frontend Setup
```bash
cd frontend
npm install
```

## Backend Setup
We recommend using a python environment to run the backend server. Use Python version 3.12.8. 
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

# Git Advice
* Don't ever work on the main branch.
* When merging branch to main always pull main first.
* When writing a commit message be descripitived of what you did. Include what was done and where and what is left to do.
* Delete branches when feature/task is done and merged to main.

# How to Run the code
You need to run two different terminals to run the backend and frontend server

First terminal window for backend.
```bash
cd backend
uvicorn backend.main:app --reload
```

Second terminal window for frontend.
```bash
cd frontend
npm run dev
```

Now you should click on the local host link seen on the frontend terminal window to access the webpage we coded.