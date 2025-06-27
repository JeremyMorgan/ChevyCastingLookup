# Chevy Casting Lookup Web Interface

A Flask-based web interface for the Chevy Casting Lookup API. This application provides a user-friendly way to search and browse Chevrolet casting numbers and their specifications.

## Features

- **Quick Casting Search**: Direct lookup by casting number
- **Advanced Search**: Search by years, CID, main caps, or comments
- **Browse All**: Paginated view of all casting numbers
- **Detailed Views**: Comprehensive information for each casting
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **Real-time API Status**: Shows connection status to the FastAPI backend

## Prerequisites

- Python 3.7+
- FastAPI backend running on port 8000 (from the main project)
- Modern web browser

## Installation

1. Navigate to the Flask web interface directory:
   ```bash
   cd flask_web_interface
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Method 1: Using the runner script (Recommended)
```bash
python run_flask.py
```

### Method 2: Direct Flask execution
```bash
python app.py
```

### Method 3: Using Flask CLI
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

## Accessing the Application

Once started, the web interface will be available at:
- **Local access**: http://localhost:5000
- **Network access**: http://YOUR_IP_ADDRESS:5000

## API Backend Requirement

**Important**: This web interface requires the FastAPI backend to be running on port 8000. 

To start the FastAPI backend:
```bash
# From the main project directory
python run.py
```

The FastAPI backend should be accessible at http://localhost:8000

## Application Structure

```
flask_web_interface/
├── app.py                 # Main Flask application
├── api_client.py          # API client for FastAPI communication
├── run_flask.py          # Application runner script
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/           # Jinja2 templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── results.html     # Search results
│   └── casting_detail.html # Casting details
└── static/              # Static assets
    ├── css/
    │   └── style.css    # Custom styles
    └── js/
        └── main.js      # JavaScript functionality
```

## Usage

### Quick Search
1. Enter a casting number in the search box on the home page
2. Click "Search" to find the specific casting
3. If found, you'll be redirected to the detailed view

### Advanced Search
1. Click "Advanced Search Options" on the home page
2. Fill in any combination of search criteria:
   - Production Years (e.g., "1970-75")
   - Cubic Inch Displacement (e.g., 350)
   - Main Caps (e.g., "4-bolt")
   - Comments (search within comments)
3. Click "Advanced Search" to see results

### Browse All
1. Click "Browse All" to see paginated results of all castings
2. Use the pagination controls to navigate through results
3. Click on any casting number to view detailed information

## Configuration

### API Endpoint
The default API endpoint is `http://localhost:8000`. To change this, modify the `CastingAPIClient` initialization in `app.py`:

```python
api_client = CastingAPIClient(base_url="http://your-api-server:8000")
```

### Flask Configuration
Key configuration options in `app.py`:
- `secret_key`: Change this for production use
- `debug`: Set to `False` for production
- `host` and `port`: Modify as needed

## Development

### Adding New Features
1. Add new routes in `app.py`
2. Create corresponding templates in `templates/`
3. Add any required JavaScript in `static/js/main.js`
4. Update styles in `static/css/style.css`

### Error Handling
The application includes comprehensive error handling:
- API connection errors
- Invalid search parameters
- Missing casting numbers
- Server errors

## Troubleshooting

### Common Issues

1. **"Unable to connect to the casting lookup API"**
   - Ensure the FastAPI backend is running on port 8000
   - Check if the API is accessible at http://localhost:8000

2. **"No casting found"**
   - Verify the casting number is correct
   - Try using the advanced search with partial criteria

3. **Page not loading**
   - Check that Flask is running on port 5000
   - Ensure no other application is using port 5000

### Logs
The application logs important events and errors. Check the console output for debugging information.

## Production Deployment

For production deployment:

1. Set `debug=False` in `app.py`
2. Change the `secret_key` to a secure random value
3. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
4. Configure a reverse proxy (nginx/Apache) if needed
5. Set up proper logging and monitoring

## License

This project follows the same license as the main Chevy Casting Lookup project.
