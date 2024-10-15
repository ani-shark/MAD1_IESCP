This project is a web-based platform that connects sponsors with influencers to facilitate marketing campaigns.
Sponsors can create and manage campaigns, while influencers can respond to ad requests and manage their profiles.
The platform also includes an admin role for overseeing the entire system.

Before you can run this project, make sure you have the following installed on your system:
- Python 3.8 or later
- pip (Python package installer)
- Virtual environment (optional but recommended)

Navigate to the project directory:
    cd IeScp

Set Up the Virtual Environment (Optional)
It’s recommended to run the project in a virtual environment.
To create and activate a virtual environment, use the following commands:
    python3 -m venv mad_env
    source mad_env/bin/activate

Install the necessary packages listed in `requirements.txt`:
    pip install -r requirements.txt

Set Up the Database
To set up the database, follow these steps:
- Initialize the database with the necessary tables:
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade

Run the Application, start the flask development server locally:
    python run.py (or) flask run


The application will be available at `http://127.0.0.1:5000/` in your web browser.

Accessing the Application
Once the server is running, you can access the application and log in as a sponsor, influencer, or admin by creating an account or using existing credentials (if any).

Additional Notes
- Environment Variables: Ensure that any necessary environment variables (like `FLASK_APP` or `FLASK_ENV`) are correctly set in your environment.
- Admin Account: To create an admin account, you can manually add a user with the role 'admin' in the database or use the provided `create_admin.py` script.

API Endpoints
For details about the API endpoints available, please refer to the `api/resources.py` file.

Troubleshooting
- Virtual Environment Issues: If you encounter issues with the virtual environment, make sure it's activated before running any commands.
- Database Errors: If there are any database-related errors, you may need to delete the existing SQLite database file and rerun the migration commands.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Special thanks to all the contributors and those who provided guidance throughout the development of this project.


<<Admin Login Data>>
username: admin
passwrod: iadmin
