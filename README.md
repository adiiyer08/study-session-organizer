# Study Session Organizer

A full-stack application for creating and joining study sessions.

## Planned features

- Create sessions with a course, time, location, and participant limit.
- Browse and filter upcoming sessions.
- Join or leave sessions.
- Allow organizers to edit or cancel their sessions.
- Prevent registrations beyond a session's capacity.

## Planned architecture

- Frontend: React and TypeScript
- Backend: Python and FastAPI
- Database: PostgreSQL
- Local services: Docker Compose

## Current status

The backend provides a working GET /health endpoint.
Frontend, database, authentication, and containerization are planned.

## Run the backend locally

Create the environment once:

    conda create --name study-session-organizer python=3.12 pip

From the project root, activate the environment and install dependencies:

    conda activate study-session-organizer
    python -m pip install -r backend/requirements.txt

Start the development server:

    cd backend
    python -m uvicorn app.main:app --reload

Health endpoint: http://127.0.0.1:8000/health
Interactive API documentation: http://127.0.0.1:8000/docs