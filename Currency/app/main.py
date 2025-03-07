from fastapi import FastAPI
from mangum import Mangum
from app.api.routes import currency
from app.api.databases import get_db_connection

app = FastAPI()
app.include_router(currency.router)

# Conditionally add Mangum handler for AWS Lambda
handler = Mangum(app)  # Required for AWS Lambda
