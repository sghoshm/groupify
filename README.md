## The Goal of Groupify

The primary goal of the "Groupify" project, as designed, is to serve as a **turnkey, zero-cost blueprint and functional example of a modern, feature-rich (WhatsApp-style chat with AI) web, mobile, and desktop application fully deployable using *only* the free tiers of widely available cloud services and open-source technologies.**

It aims to demonstrate that:
1.  **Complex applications are achievable without upfront infrastructure costs:** By strategically combining free offerings (Oracle Cloud VMs, Supabase, Cloudflare Pages, GitHub Actions), developers can build and launch production-ready applications.
2.  **Open source fuels innovation:** Leveraging open-source components like FastAPI, Flutter, and Ollama provides powerful building blocks without licensing fees.
3.  **A complete development lifecycle is possible on free tiers:** From CI/CD and hosting to database, storage, authentication, and even integrated AI, the entire stack can be managed within generous free limits for initial development, prototyping, or projects with modest scale.

Groupify isn't just about building a chat app; it's about proving the viability of a cost-effective, end-to-end development and deployment strategy using the "always free" resources available today.

## Advanced Directory Structure Explanation

This directory structure is organized to cleanly separate concerns across different services (backend, frontend, AI) and aspects of the project life cycle (CI/CD, documentation, configuration, testing). It follows common conventions for Python/FastAPI and Flutter projects while integrating the necessary infrastructure definitions (Docker, Docker Compose).

Here is a detailed breakdown:

```
groupify/
├── .github/                      # Contains configurations specific to GitHub, primarily for automated workflows.
│   └── workflows/                # Stores GitHub Actions workflow files.
│       ├── ci.yml                # The core workflow for Continuous Integration and Deployment.
│       │                         #   Purpose: Automates building, testing (optional, but recommended), and deployment of the backend.
│       │                         #   Contents: Defines jobs that run on specific events (e.g., push to main). Includes steps to checkout code,
│       │                         #             build the backend Docker image, and use SSH to deploy/update containers on the Oracle VM.
│       │                         #             Leverages GitHub Actions' free minutes.
│       └── (Optional) frontend_deploy.yml # An optional, separate workflow for automating the Flutter Web deployment.
│                                 #   Purpose: Isolates the frontend web build and deployment process.
│                                 #   Contents: Defines a job triggered by pushes to the frontend codebase or a specific branch.
│                                 #             Builds the Flutter web app (`flutter build web`).
│                                 #             Might trigger deployment via Cloudflare Pages' API or by pushing the `build/web` content
│                                 #             to a Git branch monitored by Cloudflare Pages.
│
├── ai/                           # Encapsulates configuration and resources specifically for the AI (Ollama) service.
│   ├── docker-compose.yml        # Docker Compose file to define and manage the Ollama container.
│   │                         #   Purpose: Defines the `ollama` service, specifying the Docker image (`ollama/ollama`), port mappings (e.g., 11434),
│   │                         #             and crucial volume mounts.
│   │                         #   Contents: YAML definition including service name, image, ports, and a volume definition to persist
│   │                         #             Ollama's data (downloaded models, configurations) outside the container lifecycle, ensuring models aren't
│   │                         #             re-downloaded on container restarts.
│   └── models/                   # Directory potentially used for custom AI model files or Modelfiles.
│       └── llama-2/              # A placeholder subdirectory indicating where model-specific files might reside if needed for import or customization.
│                                 #   Purpose: While Ollama typically manages models via its CLI (`ollama pull`), this directory allows for storing
│                                 #             custom `Modelfiles` or local model weights (`ollama import`) if deviating from standard pulled models.
│                                 #   Contents: Custom `Modelfile` definitions, or local model files depending on the specific use case.
│
├── backend/                      # Contains all code and configurations for the FastAPI application.
│   ├── Dockerfile                # Defines how to build the Docker image for the backend service.
│   │                         #   Purpose: Packages the Python application and its dependencies into a portable container.
│   │                         #   Contents: Instructions for setting up the environment (Python version), installing dependencies from `requirements.txt`,
│   │                         #             copying the application code (`app/`), setting environment variables, exposing the application port,
│   │                         #             and defining the command to start the application (e.g., `uvicorn`).
│   ├── requirements.txt          # Lists all Python packages required by the backend application.
│   │                         #   Purpose: Ensures all necessary libraries (FastAPI, Supabase client, Requests, Pydantic, etc.) are installed.
│   │                         #   Contents: A simple list of package names and their versions (e.g., `fastapi==0.104.1`, `supabase-py==2.0.0`).
│   ├── docker-compose.yml        # Docker Compose file specifically for the backend service.
│   │                         #   Purpose: Defines the `backend` service, its build context (the current directory), port mapping, and
│   │                         #             configures essential environment variables required by the application (Supabase credentials,
│   │                         #             Ollama endpoint). It likely depends on or connects to the `ollama` service defined elsewhere (e.g., in `ai/docker-compose.yml`)
│   │                         #             using Docker networking.
│   │                         #   Contents: YAML definition including `build: .`, `ports:`, `environment:`, and potentially `depends_on:` or network configurations
│   │                         #             to reach the Ollama service.
│   └── app/                      # The core Python package for the backend application.
│       ├── main.py               # The main entry point for the FastAPI application instance.
│       │                         #   Purpose: Creates the main `FastAPI` app object, includes all sub-routers (from `api/v1/api.py`),
│       │                         #             configures global middleware (like CORS), and sets up application lifespan events (startup/shutdown logic).
│       │                         #   Contents: FastAPI app initialization and configuration code.
│       ├── api/                  # Contains API versioning.
│       │   └── v1/               # Specific version directory (Version 1).
│       │       ├── api.py        # The main router for API version 1.
│       │       │                         #   Purpose: Acts as an aggregate router, collecting and including all specific endpoint routers
│       │       │                         #             (from `endpoints/`). This simplifies adding new endpoint groups.
│       │       │                         #   Contents: `APIRouter` instance creation and `include_router` calls for `auth`, `users`, `chat` routers.
│       │       └── endpoints/    # Contains the actual implementation of API endpoints.
│       │           ├── auth.py   # FastAPI router and endpoint functions for authentication.
│       │           │                         #   Purpose: Handles user registration (`POST /register`), login (`POST /login`), and potentially logout.
│       │           │                         #             Interacts with `utils/supabase_client.py` for Supabase Auth operations.
│       │           │                         #             Uses schemas from `schemas/auth.py` for request body validation and response formatting.
│           │           ├── users.py  # FastAPI router and endpoint functions for user profiles.
│           │           │                         #   Purpose: Handles fetching (`GET /me`, `GET /{user_id}`) and updating (`PUT /me`) user profile data.
│           │           │                         #             Interacts with `utils/supabase_client.py` for database operations on the 'profiles' table.
│           │           │                         #             Uses schemas from `schemas/users.py`. Requires authentication (dependency on `utils/dependencies.py`).
│           │           └── chat.py   # FastAPI router and endpoint functions for chat messages and AI interaction.
│           │                         #   Purpose: Handles sending messages (`POST /send`), fetching chat history (`GET /messages`), and potentially triggering AI responses (`POST /chat/ai`).
│           │                         #             Interacts with `utils/supabase_client.py` for message storage and `utils/ollama_client.py` for AI calls.
│           │                         #             Uses schemas from `schemas/chat.py`. Requires authentication.
│       ├── core/                 # Contains core application configuration and base components.
│       │   ├── config.py         # Defines application settings loaded from environment variables.
│       │   │                         #   Purpose: Provides a centralized way to access configuration parameters (Supabase, Ollama URLs/Keys) throughout the application.
│       │   │                         #   Contents: A class (e.g., `Settings`) that reads values from environment variables, often with default values for local development.
│       │   └── (Optional) constants.py # Defines application-wide constants (e.g., max message length, default page size).
│       ├── utils/                # Houses reusable utility functions, clients, and helpers.
│       │   ├── supabase_client.py# Initializes and provides a configured Supabase client instance.
│       │   │                         #   Purpose: Centralizes Supabase client creation, making it easy to use across different parts of the application (endpoints, services).
│       │   │                         #   Contents: Code to create and potentially memoize the Supabase client object using credentials from `core/config.py`. Might include basic error handling wrappers.
│       │   └── ollama_client.py  # Initializes and provides a client for interacting with the Ollama AI service.
│       │                         #   Purpose: Abstract the communication with the Oll Ollama API (`http://ollama:11434` if running in Docker).
│       │                         #   Contents: A class or functions that handle sending prompts to Ollama's API and parsing responses, using the endpoint from `core/config.py`.
│       │   └── (Optional) dependencies.py # FastAPI dependency injection functions.
│       │                         #   Purpose: Provides common logic required by multiple endpoints, e.g., authenticating a user from a token (`get_current_user`).
│       │   └── (Optional) error_handlers.py # Custom exception handlers for FastAPI.
│       │                         #   Purpose: Define how specific exceptions (e.g., `Unauthorized`, `NotFound`) are translated into standard HTTP responses.
│       ├── (Optional) schemas/   # Contains Pydantic models used for data validation, serialization, and OpenAPI documentation.
│       │                         #   Purpose: Defines the expected structure of request bodies, response payloads, and data models used internally.
│       │   ├── auth.py           # Pydantic models for authentication (e.g., `LoginRequest`, `RegisterRequest`, `TokenResponse`).
│       │   ├── users.py          # Pydantic models for user data (e.g., `UserProfile`, `UpdateUserProfile`).
│       │   └── chat.py           # Pydantic models for chat data (e.g., `Message`, `SendMessageRequest`, `AIResponse`).
│       ├── (Optional) services/  # Implements the business logic, abstracting interactions with clients (Supabase, Ollama) from endpoints.
│       │                         #   Purpose: Promotes separation of concerns, makes logic reusable and easier to test independently from API routing.
│       │   ├── auth_service.py   # Business logic for authentication flows.
│       │   ├── user_service.py   # Business logic for managing users.
│       │   └── chat_service.py   # Business logic for handling messages and AI interactions.
│       └── (Optional) tests/         # Directory for backend tests (unit, integration, API tests).
│           ├── conftest.py           # Configuration file for Pytest, including fixtures (e.g., test client, mock dependencies).
│           ├── api/                  # Tests specifically for the API endpoints (e.g., testing HTTP status codes, request/response formats).
│           ├── unit/                 # Unit tests for smaller components (utilities, service methods).
│           └── integration/          # Integration tests for interactions between multiple components (e.g., service calling client).
│
├── frontend/                     # Contains the source code and project files for the Flutter application.
│   ├── pubspec.yaml              # Specifies the project's dependencies (packages), metadata, and assets.
│   │                         #   Purpose: Manages external libraries (e.g., Supabase Flutter, HTTP client, state management packages) and application configuration.
│   ├── pubspec.lock              # Records the exact versions of all dependencies used.
│   │                         #   Purpose: Ensures consistent builds across different environments.
│   ├── analysis_options.yaml     # Configures static analysis for Dart code (linter rules).
│   │                         #   Purpose: Helps maintain code quality and consistency.
│   ├── .gitignore                # Git ignore file tailored for Flutter projects.
│   │                         #   Purpose: Excludes build artifacts, platform-specific generated files, dependency caches, etc., from version control.
│   ├── lib/                      # Contains the primary Dart source code for the application.
│   │   ├── main.dart             # The main entry point for the Flutter application (`void main()`).
│   │   │                         #   Purpose: Initializes the app, runs the main widget (`GroupifyApp`).
│   │   ├── groupify_app.dart     # The root widget of the application (e.g., `MaterialApp`).
│   │   │                         #   Purpose: Configures global theme, routing, and potentially top-level providers for state management.
│   │   ├── screens/              # Contains widgets that represent entire screens or pages in the application UI.
│   │   │   ├── auth/             # Widgets for authentication flow (LoginScreen, RegisterScreen).
│   │   │   ├── chat/             # Widgets for chat interfaces (ChatListScreen, ChatScreen).
│   │   │   └── settings/         # Widgets for user settings and profile management.
│   │   ├── widgets/              # Contains reusable, smaller UI components used across different screens.
│   │   │                         #   Purpose: Promotes modularity and consistency in the UI.
│   │   │   ├── chat_bubble.dart  # Widget to display a single chat message visually.
│   │   │   ├── user_avatar.dart  # Widget to display a user's profile picture.
│   │   │   └── (e.g.) custom_text_field.dart, primary_button.dart
│   │   ├── services/             # Implements application-level logic, often interacting with external resources (API, Supabase).
│   │   │                         #   Purpose: Separates business logic and data fetching from UI widgets.
│   │   │   ├── api_service.dart  # Handles communication with the custom FastAPI backend API (using `http` or `dio` package).
│   │   │   ├── auth_service.dart # Manages user authentication state and interacts with Supabase Auth via the Supabase Flutter client.
│   │   │   └── chat_service.dart # Handles fetching and sending chat messages, potentially calling the API for AI interactions.
│   │   ├── models/               # Defines Dart classes that represent the data structures used in the application.
│   │   │                         #   Purpose: Provides a type-safe way to handle data fetched from the backend or Supabase (e.g., User, Message objects). Often includes `fromJson`/`toJson` methods or uses code generation like `json_serializable`.
│   │   │   ├── user.dart         # Data model for a user profile.
│   │   │   └── message.dart      # Data model for a chat message.
│   │   ├── utils/                # Contains utility functions, constants, and helpers not tied to specific UI or services.
│   │   │   ├── constants.dart    # Application-wide constants (e.g., API base URL, default values).
│   │   │   └── date_utils.dart   # Helpers for formatting dates and times.
│   │   ├── state/                # Implements the chosen state management pattern (Provider, Riverpod, BLoC, GetX, etc.).
│   │   │                         #   Purpose: Manages the application's state (e.g., currently logged-in user, list of chat messages) and notifies UI widgets of changes. The structure varies significantly based on the chosen pattern.
│   │   │   ├── auth_state.dart   # Example: A ChangeNotifer or Riverpod Provider managing the authentication status.
│   │   │   └── chat_provider.dart# Example: A BLoC or Provider managing chat data for a specific screen or the whole app.
│   │   └── (Optional) routes/    # Centralized definitions and management for application navigation routes.
│   ├── assets/                   # Contains static assets like images, fonts, and localization files.
│   │   ├── images/               # Image files used in the UI.
│   │   ├── fonts/                # Custom font files.
│   │   └── l10n/                 # Localization files if using Flutter's internationalization system (`.arb` files).
│   ├── test/                     # Contains unit and widget tests for the Dart code.
│   │   ├── widget_test.dart      # An example widget test file.
│   │   └── lib/                  # Mirrors the structure of `lib/` for organizing test files (`*_test.dart`).
│   ├── integration_test/         # Contains integration tests for testing application flows end-to-end.
│   │   └── app_test.dart         # An example integration test file.
│   ├── android/                  # Contains the native Android project files.
│   ├── ios/                      # Contains the native iOS project files.
│   ├── linux/                    # Contains the native Linux desktop project files.
│   ├── macos/                    # Contains the native macOS desktop project files.
│   ├── windows/                  # Contains the native Windows desktop project files.
│   ├── web/                      # Contains files specific to the Flutter web build.
│   │   ├── index.html            # The main HTML file that hosts the Flutter web app.
│   │   │                         #   Purpose: The entry point for the browser. Includes the necessary scripts to load the Flutter app.
│   │   ├── manifest.json         # Web app manifest for Add to Home Screen functionality.
│   │   └── (e.g.) favicon.png, icons/ # Icons and other web-specific assets.
│   └── build/                    # This directory is automatically generated by `flutter build` and contains compiled artifacts.
│                                 #   Purpose: Stores the ready-to-deploy output for each platform (web, apk, ipa, executables).
│                                 #   Note: This directory should *always* be gitignored.
│
├── docs/                         # Directory for project documentation.
│   ├── architecture.md           # Explains the overall system architecture, how components interact, and the technology stack.
│   ├── setup.md                  # Detailed instructions for setting up the development environment and deploying the application.
│   └── api/                      # Documentation related to the backend API.
│       └── openapi.json          # The generated OpenAPI (Swagger) specification file from FastAPI.
│                                 #   Purpose: Provides interactive API documentation via Swagger UI (`/docs` endpoint in FastAPI) and can be used by clients to generate code.
│
├── .env.example                  # An example file listing all required environment variables.
│                                 #   Purpose: Helps developers understand what configuration is needed and provides a template.
│                                 #   Contents: Key=VALUE placeholders (e.g., `SUPABASE_URL=`, `SUPABASE_KEY=`, `OLLAMA_ENDPOINT=`). Actual values should be in a separate `.env` file that is gitignored.
│
├── .gitignore                    # Root-level Git ignore file.
│                                 #   Purpose: Specifies files and directories that Git should ignore across the entire project (e.g., `.env` files, build directories, OS-specific files, IDE files).
│
├── LICENSE                       # Contains the chosen open-source license for the project.
│                                 #   Purpose: Defines how others can use, modify, and distribute your code. Essential for open-source projects.
│
└── README.md                     # The main project README file.
                                  #   Purpose: Provides a high-level overview of the project, its goals, features, setup instructions, and links to more detailed documentation. It's the first file someone sees when looking at the repository.
```

## How Groupify is Deployable (End-to-End Zero-Cost Pipeline)

The deployability of Groupify relies on orchestrating deployments across multiple free-tier services, triggered by code changes and managed infrastructure.

Here's the step-by-step deployment process for each component:

1.  **Core Infrastructure Provisioning (Manual - One Time):**
    * **Oracle Cloud Free Tier:** Sign up and provision **two Always Free Compute Instances**. Choose a suitable shape (Ampere ARM or AMD E-series, 1 OCPU, 1 GB RAM). Note their public IP addresses. Configure the **Virtual Cloud Network (VCN) Security List or Network Security Group (NSG)** associated with these VMs to open necessary ingress ports:
        * `22` (SSH) - For deployment via GitHub Actions and administration.
        * `80`, `443` (HTTP/HTTPS) - If running a reverse proxy (like Nginx/Caddy) on the VM to route traffic to your backend or potentially serve static files (though Cloudflare Pages handles web serving).
        * `8000` (Backend FastAPI) - Direct access to the backend API (useful for testing, or if not using a reverse proxy).
        * `11434` (Ollama) - Direct access to the Ollama API (might be needed for initial model setup or if the backend connects externally, though Docker internal networking is preferred).
    * **Supabase Free Tier:** Sign up and create a new project.
        * **Database:** No deployment needed; it's a managed Postgres instance. Create your `profiles` table and any other necessary tables (e.g., `messages`, `chat_rooms`) via the Supabase UI or migration scripts run manually/via CI.
        * **Auth:** Enable email/password authentication and configure settings via the Supabase UI.
        * **Storage:** Configure buckets via the Supabase UI if needed for user avatars or file sharing.
        * Note your **Project URL** and **Anon Key** from the Supabase settings; these are crucial environment variables for the backend and frontend.
    * **Cloudflare Pages Free Tier:** Sign up and connect your GitHub repository. Configure a new project to build the `frontend/` directory. Specify the build command (`flutter build web`) and the output directory (`build/web`).
    * **GitHub Actions Free Tier:** This is enabled by default for your GitHub repository. You just need to define the workflows (`.github/workflows/`). Configure **GitHub Secrets** for sensitive information needed by your workflows, such as the Oracle VM's SSH key (`VM_SSH_KEY`), hostname/IP (`VM_HOST`), and username (`VM_USER`), as well as Supabase credentials if needed by CI steps (though less common for deployment).
    * **UptimeRobot Free Tier:** Sign up and create HTTP monitors pointing to your deployed backend API endpoint (`http://<VM_IP>:8000` or `https://yourdomain.com/api`) and the frontend web URL (`https://groupify.pages.dev` or `https://yourdomain.com`).

2.  **Backend & AI Deployment Pipeline (Automated via GitHub Actions):**
    * **Trigger:** A code `push` to the main branch (or any configured branch) in the `groupify/backend/` directory or related files (`requirements.txt`, `ai/docker-compose.yml`).
    * **GitHub Action (`.github/workflows/ci.yml`):**
        * **Checkout:** Clones the latest code from the repository.
        * **Build Backend Docker Image:** Navigates to `backend/` and runs `docker build -t groupify-backend .`. This creates a fresh Docker image containing the latest backend code and dependencies.
        * **(Optional) Test:** Runs backend tests (`pytest ./backend/tests`) within the action runner or a temporary container built from the image. If tests fail, the workflow stops.
        * **SSH Deploy:** Uses the `appleboy/ssh-action` or similar action.
            * Connects to the Oracle VM using the provided SSH credentials (from GitHub Secrets).
            * Navigates to the project directory on the VM (e.g., `~/groupify`).
            * Copies updated Docker Compose files (`ai/docker-compose.yml`, `backend/docker-compose.yml`) and potentially the new backend Docker image (though building on the VM or using a registry is better for image size). A common pattern is:
                * Pull the *latest backend image* from a container registry (if pushed there first, requires setting up a free registry or using Docker Hub's free tier). Or, `rsync` the backend directory and build on the VM. *Simpler zero-cost is often building on the VM.*
                * Ensure Ollama service is defined and potentially running via `ai/docker-compose.yml`.
                * Run `docker-compose -f backend/docker-compose.yml -f ai/docker-compose.yml pull` (pulls necessary images like Ollama).
                * Run `docker-compose -f backend/docker-compose.yml -f ai/docker-compose.yml up -d --build --force-recreate backend ollama`. This command:
                    * Uses both compose files.
                    * Starts services in detached mode (`-d`).
                    * Builds the backend image (`--build`) using the local code (if rsynced) or uses the image name if pulled.
                    * Forces recreation of containers (`--force-recreate`) to pick up image changes.
                    * Only targets the `backend` and `ollama` services.
                    * Sets necessary environment variables (Supabase URLs, Ollama Endpoint) which should be configured on the VM itself or passed securely to `docker-compose`.
    * **VM Execution:** Docker Compose on the Oracle VM pulls/builds the latest images and starts/restarts the `backend` and `ollama` containers. The `backend` container communicates with the `ollama` container via Docker's internal network (e.g., addressing it as `ollama` if services are linked or on the same network). It connects to Supabase remotely over the internet using the provided URL/Key.

3.  **Frontend Web Deployment Pipeline (Automated via Cloudflare Pages Git Integration):**
    * **Trigger:** A code `push` to the main branch (or configured production branch) in the `groupify/frontend/` directory.
    * **Cloudflare Pages Build Process:**
        * Cloudflare detects the commit via Git integration.
        * It pulls the latest code.
        * It executes the configured build command (`flutter build web`). This compiles the Dart code into HTML, CSS, and JavaScript, placing the output in the `build/web` directory.
        * It deploys the contents of the specified output directory (`build/web`) to Cloudflare's global CDN.
    * **Result:** The web application is now accessible via the Cloudflare Pages URL (e.g., `your-project-name.pages.dev`). If you configure a custom domain, Cloudflare handles the DNS and SSL automatically.

4.  **Database, Auth, Storage Management (Managed Service):**
    * These are hosted and maintained by Supabase. You interact with them primarily via the Supabase web UI for schema definition, data viewing, user management, etc., or programmatically via the Supabase client libraries in your backend and frontend code.
    * Schema changes (creating tables, columns, RLS policies) are applied directly via the Supabase dashboard SQL editor or migration tools (manual or potentially automated via CI if you set up a migration runner, but this adds complexity).

5.  **Mobile & Desktop Distribution (Manual or CI-assisted Build):**
    * **Build:** You run `flutter build apk`, `flutter build ios`, `flutter build windows`, etc., either locally on your development machine or as part of a separate GitHub Actions workflow.
    * **Distribution:** The resulting build artifacts (`.apk`, `.ipa`, `.exe`, etc.) are *not* deployed to the cloud hosting providers mentioned for the backend or web app.
        * **Mobile:** You manually upload `.apk` to the Google Play Console (developer account required, not free) and `.ipa` to Apple App Store Connect (developer account required, not free).
        * **Desktop:** You can distribute installers directly (e.g., via a download link) or potentially through platform-specific stores (Microsoft Store, Snapcraft, etc.).

6.  **Monitoring Deployment (Managed Service):**
    * UptimeRobot continuously sends requests to the public endpoints (backend API, frontend URL) you configured. It's a SaaS service, so there's no code deployment from your side; you manage monitors via their dashboard.

**In summary, the deployment is a hybrid process:**

* **Automated for Backend & AI:** Git push triggers CI/CD, which builds Docker images and uses SSH to update and restart containers on your Oracle VM.
* **Automated for Frontend Web:** Git push triggers Cloudflare Pages' integrated build and static site deployment.
* **Managed for DB, Auth, Storage, Monitoring:** These services are configured via provider dashboards and accessed remotely by your deployed applications.
* **Manual/CI-assisted Build for Mobile/Desktop:** Native builds are created and then distributed through platform-specific channels.

This setup allows the core, always-running components (Backend, AI, Web App) to be automatically updated based on code changes within the zero-cost infrastructure.
