# Vacation Management System

## Table of Contents
- [Project Description](#project-description)
- [Team Member Contributions](#team-member-contributions)
- [Technical Architecture](#technical-architecture)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Database Schema](#database-schema)
- [Usage Guide](#usage-guide)
- [Security Features](#security-features)
- [Error Handling](#error-handling)
- [Contributing](#contributing)


## Project Description

The Vacation Management System is a robust Python-based application that enables users to discover, manage, and interact with vacation packages. Built with a focus on security and usability, the system provides different functionality levels for regular users and administrators, ensuring efficient vacation management and user engagement.

### Core Objectives
- Provide an intuitive platform for browsing and managing vacation packages
- Enable secure user authentication and authorization
- Allow users to interact with vacation listings through a like system
- Provide administrators with comprehensive vacation management tools
- Ensure data security and validation at all levels

## Team Member Contributions

### Ben Ari Maymon - 
- Designed and implemented the Data Access Layer (DAL)
- Developed the UserLogic module for user management and validation
- Created the VacationLogic module for vacation operations
- Built the main application interface and menu system
- Implemented database operations and connections
- Developed user input handling and validation
- Created core system architecture

### Agam Avaksis - 
- Designed and implemented the SystemFacade pattern
- Developed the LikeLogic module for vacation interactions
- Created comprehensive testing strategy
- Performed system testing and validation
- Implemented error handling and validation
- Documentation and code review

### Collaborative Achievements
- Implemented layered architecture design
- Regular code reviews and pair programming
- Documentation updates and maintenance
- System integration and testing
- Bug fixing and feature enhancements

## Technical Architecture

### System Layers
1. Presentation Layer (main.py)
   - User interface
   - Input/output handling
   - Menu system

2. Business Logic Layer
   - UserLogic: User management and validation
   - VacationLogic: Vacation operations and validation
   - LikeLogic: Like system management

3. Data Access Layer (DAL)
   - Database operations
   - Query execution
   - Connection management

4. System Facade
   - Coordinates between layers
   - Manages authentication
   - Handles authorization

## Features

### Regular User Features
- Account registration and login
- Browse vacation packages
- View detailed vacation information
- Like/unlike vacations
- View liked vacations
- Secure password management

### Administrator Features
- Full vacation CRUD operations
- Add new destinations
- Edit vacation details
- Remove vacation packages
- System-wide vacation view

## Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL Server
- pip package manager

### Installation Steps

1. Clone the repository:
```bash
git clone [repository-url]
cd vacation-management-system
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install mysql-connector-python
pip install python-dotenv
pip install bcrypt
pip install python-dateutil
```

4. Configure environment:
Create `.env` file with:
```env
DB_HOST=localhost
DB_NAME=vacation_system
DB_USER=your_username
DB_PASSWORD=your_password
```

5. Set up database:
```sql
CREATE DATABASE vacation_system;
USE vacation_system;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    role INT DEFAULT 1
);

CREATE TABLE countries (
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL
);

CREATE TABLE vacations (
    vacation_id INT AUTO_INCREMENT PRIMARY KEY,
    vacation_title VARCHAR(100) NOT NULL,
    country INT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    img_url VARCHAR(255),
    FOREIGN KEY (country) REFERENCES countries(country_id)
);

CREATE TABLE likes (
    like_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    vacation_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (vacation_id) REFERENCES vacations(vacation_id)
);
```

6. Run application:
```bash
python main.py
```

## Usage Guide

### Regular Users
1. Register new account:
   - Enter personal details
   - Provide valid email
   - Create secure password
   - Confirm age (18+)

2. Browse vacations:
   - View all available packages
   - See pricing and dates
   - Check destination details

3. Interact with vacations:
   - Like favorite packages
   - Unlike previously liked vacations
   - View personal liked list

### Administrators
1. Vacation Management:
   - Add new vacation packages
   - Edit existing vacations
   - Remove outdated listings
   - View system-wide data

2. Access admin panel:
   - Login with admin credentials
   - Use extended feature set
   - Manage vacation database

## Security Features

### Password Security
- Bcrypt hashing
- Minimum length: 6 characters
- Must include uppercase and lowercase letters
- Must include numbers
- Must include special characters

### Data Validation
- Email format verification
- Date range validation (start date must be future date)
- Price range checks ($1,000 - $10,000)
- Input sanitization
- Age verification (18+)

### System Security
- Role-based access control
- Session management
- SQL injection prevention through parameterized queries
- Comprehensive error handling

## Error Handling

The system implements comprehensive error handling for:
- Invalid login credentials
- Registration validation errors
- Database connection issues
- Invalid vacation data
- Authorization failures
- Input validation errors
- Date format errors
- Price range violations

## Project Structure
```
vacation-management-system/
├── main.py                 # Main application entry point
├── utils/
│   └── dal.py             # Data Access Layer
├── logic/
│   ├── user_logic.py      # User management logic
│   ├── vacation_logic.py  # Vacation operations logic
│   └── like_logic.py      # Like system logic
├── facade/
│   └── system_facade.py   # System facade pattern
└── .env                   # Environment configuration
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

### Coding Standards
- Follow PEP 8 Python style guide
- Include docstrings for all functions
- Write unit tests for new features
- Update documentation as needed



---

Developed by Ben Ari Maymon and Agam Avaksis .