# Chevrolet Casting Number Lookup API

A FastAPI-based API for looking up Chevrolet engine casting numbers and their associated data. This API allows users to query a SQLite database of Chevrolet casting information by casting number.

## Features

- Lookup Chevrolet casting information by casting number
- Search castings by various criteria (years, CID, main caps, comments, etc.)
- RESTful API with full CRUD operations
- Automatic API documentation with Swagger UI
- CSV data import utility
- Database migration tool

## Project Structure

```
CastingLookup/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── casting.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   └── casting.py
│   ├── schemas/
│   │   └── casting.py
│   ├── utils/
│   │   └── import_data.py
│   └── main.py
├── tests/
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- Pandas (for CSV import)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/JeremyMorgan/CastingLookup.git
cd CastingLookup
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the API

To start the API server:

```bash
python run.py
```

Or directly with uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000.

- API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

### Database Migration

To migrate the database to the new schema and import the Chevrolet casting data:

```bash
python migrate_database.py
```

Options:
- `--file`: Path to the CSV file (default: chev-casting.csv)
- `--batch-size`: Number of records to insert at once (default: 100)
- `--skip-drop`: Skip dropping existing tables

Example:
```bash
python migrate_database.py --file chev-casting.csv --batch-size 200
```

### Importing CSV Data

To import casting data from a CSV file without migrating the database:

```bash
python -m app.utils.import_data path/to/your/data.csv
```

Options:
- `--method`: Method to use for importing data (`pandas`, `csv`, or `chev`, default: `chev`)
- `--batch-size`: Number of records to insert at once (default: 1000)

Example:
```bash
python -m app.utils.import_data chev-casting.csv --method chev --batch-size 500
```

### Using the API Client

The project includes a Python API client in the `examples` directory that demonstrates how to interact with the API programmatically.

To use the API client:

```bash
python -m examples.api_client --action list
```

Available actions:
- `list`: List all castings
- `get`: Get a specific casting by number
- `create`: Create a new casting
- `update`: Update an existing casting
- `delete`: Delete a casting
- `search`: Search for castings based on various criteria

Example:
```bash
# Get a specific casting
python -m examples.api_client --action get --casting-id "140029"

# Search for castings
python -m examples.api_client --action search --years "1980" --cid 350

# Create a new casting
python -m examples.api_client --action create --data '{"casting": "123456", "years": "1970-75", "cid": 350, "comments": "Test casting"}'
```

There's also an interactive example script that demonstrates the API client usage:

```bash
python -m examples.api_client_example
```

## API Endpoints

### Castings

- `GET /api/castings/`: Get a list of all castings
- `GET /api/castings/{casting_id}`: Get a specific casting by its number
- `POST /api/castings/`: Create a new casting
- `PUT /api/castings/{casting_id}`: Update an existing casting
- `DELETE /api/castings/{casting_id}`: Delete a casting
- `GET /api/castings/search/`: Search for castings based on various criteria (years, CID, main caps, comments)

## CSV Format

The import utility expects a CSV file with the following columns:

- `Years`: Production years range (e.g., "1980-85")
- `Casting`: Unique casting number (required)
- `CID`: Cubic Inch Displacement
- `Low Power`: Low power rating
- `High Power`: High power rating
- `Main Caps`: Number of main caps
- `Comments`: Additional comments or notes

Example CSV:

```csv
Years,Casting,CID,Low Power,High Power,Main Caps,Comments,
1980-85,140029,350,-,-,2,cars,
1973-80,330817,400,150,180,2,"car, truck",
1975,355909,262,110,110,2,"car, truck",
```

## Development

### Running Tests

To run the tests:

```bash
python run_tests.py
```

Or directly with pytest:

```bash
pytest
```

### Database

The API uses SQLite as its database. The database file is created at `./castings.db` when the application is first run.

## License

[Creative Commons Universal CC 1.0 Universal](LICENSE)


