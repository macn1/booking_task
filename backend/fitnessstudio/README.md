## Table of Contents
- [Features](#features)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
- [Data Seeding](#data-seeding)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Timezone Handling](#timezone-handling)
- [Error Handling](#error-handling)

## Features ✨
- View upcoming fitness classes (Yoga, Zumba, HIIT)
- Book available class slots
- View client booking history
- Timezone-aware scheduling
- Data seeding via CSV files
- Comprehensive error handling

### Installation
1. Clone the repository:
   git clone  https://github.com/macn1/booking_task.git
2.Create and activate virtual environment:
bashpython -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate

3.installation
pip install -r requirements.txt

4.Run migrations:
python manage.py migrate

5.Load sample data:
python manage.py seed_all

6.Start development server:
python manage.py runserver

API Endpoints 🌐
Base URL: http://localhost:8000/api
Endpoint	Method	Description

/classes/	 GET	List all upcoming classes
/book/	    POST	Create a new booking
/bookings/	 GET	List bookings by email



Example Requests
1. Get Available Classes
curl -X GET "http://localhost:8000/api/classes/?timezone=America/New_York"

2. Create Booking
curl -X POST "http://localhost:8000/api/book/" \
-H "Content-Type: application/json" \
-d '{"fitness_class": 1, "client_name": "John Doe", "client_email": "john@example.com"}'

3. Get Client Bookings
curl -X GET "http://localhost:8000/api/bookings/?email=john@example.com"


Testing 🧪
Run Unit Tests
python manage.py test