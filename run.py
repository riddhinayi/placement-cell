from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    # Create admin user if not exists
    if not User.query.filter_by(email='admin@placement.com').first():
        admin = User(
            name     = 'Admin',
            email    = 'admin@placement.com',
            password = generate_password_hash('admin123'),
            role     = 'admin'
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created!')

    print('Database ready!')

if __name__ == '__main__':
    app.run(debug=True)