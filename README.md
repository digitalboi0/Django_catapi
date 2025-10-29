```markdown
# Country Currency & Exchange Rate API

A RESTful API that fetches country data from external APIs, caches it in a database, and provides CRUD operations with filtering, sorting, and image generation capabilities.

## 🚀 Features

- Fetch and cache country data from REST Countries API
- Retrieve real-time exchange rates
- Calculate estimated GDP for each country
- Filter countries by region and currency
- Sort countries by various fields (GDP, name, population)
- Generate summary images with top GDP countries
- Full CRUD operations on country data

## 📋 Prerequisites

- Python 3.8+
- MySQL (for production) or SQLite (for local development)
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/digitalboi0/Django_catapi
    cd Django_catapi
    cd countryapi
```

### 2. Create and activate virtual environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```cmd
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration (for production)
DB_NAME=country_api_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

**Note:** For local development, you can use SQLite (no MySQL required). The app will automatically use SQLite if `DATABASE_URL` is not set.

### 5. Run Migrations

```cmd
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the development server

```cmd
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### 1. Refresh Country Data
Fetch all countries and exchange rates from external APIs and cache them.

**Endpoint:** `POST /countries/refresh/`

**Response:**
```json
{
  "message": "countries refreshed completed",
  "countries_updated": 0,
  "countries_created": 250,
  "countries_skipped": 5,
  "time_refreshed": "2025-10-29T12:00:00Z"
}
```

### 2. List All Countries
Get all countries with optional filtering and sorting.

**Endpoint:** `GET /countries/`

**Query Parameters:**
- `region` - Filter by region (e.g., `?region=Africa`)
- `currency` - Filter by currency code (e.g., `?currency=NGN`)
- `sort` - Sort results:
  - `gdp_desc` - GDP descending
  - `gdp_asc` - GDP ascending
  - `name_asc` - Name ascending
  - `name_desc` - Name descending
  - `population_desc` - Population descending
  - `population_asc` - Population ascending

**Examples:**
```bash
GET /countries/?region=Africa
GET /countries/?currency=USD&sort=gdp_desc
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Nigeria",
    "capital": "Abuja",
    "region": "Africa",
    "population": 206139589,
    "currency_code": "NGN",
    "exchange_rate": 1600.23,
    "estimated_gdp": 25767448125.2,
    "flag_url": "https://flagcdn.com/ng.svg",
    "last_refreshed_at": "2025-10-29T12:00:00Z"
  }
]
```

### 3. Get Single Country
Retrieve a specific country by name.

**Endpoint:** `GET /countries/:name/`

**Example:**
```bash
GET /countries/Nigeria/
```

**Response:**
```json
{
  "id": 1,
  "name": "Nigeria",
  "capital": "Abuja",
  "region": "Africa",
  "population": 206139589,
  "currency_code": "NGN",
  "exchange_rate": 1600.23,
  "estimated_gdp": 25767448125.2,
  "flag_url": "https://flagcdn.com/ng.svg",
  "last_refreshed_at": "2025-10-29T12:00:00Z"
}
```

### 4. Delete Country
Delete a country record from the database.

**Endpoint:** `DELETE /countries/:name/`

**Example:**
```bash
DELETE /countries/Nigeria/
```

**Response:**
```json
{
  "message": "country deleted"
}
```

### 5. Get Status
Show total countries and last refresh timestamp.

**Endpoint:** `GET /status/`

**Response:**
```json
{
  "total_countries": 250,
  "last_refreshed_at": "2025-10-29T12:00:00Z"
}
```

### 6. Get Summary Image
Retrieve the generated summary image showing top GDP countries.

**Endpoint:** `GET /countries/image/`

**Response:** PNG image file

**Download Example:**
```bash
curl http://localhost:8000/countries/image/ --output summary.png
```

## 🧪 Testing the API

### Using curl (Windows Command Prompt):

```cmd
# Refresh data
curl -X POST http://localhost:8000/countries/refresh/

# Get status
curl http://localhost:8000/status/

# List all countries
curl http://localhost:8000/countries/

# Filter by region
curl "http://localhost:8000/countries/?region=Africa"

# Sort by GDP
curl "http://localhost:8000/countries/?sort=gdp_desc"

# Get specific country
curl http://localhost:8000/countries/Nigeria/

# Delete country
curl -X DELETE http://localhost:8000/countries/Nigeria/

# Get summary image
curl http://localhost:8000/countries/image/ --output summary.png
```

### Using Postman:
1. Import the endpoints into Postman
2. Set base URL to `http://localhost:8000`
3. Test each endpoint with appropriate HTTP methods

## 📦 Dependencies

```txt
Django>=5.1.2
djangorestframework
requests
Pillow
python-decouple
dj-database-url
mysqlclient
gunicorn
```

## 🗄️ Database Schema

### Country Model

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | AutoField | Yes | Primary key (auto-increment) |
| name | CharField | Yes | Country name (unique) |
| capital | CharField | No | Capital city |
| region | CharField | No | Geographic region |
| population | BigInteger | Yes | Population count |
| currency_code | CharField | No | ISO currency code |
| exchange_rate | Decimal | No | Exchange rate vs USD |
| estimated_gdp | BigInteger | No | Calculated GDP estimate |
| flag_url | URLField | No | Country flag image URL |
| last_refreshed_at | DateTime | Yes | Last update timestamp |

## 🚀 Deployment

### Railway Deployment

1. **Create Railway Account:** https://railway.app

2. **Install Railway CLI:**
```cmd
npm i -g @railway/cli
```

3. **Login to Railway:**
```cmd
railway login
```

4. **Initialize Project:**
```cmd
railway init
```

5. **Add MySQL Database:**
- Go to Railway dashboard
- Click "New" → "Database" → "Add MySQL"
- Railway will provide `DATABASE_URL` automatically

6. **Deploy:**
```cmd
railway up
```

7. **Run Migrations:**
```cmd
railway run python manage.py migrate
```

### Environment Variables on Railway

Set these in your Railway dashboard:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to `False` for production
- `DATABASE_URL` - Automatically provided by Railway

## ⚠️ Error Handling

The API returns consistent JSON error responses:

| Status Code | Description | Example Response |
|-------------|-------------|------------------|
| 200 | Success | Country data returned |
| 400 | Bad Request | `{"error": "Validation failed"}` |
| 404 | Not Found | `{"error": "Country not found"}` |
| 500 | Internal Error | `{"error": "Internal server error"}` |
| 503 | Service Unavailable | `{"error": "External data source unavailable"}` |

## 🎨 Image Generation

The `/countries/refresh/` endpoint automatically generates a summary image containing:
- Total number of countries
- Top 5 countries by estimated GDP
- Last refresh timestamp

Image is saved at `cache/summary.png` and served via `/countries/image/` endpoint.

## 📝 Notes

- Exchange rates are fetched from: https://open.er-api.com/v6/latest/USD
- Country data from: https://restcountries.com/v2/all
- GDP calculation: `population × random(1000-2000) ÷ exchange_rate`
- Countries without currencies have `null` values for `currency_code` and `exchange_rate`
- Case-insensitive country name matching

## 🐛 Troubleshooting

### MySQL Connection Issues
If you get MySQL connection errors:
1. Ensure MySQL service is running
2. Verify credentials in `.env` file
3. Check if database exists: `CREATE DATABASE country_api_db;`

### Pillow Installation Issues (Windows)
If Pillow fails to install:
```cmd
pip install --upgrade pip
pip install Pillow
```

### Missing Dependencies
```cmd
pip install -r requirements.txt --upgrade
```

## 📄 License

This project is created as part of a backend development task.

## 👤 Author

[Your Name]

## 🤝 Contributing

This is a task project. For any issues or suggestions, please contact the author.
```

---

**Now create these additional files:**

### **requirements.txt**
```txt
Django==5.1.2
djangorestframework
requests
Pillow
python-decouple
dj-database-url
mysqlclient
gunicorn
```

### **.gitignore**
```
# Python
*.py[cod]
__pycache__/
*.so
*.egg
*.egg-info/
dist/
build/

# Django
*.log
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment
.env
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Cache
cache/
*.png

# OS
.DS_Store
Thumbs.db
```

### **runtime.txt** (for Railway)
```txt
python-3.11.0
```

### **Procfile** (for Railway)
```
web: python manage.py migrate && gunicorn your_project_name.wsgi
```


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
