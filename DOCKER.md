# Run the complete application with Docker

## Prerequisites

Install and start Docker Desktop. The first start needs Internet access to
download the Docker images, the Ollama model, and the embedding model. After
they are downloaded, Docker reuses the local volumes on later starts.

## Start everything

From the project root:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

The first run can take several minutes because the AI model and Python
dependencies are large. Wait until the `backend` service is healthy, then open:

```text
http://localhost:5173
```

This is the only address students need. The React frontend forwards chat and
book-upload requests internally to the FastAPI backend.

To use the system from another device on the same network, open this address
on that device, replacing `YOUR-COMPUTER-IP` with the IP address of the
computer running Docker:

```text
http://YOUR-COMPUTER-IP:5173
```

Allow Docker Desktop through the host firewall if the other device cannot
connect.

## Books and persistence

- Copy teacher textbooks into `backend/Books/`, including subfolders. The
  backend detects new or changed PDFs automatically.
- Books uploaded through Settings are stored in `backend/Books/uploads/`.
- The PDF folder is mounted from the computer, so it remains after containers
  stop or are rebuilt.
- The vector index, embedding model, and Ollama model are retained in named
  Docker volumes.

## Useful commands

```powershell
# Start after the first build
docker compose up

# Run in the background
docker compose up -d

# Inspect services and logs
docker compose ps
docker compose logs -f backend

# Stop containers without deleting books, models, or index data
docker compose down
```

Do not run `docker compose down -v` unless you intentionally want to delete
the downloaded AI models, embedding cache, and indexed library. Your PDFs in
`backend/Books/` are kept because they are stored on the host computer.
