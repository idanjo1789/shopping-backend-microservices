# shopping-backend-microservices

Microservices-based eCommerce platform built with FastAPI, MySQL, Docker, and Streamlit.

---

## Project Overview

This project is a full end-to-end microservices-based shopping platform.

It was built as a final project with emphasis on:
- backend architecture
- business logic
- authentication
- stock handling
- order lifecycle
- favorite items
- chat assistant integration

The UI is implemented with Streamlit, while the backend is built with FastAPI and MySQL, all running with Docker.

---

## Architecture

The system is built from 3 main services:

### 1. User Service
Responsible for:
- user registration
- login and authentication
- JWT token generation and validation
- password hashing with bcrypt
- account deletion
- returning current user details

### 2. Store Service
Responsible for:
- product management
- product search and filtering
- favorite items
- order management
- stock validation
- stock updates after purchase
- chat assistant integration

### 3. Streamlit Frontend
Responsible for:
- main shopping page
- login and registration page
- favorites page
- orders page
- chat assistant page
- session token handling
- navigation between pages

---

## Technology Stack

### Backend
- Python
- FastAPI
- MySQL
- Docker
- databases
- aiomysql
- JWT
- passlib / bcrypt

### Frontend
- Python
- Streamlit

### AI
- OpenAI Chat API

---

## Main Features

### Shop Page
The main page of the system is the **Shop** page.

It includes:
- product search
- products grid
- product images
- price display
- stock display
- product descriptions

Search supports:
- regular text search by product name
- multiple names separated by comma
- price search using:
  - `>`
  - `<`
  - `=`

Examples:
- `JBL`
- `Flip, Charge`
- `>500`
- `<300`
- `=450`

If no products are found, the system displays a proper message.

---

### Authentication
Users can:
- register
- login
- logout
- view account details
- delete their account

Passwords are stored encrypted and never in plain text.

---

### Favorites
Logged-in users can:
- add items to favorites
- remove items from favorites
- view favorite items in a dedicated page

Rules:
- each favorite item appears only once
- favorites are saved in the database
- favorites remain after logout/login
- only logged-in users can use favorites

---

### Orders
The platform supports two order statuses:
- `TEMP`
- `CLOSE`

Rules:
- each user can have only one TEMP order
- adding the first item creates a TEMP order automatically
- users can add items to the TEMP order
- users can update quantities
- users can remove items
- if the TEMP order becomes empty, it is deleted
- purchasing closes the order
- closed orders appear in order history
- stock decreases only after purchase
- users cannot order more than the available stock

---

### Stock Management
Each product has stock information.

Rules:
- users cannot add more items than exist in stock
- out-of-stock items are shown with stock `0`
- if stock is `0`, the user cannot add the item to the order
- stock updates happen only on successful purchase

---

### Chat Assistant
The system includes a chat assistant for store products.

Features:
- answers questions about products in the store
- uses store catalog data before generating responses
- limited number of prompts per session

---

## Project Structure

```text
shopping-backend-microservices/
│
├── docker-compose.yml
├── README.md
├── .env
│
├── user-service/
│   ├── .env
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── exceptions.py
│       ├── controller/
│       ├── service/
│       ├── repository/
│       ├── model/
│       └── resources/db-migrations/
│
├── store-service/
│   ├── .env
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── exceptions.py
│       ├── controller/
│       ├── service/
│       ├── repository/
│       ├── model/
│       ├── scripts/
│       └── resources/db-migrations/
│
└── streamlit-app/
    ├── .env
    ├── Dockerfile
    ├── requirements.txt
    ├── app.py
    ├── pages/
    └── services/
