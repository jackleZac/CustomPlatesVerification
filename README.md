# Truck Plate Recognition Backend
This is a Flask-based backend for a truck plate recognition system designed for customs use. It processes truck number plates (assuming OCR is handled externally), stores truck records in a MySQL database, and searches for approximate matches using a Levenshtein Distance algorithm optimized with a BK-Tree. The backend exposes RESTful APIs for a separate frontend to interact with, enabling efficient matching of plate numbers despite potential OCR errors.

## Features

- **Efficient Search**: Uses a BK-Tree to perform approximate string matching with Levenshtein Distance, tolerating OCR errors (e.g., "ABCI23" matches "ABC123").
- **MySQL Integration**: Stores truck records (plate number, truck ID, owner) and retrieves details for matches.
- **Modular Architecture**: Separates routes, database utilities, and search logic for maintainability.
- **API Endpoints**: Provides endpoints to search for plates and add new truck records.

## Setup Instructions

### Prerequisites

- Python 3.x
- MySQL
- Flask

### Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/yourusername/truck_plate_validator.git
   cd truck_plate_validator

## Search Algorithm

The backend implements Levenshtein Distance with a BK-Tree for efficient approximate string matching:

### Levenshtein Distance

- Measures the minimum number of single-character edits (insertions, deletions, substitutions) to transform one string into another.
- Example: Distance between "ABCI23" and "ABC123" is 1 (substitute "I" with "1").
- Time complexity: O(m * n) for two strings of lengths m and n.

### BK-Tree

- **Metric Tree**: Organizes strings based on their Levenshtein Distance from a root node.
- **Search Efficiency**: Uses the triangle inequality to prune branches during search, reducing the time complexity from O(n * m * k) (naive comparison with all database entries) to O(log n) on average for a database of n plates.
- **Example**: Searching "ABCI23" with a max distance of 2 quickly returns "ABC123" (distance 1) by avoiding unnecessary comparisons.
- **Initialization**: The BK-Tree is initialized with all plate numbers from the database on startup and updated when new trucks are 

## Project Structure

The project structure includes the following files and directories:

- `main.py` - Flask app entry point
- `routes.py` - API routes
- `bk_tree.py` - BK-Tree and Levenshtein Distance implementation
- `db.py` - MySQL database utilities
- `config.py` - Configuration (e.g., MySQL credentials)
- `requirements.txt` - Dependencies
- `README.md` - This file

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- OCR tools like Tesseract (optional, if integrating image processing directly)

1. **Clone the Repository**

   ```sh
   git clone <repository-url>
   cd truck_plate_backend

2. **Install Dependencies**

   ```sh
   pip install -r requirements.txt

3. **Run the Backend**
   
   ```sh
   python main.py

### API Endpoints
***POST /api/search_plate***
- `Description`: Searches for truck records matching the provided plate number within a specified Levenshtein Distance tolerance

  \\\json { "exampleKey": "exampleValue", "anotherKey": "anotherValue" } \\\

***Response (200 OK):***
  \\\json {"matches": [{ "plate_number": "ABC123", "truck_id": "T001", "owner": "Stark", "distance": 1}]}

