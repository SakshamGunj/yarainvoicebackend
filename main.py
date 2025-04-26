from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from .pdf_service import generate_pdf
from .invoice_generator import generate_invoice_html

app = FastAPI(title="Invoice Generator API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Item(BaseModel):
    name: str
    qty: int
    price: float

class Company(BaseModel):
    name: str
    address: str
    phone: str
    gst: str

class Client(BaseModel):
    name: str
    address: str
    gst: Optional[str] = None

class Invoice(BaseModel):
    number: str
    date: str
    taxRate: float
    advancePayment: float = 0.0

class InvoiceData(BaseModel):
    company: Company
    client: Client
    invoice: Invoice
    items: List[Item]
    notes: str
    bankDetails: str

@app.post("/generate-pdf")
async def create_pdf(data: InvoiceData):
    try:
        # Generate HTML
        html_content = generate_invoice_html(data.dict())
        
        # Generate PDF
        pdf_content = await generate_pdf(html_content)
        
        # Create response with PDF file
        filename = f"{data.company.name}_Invoice_{data.invoice.number}.pdf"
        
        response = Response(content=pdf_content)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
