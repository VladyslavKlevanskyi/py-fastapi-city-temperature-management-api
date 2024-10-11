# City Temperature Management API

## Overview

This FastAPI application provides a management system for cities and their corresponding temperature data. The application includes a CRUD API for managing city information and a separate API for fetching and storing temperature data.

- **City Management**: Create, read, update, and delete city records.
- **Temperature Tracking**: Fetch current temperature data for cities from an online resource and store it in the database.
- **Data Retrieval**: Access temperature records for individual cities or all recorded temperatures.

## Technologies Used

- **FastAPI**: For building the web application.
- **SQLAlchemy**: For database management and ORM.
- **SQLite**: As the database for storing city and temperature data.
- **Pydantic**: For data validation and serialization.

## Getting Started

### Prerequisites

- Python 3.11+
- A virtual environment (recommended)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd city_temperature_management_api
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Set up your environment variables in a .env file (see .env.example for a template).

### Database Migration

Run the following command to create the database and tables:

   ```
   alembic revision --autogenerate -m "Initial migration"
   ```
   ```
   alembic upgrade head
   ```
### Running the Application

You can start the application using Uvicorn:
   ```
   uvicorn app.main:app --reload
   ```

### API Endpoints

#### Cities
 - `POST /cities:` Create a new city.
 - `GET /cities:` Get a list of all cities.
 - `GET /cities/{city_id}:` Get details of a specific city (optional).
 - `PUT /cities/{city_id}:` Update details of a specific city (optional).
 - `DELETE /cities/{city_id}:` Delete a specific city.

#### Temperatures

 - `POST /temperatures/update:` Fetch and store the current temperature for all cities.
 - `GET /temperatures:` Get a list of all temperature records.
 - `GET /temperatures/?city_id={city_id}:` Get temperature records for a specific city.

## Design Choices

1. **FastAPI Framework:** FastAPI is chosen for its speed, ease of use, and automatic generation of OpenAPI documentation.

2. **Asynchronous Programming:** Using async and await allows for non-blocking requests, which is crucial when fetching temperature data from an online API.

3. **SQLite:** SQLite is used for simplicity and ease of setup. It is suitable for development and testing. For production, a more robust database solution could be implemented.

4. **Modular Structure:** The project is organized into directories for models, schemas, CRUD operations, and database configuration to promote separation of concerns and maintainability.

## Assumptions and Simplifications

1. Temperature Data Source: The application assumes a reliable source for fetching current temperatures is available. This is typically an external API.

2. Data Validation: Basic validation is implemented using Pydantic models to ensure data integrity.

3. Error Handling: Basic error handling is implemented.