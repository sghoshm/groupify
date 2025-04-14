import os
import subprocess

def create_empty_file(filepath):
    """Creates an empty file if it doesn't exist."""
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            pass

def create_directory(path):
    """Creates a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory '{path}' already exists.")

def create_project_structure():
    """Creates the 'groupify' project structure and initializes the Flutter frontend."""

    project_name = "groupify"
    backend_dir = os.path.join(project_name, "backend")
    frontend_dir = os.path.join(project_name, "frontend")
    docker_dir = os.path.join(project_name, "docker")
    ollama_docker_dir = os.path.join(docker_dir, "ollama")

    backend_app_dir = os.path.join(backend_dir, "app")
    backend_app_api_v1_dir = os.path.join(backend_app_dir, "api", "v1")
    backend_app_api_v1_endpoints_dir = os.path.join(backend_app_api_v1_dir, "endpoints")
    backend_app_core_dir = os.path.join(backend_app_dir, "core")
    backend_app_crud_dir = os.path.join(backend_app_dir, "crud")
    backend_app_models_dir = os.path.join(backend_app_dir, "models")
    backend_app_schemas_dir = os.path.join(backend_app_dir, "schemas")
    backend_app_utils_dir = os.path.join(backend_app_dir, "utils")
    backend_alembic_dir = os.path.join(backend_dir, "alembic")

    # Create the main groupify directory
    create_directory(project_name)

    # Create backend directories
    create_directory(backend_dir)
    create_directory(backend_app_dir)
    create_directory(backend_app_api_v1_dir)
    create_directory(backend_app_api_v1_endpoints_dir)
    create_directory(backend_app_core_dir)
    create_directory(backend_app_crud_dir)
    create_directory(backend_app_models_dir)
    create_directory(backend_app_schemas_dir)
    create_directory(backend_app_utils_dir)
    create_directory(backend_alembic_dir)

    # Create empty __init__.py files for backend packages
    create_empty_file(os.path.join(backend_app_dir, "__init__.py"))
    create_empty_file(os.path.join(backend_app_api_v1_dir, "__init__.py"))
    create_empty_file(os.path.join(backend_app_api_v1_endpoints_dir, "__init__.py"))
    create_empty_file(os.path.join(backend_app_core_dir, "__init__.py"))
    create_empty_file(os.path.join(backend_app_crud_dir, "__init__.py"))
    create_empty_file(os.path.join(backend_app_models_dir, "__init__.py"))
    create_empty_file(os.path.join(backend_app_schemas_dir, "__init__.py"))
    create_empty_file(os.path.join(backend_app_utils_dir, "__init__.py"))

    # Create empty backend files
    create_empty_file(os.path.join(backend_app_dir, "main.py"))
    create_empty_file(os.path.join(backend_app_api_v1_dir, "api.py"))
    create_empty_file(os.path.join(backend_app_api_v1_endpoints_dir, "auth.py"))
    create_empty_file(os.path.join(backend_app_api_v1_endpoints_dir, "chat.py"))
    create_empty_file(os.path.join(backend_app_api_v1_endpoints_dir, "users.py"))
    create_empty_file(os.path.join(backend_app_core_dir, "config.py"))
    create_empty_file(os.path.join(backend_app_crud_dir, "chat.py"))
    create_empty_file(os.path.join(backend_app_crud_dir, "user_profile.py"))
    create_empty_file(os.path.join(backend_app_models_dir, "chat.py"))
    create_empty_file(os.path.join(backend_app_models_dir, "user_profile.py"))
    create_empty_file(os.path.join(backend_app_schemas_dir, "chat.py"))
    create_empty_file(os.path.join(backend_app_schemas_dir, "user_profile.py"))
    create_empty_file(os.path.join(backend_app_utils_dir, "appwrite_client.py"))
    create_empty_file(os.path.join(backend_dir, "alembic.ini"))
    create_empty_file(os.path.join(backend_dir, "requirements.txt"))
    create_empty_file(os.path.join(backend_dir, "Dockerfile"))

    # Initialize the Flutter frontend
    print("\nInitializing Flutter frontend...")
    try:
        subprocess.run(["flutter", "create", frontend_dir], check=True)
        print(f"Flutter project created in: {frontend_dir}")
    except FileNotFoundError:
        print("Error: Flutter command not found. Please ensure Flutter is installed and in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating Flutter project: {e}")

    # Create Docker directories and files
    create_directory(docker_dir)
    create_directory(ollama_docker_dir)
    create_empty_file(os.path.join(docker_dir, "docker-compose.yml"))
    create_empty_file(os.path.join(ollama_docker_dir, "Dockerfile"))

    # Create root level files
    create_empty_file(os.path.join(project_name, ".gitignore"))
    create_empty_file(os.path.join(project_name, "README.md"))

if __name__ == "__main__":
    create_project_structure()
    print("\nProject setup complete with all directories and initial files!")