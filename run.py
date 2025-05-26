import os
from app import create_app, db
from flask_migrate import Migrate, upgrade, migrate, init
from sqlalchemy.exc import OperationalError

app = create_app()
migrate_obj = Migrate(app, db)


def auto_migrate():
  with app.app_context():
    # Nếu thư mục migrations chưa tồn tại, khởi tạo nó
    if not os.path.exists('migrations'):
      init()
      print("[Flask-Migrate] Initialized migrations folder.")

    try:
      migrate(message="auto migrate")
      print("[Flask-Migrate] Migration generated.")
      upgrade()
      print("[Flask-Migrate] Database upgraded.")
    except OperationalError as e:
      print(f"[Flask-Migrate] Database error: {e}")
    except Exception as e:
      print(f"[Flask-Migrate] Unexpected error: {e}")


if __name__ == '__main__':
  auto_migrate()
  app.run(debug=True)