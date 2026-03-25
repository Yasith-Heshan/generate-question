class Settings:
    PROJECT_NAME: str = "Simple FastAPI App"
    VERSION: str = "1.0.0"

    JWT_SECRET_KEY: str = "supersecretkey123"  # change in production, set via ENV
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60

settings = Settings()
