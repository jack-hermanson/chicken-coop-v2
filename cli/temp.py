from application import create_app
from application.modules.shifts.services.generate_shifts import generate_shifts

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        generate_shifts()
