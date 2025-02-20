from app import create_app, db
from flask_migrate import Migrate


app = create_app()
migrate = Migrate(app, db)
app.secret_key = '441c57d296fa7518e19c580629b2f709'
if __name__ == "__main__":
    app.run(debug=True)
