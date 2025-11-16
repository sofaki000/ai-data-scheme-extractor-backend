from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI(title="AI Data Schema Extractor API")

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}


# Pydantic model to validate input
class EmailRequest(BaseModel):
    email: EmailStr


@app.post("/send-email/")
async def send_email(request: EmailRequest):
    email_address = request.email

    # Here, you can integrate your sending logic (SMTP, API, etc.)
    # For demo, we just print it
    print(f"Received email to send: {email_address}")

    # Simulate sending success
    return {"message": f"Email {email_address} received and processed successfully"}