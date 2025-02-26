
```markdown
# Library Management System

This is a Django REST Framework (DRF) application for managing books and loans in a library. It includes features like user authentication, book management, and loan tracking.

## Features

- **User Roles**:
  - Anonymous users can browse books.
  - Registered users can borrow and return books.
  - Admins can add/remove books and manage users.
- **Authentication**:
  - JWT authentication for secure API access.
- **Database**:
  - PostgreSQL for production and development.
- **API Documentation**:
  - Swagger UI for interactive API documentation.
- **Docker**:
  - The project is containerized using Docker for easy setup and deployment.

## Prerequisites

- Docker (mandatory)
- Docker Compose (mandatory)
- Git

---

## Running the Project with Docker

### 1. Install Docker and Docker Compose

Download and install Docker and Docker Compose from [here](https://www.docker.com/get-started).

### 2. Clone the Repository

```bash
git clone https://github.com/joshuagr33n/library-management.git
cd library-management
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory or run the following command:


```bash
cp .env.example .env
```

and add the following:

```
DB_NAME=library_management
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Django settings
SECRET_KEY=your-secret-key
DEBUG=True

# Heroku settings (if applicable)
DATABASE_URL=your-database-url
```

### 4. Build and Run the Docker Containers

```bash
docker-compose up --build
```

This will:
- Build the Docker images.
- Start the PostgreSQL database.
- Run the Django application.

### 5. Access the Application

Visit `http://127.0.0.1:8000/` to access the API.

### 6. Run Migrations

Open a new terminal and run:

```bash
docker-compose exec web python manage.py migrate
```

### 7. Create a Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### 8. Stop the Docker Containers

To stop the containers, run:

```bash
docker-compose down
```

---

## API Documentation

You can explore and test the API using Swagger:

1. Run the Docker containers:
   ```bash
   docker-compose up
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/swagger/
   ```

---

## Deployment to Heroku

### 1. Install the Heroku CLI

Download and install the Heroku CLI from [here](https://devcenter.heroku.com/articles/heroku-cli).

### 2. Login to Heroku

```bash
heroku login
```

### 3. Create a New Heroku App

```bash
heroku create library-management-app
```

### 4. Set Environment Variables on Heroku

Set the required environment variables on Heroku:

```bash
heroku config:set DB_NAME=library_management
heroku config:set DB_USER=postgres
heroku config:set DB_PASSWORD=postgres
heroku config:set DB_HOST=localhost
heroku config:set DB_PORT=5432
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
```

### 5. Push Code to Heroku

```bash
git init
git add .
git commit -m "Initial commit"
git remote add heroku https://git.heroku.com/library-management-app.git
git push heroku master
```

### 6. Run Migrations on Heroku

```bash
heroku run python manage.py migrate
```

### 7. Create a Superuser on Heroku

```bash
heroku run python manage.py createsuperuser
```

### 8. Open Your App

```bash
heroku open
```

Visit your app URL (e.g., `https://library-management-app.herokuapp.com/`) to access the API.

---

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

---

### Docker Files

Here are the `Dockerfile` and `docker-compose.yml` files for reference:

#### `Dockerfile`

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "library_management.wsgi", "--bind", "0.0.0.0:8000"]
```

#### `docker-compose.yml`

```yaml
version: '3.8'

services:
  db:
    image: postgres:17
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: library_app_db
    volumes:
      - postgres_data:/var/lib/postgresql/data/

  web:
    build: .
    command: gunicorn library_management.wsgi --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DB_HOST: db
      DB_NAME: library_app_db
      DB_USER: postgres
      DB_PASSWORD: postgres

volumes:
  postgres_data:
```

---

