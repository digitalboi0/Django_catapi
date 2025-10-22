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

# String Analyzer API

This is a Django REST API that analyzes strings and stores their computed properties. It fulfills the requirements for Backend Stage 1.

## Features

*   Provides a `POST /strings` endpoint to analyze a string and store its properties.
*   Provides a `GET /strings/{string_value}` endpoint to retrieve a specific analyzed string.
*   Provides a `GET /strings` endpoint to list all analyzed strings with optional filtering.
*   Provides a `GET /strings/filter-by-natural-language` endpoint to filter strings using natural language queries.
*   Provides a `DELETE /strings/{string_value}` endpoint to delete a specific analyzed string.
*   Computes and stores the following properties for each string:
    *   `length`: Number of characters.
    *   `is_palindrome`: Boolean (case-insensitive).
    *   `unique_characters`: Count of distinct characters (case-insensitive).
    *   `word_count`: Number of words separated by whitespace.
    *   `sha256_hash`: SHA-256 hash of the string (used as the primary key).
    *   `character_frequency_map`: Object mapping each character (case-insensitive) to its occurrence count.
*   Handles duplicate string analysis attempts.
*   Validates input data types (ensures `value` is a string).
*   Implements filtering via query parameters.
*   Implements basic natural language filtering.
*   Handles conflicting filters in natural language queries.
*   Returns appropriate HTTP status codes and error messages.
*   Uses environment variables for configuration.

## Prerequisites

*   Python 3.x (e.g., 3.9, 3.10, 3.11)
*   pip (Python package installer)

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
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


    *   **Important:** Ensure your `.env` file is listed in your `.gitignore` file so that it's not accidentally committed to the repository.

4.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Start the Development Server:**
    ```bash
    python manage.py runserver
    ```

## Running Locally

After completing the setup steps above, your API will be running locally. By default, it starts on `http://127.0.0.1:8000/`.

## Dependencies

This project relies on the following Python packages, listed in `requirements.txt`:

*   Django
*   djangorestframework
*   requests
*   python-decouple
*   django-cors-headers
*   gunicorn (if deploying)

## API Endpoints

*   **POST** `/api/strings`: Analyzes a string and stores its properties.
    *   **Request Body:** `{"value": "string to analyze"}`
    *   **Response Format:** See task description.
    *   **Errors:** 400, 409, 422

*   **GET** `/api/strings/{string_value}`: Retrieves a specific string's data.
    *   **Response Format:** See task description.
    *   **Errors:** 404

*   **GET** `/api/strings`: Lists all strings with optional filtering.
    *   **Query Parameters:** `is_palindrome`, `min_length`, `max_length`, `word_count`, `contains_character`
    *   **Response Format:** See task description.
    *   **Errors:** 400

*   **GET** `/api/strings/filter-by-natural-language`: Filters strings using natural language.
    *   **Query Parameter:** `query`
    *   **Response Format:** See task description.
    *   **Errors:** 400, 422

*   **DELETE** `/api/strings/{string_value}`: Deletes a specific string.
    *   **Response:** 204 No Content.
    *   **Errors:** 404

## Notes

*   The `/api/me` endpoint from Stage 0 is still present.
*   Ensure the `SECRET_KEY` environment variable is set securely in production.
*   The `DEBUG` environment variable should be `False` in production.
*   The `ALLOWED_HOSTS` setting includes `.railway.app` and `127.0.0.1`.
