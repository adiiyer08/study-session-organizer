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

The API supports health checks and creating and listing study sessions.
Creation validates text fields, timezone-aware future start times, and
capacity limits.

Sessions are temporarily stored in process memory and are lost when the
server restarts. Storage is not shared between server processes.

Frontend, persistent database storage, authentication, and public deployment
are planned. Docker packaging is available.

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

## Run the backend with Docker

Requires Docker with its engine running.

From the project root, build the image:

    docker build -t study-session-api:dev ./backend

Run the container:

    docker run --rm --name study-session-api -p 127.0.0.1:8000:8000 study-session-api:dev

Open http://127.0.0.1:8000/health or http://127.0.0.1:8000/docs.

Stop the container with Control+C.
Rebuild the image after changing application code or dependencies.