# Import the 'create_engine' function from SQLAlchemy, which is used to establish the actual connection to the database.
from sqlalchemy import create_engine

# Import 'declarative_base' which is used to create a base class. Our database models (like User, Post, etc.) will inherit from this class.
from sqlalchemy.ext.declarative import declarative_base

# Import 'sessionmaker' which is a factory class that creates new database Session objects to interact with the database.
from sqlalchemy.orm import sessionmaker

# Define the connection URL for the SQLite database. This tells SQLAlchemy to use SQLite and create a file named 'blog.db' in the current directory.
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# Create the SQLAlchemy engine. The engine is the entry point to the database (it handles the connection pool and SQL execution).
engine = create_engine(
    # Pass the database URL. 'connect_args={"check_same_thread": False}' is required ONLY for SQLite 
    # because SQLite by default only allows one thread to communicate with it, but FastAPI can make requests on multiple threads.
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class. Each instance of SessionLocal will be a unique database session.
# - autocommit=False: We want to manually commit transactions (save changes) using db.commit().
# - autoflush=False: We don't want SQLAlchemy to automatically send changes to the database before we query.
# - bind=engine: Bind this session factory to the database engine we created above.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the Base class. We will inherit from this class when creating database models so SQLAlchemy knows they map to database tables.
Base = declarative_base()


# Define a generator function 'get_db' to handle database sessions for our FastAPI routes.
def get_db():
    # Open a new database session.
    db = SessionLocal()
    try:
        # 'yield' provides the database session ('db') to the route that requested it, and temporarily pauses here.
        yield db
    finally:
        # After the route finishes executing and sends the response, the code resumes here and closes the session to free up resources.
        db.close()

