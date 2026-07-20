from app import create_app
from app.extensions import db
from app.models.role import Role
from app.models.user import User

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
