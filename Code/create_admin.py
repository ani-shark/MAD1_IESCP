from app import create_app, db
from app.models import User, Admin
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create an admin user
    username = "admin"
    email = "admin@example.com"
    password = "iadmin"
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    admin_user = User(username=username, email=email, password=hashed_password, role='admin')
    db.session.add(admin_user)
    db.session.commit()

    # Link the user to the Admin model
    admin = Admin(user_id=admin_user.id)
    db.session.add(admin)
    db.session.commit()

    print("Admin user created successfully!")
