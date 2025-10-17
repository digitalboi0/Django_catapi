# Profile API with Cat Facts

This is a simple Django REST API that returns profile information along with a dynamic cat fact fetched from an external API.

## Features

*   Provides a `GET /me` endpoint.
*   Returns profile data (email, name, stack) in a predefined JSON structure.
*   Integrates with the Cat Facts API (`https://catfact.ninja/fact`) to fetch a random cat fact on each request.
*   Includes a dynamic timestamp in ISO 8601 format.
*   Handles external API errors gracefully.
*   Logs errors to a file (`logs/api_logs.txt`).
*   Uses environment variables for configuration.
*   Includes CORS headers for cross-origin requests.

## Prerequisites

*   Python 3.x (e.g., 3.9, 3.10, 3.11)
*   pip (Python package installer)

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/digitalboi0/Django_catapi
    cd Django_catapi
    
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    # On Windows:
    python -m venv venv
    venv\Scripts\activate
    # On macOS/Linux:
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create the Logs Directory:**
    Create a directory named `logs` in your project root (the same directory as `manage.py`).

5.  **Set up Environment Variables:**
    *   Create a file named `.env` in your project root directory.
    *   Add the following content, replacing the placeholder values with your actual information:
        ```env
        Email=xxxxxx # Replace with your email
        Name=xxxxx      # Replace with your name
        Stack=xxxx           # Replace with your stack
        Api_url=https://catfact.ninja/fact # The external API URL
        Timeout=5                      # Request timeout in seconds
        ```
    *   **Important:** Ensure your `.env` file is listed in your `.gitignore` file so that it's not accidentally committed to the repository. The `.env` file should *not* be included in the submitted repository, only the `.env.example` (if you choose to add one) or clear instructions on how to create it.

6.  **Run Migrations (Django specific, although not strictly needed for this simple API, good practice):**
    ```bash
    python manage.py migrate
    ```

7.  **Start the Development Server:**
    ```bash
    python manage.py runserver
    ```

## Running Locally

After completing the setup steps above, your API will be running locally. By default, it starts on `http://127.0.0.1:8000/`.

To test the endpoint, navigate to `http://127.0.0.1:8000/api/me` in your browser or use a tool like `curl`:

```bash
curl http://127.0.0.1:8000/api/me