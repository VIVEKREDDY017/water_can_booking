class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Chinnu12%3F@127.0.0.1:5432/water_can_app'  # Ensure this is correct
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = '441c57d296fa7518e19c580629b2f709'  # Use a secure, secret key
