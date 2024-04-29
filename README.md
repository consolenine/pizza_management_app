# Pizza Order Management API

This is a RESTful API for managing pizza orders.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/consolenine/pizza_management_app.git
    ```

2. Navigate to the project directory:

    ```bash
    cd pizza_delivery_app/backend
    ```

3. Build the Docker image:

    ```bash
    docker-compose build
    ```

4. Run the Docker container:

    ```bash
    docker-compose up -d
    ```

5. The API should now be accessible at `http://localhost:8008`.

6. Run Alembic Migrations.
    ```bash
    docker-compose run api alembic upgrade head
    ```
7. You are all set now!

## API Documentation

For detailed API documentation, please refer to the [API Documentation](http://localhost:8008/docs) file.

## Connect To Database
1. Fire up a new terminal and run
    ```bash
    psql -h 127.0.0.1 -p 5432 -U pizza_manager -d pizza_db
    ```
## Next Steps!
*Alternatively, the following can be done via direct API calls as well using your preferred methods.* **Just visit the docs and check request and response parameters**

### Create An Admin User

- The first thing we need is to send an API request to create a new admin user for transactions.
- Go to http://localhost:8080/docs
- Find the endpoint `/api/v1/admin/user/admincreate`
- Click on Try it out
- Fill the required fields.
- **TIP** - Copy app secret from **docker-compose.yml** file and paste in app_secret value

### Authenticate User

- Go to http://localhost:8080/docs
- Click on authorize
- Now input the admin email and password you used earlier.
- Click on submit
- You can now perform admin actions (create pizza, delete users, etc)

# Good Luck! 

You are all set to add pizzas, register new users as customers, place orders and a lot more!


