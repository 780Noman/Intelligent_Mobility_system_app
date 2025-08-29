# Intelligent Mobility System (IMS)

## Project Overview

The Intelligent Mobility System (IMS) is a Django-based web application designed to manage and interact with mobility-related data and integrate with advanced AI simulations. While the core web application provides an interface for data management and visualization, the integrated AI simulations (DDQN and NEAT) are intended for local execution and development, with their results often presented via video links within the web interface.

## Features

*   **Web Interface:** Built with Django, providing a robust and scalable backend.
*   **AI Simulation Integration:** Displays results from Deep Double Q-Network (DDQN) and NeuroEvolution of Augmenting Topologies (NEAT) simulations. **Note:** The simulations themselves run locally; the deployed web application does not execute them.
*   **Video Link Integration:** Seamlessly embeds external video links to showcase simulation outcomes.
*   **User Management:** (If applicable, based on previous context, assuming basic Django user model is used).
*   **Database Management:** Utilizes Django's ORM for efficient data handling.

## Local Setup and Development

Follow these steps to set up and run the IMS project on your local machine.

### Prerequisites

*   Python 3.x
*   pip (Python package installer)
*   Git

### 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone <your-github-repo-url>
cd IMS
```

### 2. Set Up Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies:

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r gui/requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the `gui/gui/` directory (or `gui/` if `settings.py` is directly there) for sensitive settings.

```
# gui/gui/.env (or gui/.env depending on your project structure)
SECRET_KEY='your_very_secret_key_here'
DEBUG=False
```
**Important:** Replace `your_very_secret_key_here` with a strong, randomly generated key. Keep `DEBUG` set to `False` for production environments.

### 5. Database Migrations

Apply the database migrations to set up your database schema:

```bash
python gui/manage.py migrate
```

### 6. Create Superuser (Optional)

To access the Django admin panel, create a superuser:

```bash
python gui/manage.py createsuperuser
```

### 7. Run the Development Server

Start the Django development server:

```bash
python gui/manage.py runserver
```

The application should now be accessible at `http://127.0.0.1:8000/`.

### Running Simulations Locally

The AI simulations (DDQN and NEAT) are designed to run in their respective local environments. These are located in the `FYP/` and `fyp1/` directories at the project root. Each directory contains its own `requirements.txt` and scripts (e.g., `main.py`, `model_testing_NEAT.py`) for running the simulations.

To run a simulation:
1.  Navigate to the specific simulation directory (e.g., `cd FYP/` or `cd fyp1/`).
2.  Set up a virtual environment and install its `requirements.txt` (if different from the main project).
3.  Execute the main simulation script.

## Deployment

This section outlines the procedures for deploying the IMS application.

### GitHub

The project is managed using Git. Standard Git workflows apply for version control and collaboration.

1.  **Initialize Git (if not already):**
    ```bash
    git init
    ```
2.  **Add Remote:**
    ```bash
    git remote add origin <your-github-repo-url>
    ```
3.  **Add and Commit Changes:**
    ```bash
    git add .
    git commit -m "Initial commit"
    ```
4.  **Push to GitHub:**
    ```bash
    git push -u origin main
    ```

### Hugging Face Spaces

The IMS application can be deployed as a Docker Space on Hugging Face.

#### Prerequisites

*   A Hugging Face account.
*   Docker installed locally (for testing Dockerfile if needed).

#### Deployment Steps

1.  **Create a New Space:**
    *   Go to [Hugging Face Spaces](https://huggingface.co/spaces).
    *   Click "Create new Space".
    *   Choose "Docker" as the Space SDK.
    *   Select a suitable hardware and visibility setting.
    *   Name your Space (e.g., `your-username/ims-app`).

2.  **Configure Secrets:**
    *   In your Hugging Face Space settings, navigate to the "Secrets" section.
    *   Add a new secret named `SECRET_KEY` and paste your Django `SECRET_KEY` value here. This ensures your sensitive key is not exposed in your code.

3.  **Push Code to Space's Git Remote:**
    Your Hugging Face Space acts as its own Git repository. You can push your project directly to it.

    *   **Add the Space as a Git Remote:**
        ```bash
        git remote add space https://huggingface.co/spaces/<your-username>/<your-space-name>
        ```
        (Replace `<your-username>` and `<your-space-name>` with your actual details).

    *   **Push your `main` branch to the Space:**
        ```bash
        git push space main
        ```
        This command will trigger a new build on Hugging Face.

#### Dockerfile

The `Dockerfile` at the project root defines how your application is built into a Docker image. It includes steps to install dependencies, copy your code, and run the Django application using Gunicorn.

#### .dockerignore

The `.dockerignore` file is crucial for optimizing your Docker image size and build times. It specifies files and directories that should be excluded from the Docker build context. For this project, it explicitly excludes:

*   `.git/`: Git version control history.
*   `venv/`: Python virtual environment.
*   `__pycache__/`, `*.pyc`, `*.pyo`, `*.pyd`: Python compiled files.
*   `.env`, `db.sqlite3`: Local environment variables and development database.
*   `FYP/`, `fyp1/`: Local simulation environments (as they are not needed for the deployed web app).
*   `gui/interface/simulations/`: Specific simulation code and models within the Django app (also not needed for deployment).

This ensures that only necessary files are included in your Docker image, leading to faster builds and reduced cold start times.

#### Troubleshooting Deployment

*   **Long Startup Times (Cold Start):** On free Hugging Face tiers, applications may experience a "cold start" delay as the container needs to spin up. This is normal.
*   **Build Failures:**
    *   **Check Logs:** Always check the "Logs" or "Build logs" tab on your Hugging Face Space page. This is the primary source of information for build errors.
    *   **Dependency Issues:** Ensure all dependencies are correctly listed in `gui/requirements.txt` and are compatible with the Docker environment.
    *   **Path Issues:** Verify all paths in your `Dockerfile` and code are correct relative to the Docker build context.
*   **Changes Not Reflecting:**
    *   Ensure you have pushed your latest changes to the correct Git remote (`origin` for GitHub, `space` for Hugging Face).
    *   Verify the branch you pushed to matches the branch Hugging Face is configured to deploy from.
    *   Check Hugging Face build logs for any errors or if a new build was triggered. Sometimes, a manual "Rebuild" from the Space settings can help.

## Security Considerations

*   **`SECRET_KEY`:** Never hardcode your `SECRET_KEY` directly in `settings.py`. Always use environment variables (e.g., via `python-decouple`) and store it as a secret in deployment environments like Hugging Face.
*   **`DEBUG` Mode:** Set `DEBUG=False` in production environments. `DEBUG=True` exposes sensitive information and should only be used during local development.

---