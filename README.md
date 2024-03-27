## Conta Control API Python

This is an API project built with FastAPI for a system to manage accounts. It includes routes for authentication with encryption, user creation, user permission management (admin, stand, and premium), user management (create, update, get one, get all), and full account management (CRUD).

### Technologies Used

- **SQLAlchemy**
- **Alembic**
- **psycopg2_binary**
- **fastapi**
- **passlib**
- **uvicorn**
- **PyJWT**

### Key Features

- **Secure Authentication:** Implementation of authentication with encryption to ensure user information security.
- **User Management:** Routes to create, update, get one, get all users in the system.
- **Account Management:** Routes to create, update, get one, get all accounts for system users.
- **Permission Management:** Routes to define and verify user permissions (admin, stand, and premium).

### Running the Project

1. Install project dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Run the server:

   ```
   uvicorn main:app --reload
   ```

3. Access the API documentation at `http://localhost:8000/docs` to view and test available routes.

### How to Contribute

- Fork the project.
- Create a branch for your feature (`git checkout -b feature/FeatureName`).
- Commit your changes (`git commit -am 'Adding a new feature'`).
- Push to the branch (`git push origin feature/FeatureName`).
- Create a new Pull Request.

```

You can copy and paste this markdown content into your README file.
```
