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

Session creation and listing now use PostgreSQL. Saved sessions survive
container recreation through a persistent database volume.

Automated tests are being updated to use an isolated PostgreSQL test
database; the previous in-memory test setup is not compatible with the
current endpoints.

## Run backend tests

With the project's Conda environment active, run from the project root:

    python -m pip install -r backend/requirements-dev.txt
    cd backend
    python -m pytest -v

Tests cover creation, listing, unique IDs, and rejection of invalid input.
Each test starts with empty in-memory storage.

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

## Run the API and PostgreSQL with Docker Compose

Requires Docker with its engine running.

On first setup, create local configuration:

    cp .env.example .env

Start the services:

    docker compose up --build -d

Check status and logs:

    docker compose ps
    docker compose logs api db

Stop and remove the containers:

    docker compose down

The named PostgreSQL volume is retained when running `docker compose down`.
Running `docker compose down -v` also deletes the database volume and its data.

The API currently stores sessions in memory. PostgreSQL is running but is
not yet connected to the application.

## Apply database migrations

With PostgreSQL running, execute from the project root:

    docker compose build api
    docker compose run --rm api python -m alembic upgrade head

Check the applied migration revision:

    docker compose run --rm api python -m alembic current

Apply migrations before starting application code that requires the new
database structure.