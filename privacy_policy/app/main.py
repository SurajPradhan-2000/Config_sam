from fastapi import FastAPI
from mangum import Mangum  # Required for AWS Lambda
from app.api.databases import get_db_connection
from app.api.routes import privacy

app = FastAPI()

# Include Language Routes
app.include_router(privacy.router)


handler = Mangum(app)
