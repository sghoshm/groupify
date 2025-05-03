# Architecture Overview

Groupify follows a microservice-oriented architecture leveraging free-tier cloud services.

## Components

- **Frontend:** Developed with **Flutter** for cross-platform compatibility (Web, Mobile, Desktop). Deployed to **Cloudflare Pages** (Web).
- **Backend:** Built with **FastAPI** (Python). Runs on an **Oracle Cloud Free Tier VM**. Handles API requests, business logic, and orchestrates interactions.
- **AI:** **Ollama** runs on the same **Oracle Cloud Free Tier VM** as the backend. Hosts and serves the Large Language Model (LLM).
- **Database, Authentication, Storage:** **Supabase Free Tier**. Provides a managed PostgreSQL database, user authentication, and file storage.
- **CI/CD:** **GitHub Actions** for automated build, test, and deployment.
- **Monitoring:** (Optional but recommended) **UptimeRobot Free Tier** to monitor service availability.

## Data Flow

1.  User interacts with the **Frontend**.
2.  **Frontend** makes API calls to the **Backend** (FastAPI).
3.  **Backend** interacts with **Supabase** for data persistence (messages, users) and authentication checks.
4.  For AI features, the **Backend** calls the **Ollama** API running on the same VM.
5.  **Ollama** processes the AI request and returns a response to the **Backend**.
6.  **Backend** sends the final response back to the **Frontend**.

## Deployment Strategy

- **Backend & AI:** Dockerized and deployed via `docker-compose` to an Oracle Cloud VM using SSH from GitHub Actions.
- **Frontend (Web):** Built as a static web application and deployed automatically to Cloudflare Pages via Git integration.
- **Frontend (Mobile/Desktop):** Built separately for distribution (e.g., app stores, direct downloads).

This architecture is designed to be cost-effective by utilizing free tiers while providing a scalable foundation for a real-world application.
