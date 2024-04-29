# Pizza Order Management API

This is a RESTful API for managing pizza orders.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/consolenine/pizza_delivery_app.git
    ```

2. Navigate to the project directory:

    ```bash
    cd pizza_delivery_app
    ```

3. Build the Docker image:

    ```bash
    docker-compose build
    ```

4. Run the Docker container:

    ```bash
    docker-compose up -d
    ```

5. The API should now be accessible at `http://localhost:8080`.

6. Run Alembic Migrations.
    ```bash
    docker-compose run web alembic upgrade head
    ```
7. You are all set now!

## API Documentation

For detailed API documentation, please refer to the [API Documentation](http://localhost:8080/docs) file.