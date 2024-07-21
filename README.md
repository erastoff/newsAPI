## NewsAPI App

### Prerequisites

- Python 3.10+
- FastAPI 0.111.1+
- beautifulsoup4 4.12.3+
- PostgreSQL
- Docker /Docker Compose

### Description

This project is a FastAPI application for parsing, storing, and retrieving news articles. The application is designed to be deployed using Docker and Docker Compose, ensuring a smooth setup and consistent environment for development and production.

### Features

- **FastAPI**: High-performance asynchronous web framework.
- **PostgreSQL**: Robust and scalable SQL database.
- **Docker**: Containerized deployment for easy setup and scalability.
- **Automatic Parsing**: Background tasks for periodically parsing and saving news articles.
- **Health Checks**: Ensures database readiness before the application starts.


### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/erastoff/newsAPI.git
   cd newsAPI

2. Create a `.env` file in the root directory and add the following environment variables:

```.env
DEBUG=True
DATABASE_NAME=mos_news_db
DATABASE_USER=mos_news_user
DATABASE_PASSWORD=mos_news_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

3. Build and start the application using Docker Compose:

```bash
# Run containers with the logs
docker-compose up --build

# Run containers in detached mode
docker-compose up -d

# Stop and remove the containers
docker-compose down --volumes
```

### Project Structure
- **app**: Contains the main application code including models, schemas, and background tasks.
- **Dockerfile**: Defines the Docker image for the FastAPI application.
- **docker-compose.yml**: Configuration for Docker Compose to run the application and database services.
- **.env**: Environment variables for configuring the database connection.

### Endpoints
- **GET /metro/news?day=`int`**: Retrieves news articles from the past `int` days.
- **Request**
```http request
http://0.0.0.0:8000/metro/news?day=5
```
- **Response**
```json
[
  {
    "title": "О реализации программы реновации в Академическом районе",
    "url": "http://mosday.ru/news/item.php?4857150&tags=metro",
    "image_url": "http://mosday.ru/news/preview/485/4857150.jpg",
    "published_at": "2024-04-23T15:52:00",
    "id": 1
  }
]
```

### Background Tasks
The application includes a background parser that periodically fetches and saves news articles. The interval for parsing is set to 600 seconds (10 minutes) by default.

