from application import create_app
from application.modules.shifts.services.generate_shifts import generate_shifts
from application.modules.shifts.services.seed_shift_assignments import seed_shift_assignments

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_shift_assignments()
        generate_shifts()
