from fastapi import FastAPI
from mangum import Mangum  # Required for AWS Lambda
from app.api.databases import get_db_connection
from app.api.routes import terms

app = FastAPI()

# Include Language Routes
app.include_router(terms.router)


handler = Mangum(app)
