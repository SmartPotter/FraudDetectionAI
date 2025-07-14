from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from app.routes import trace

from app.routes import upload, score, explain, block, blockchain, report, verify

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Walmart AI Fraud Prevention Platform",
    description="Enterprise-grade fraud detection and prevention system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all route modules
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(score.router, prefix="/api", tags=["Scoring"])
app.include_router(explain.router, prefix="/api", tags=["AI Explanation"])
app.include_router(block.router, prefix="/api", tags=["Blocklist"])
app.include_router(blockchain.router, prefix="/api", tags=["Blockchain"])
app.include_router(report.router, prefix="/api", tags=["Reports"])
app.include_router(verify.router, prefix="/api", tags=["Verification"])
app.include_router(trace.router, prefix="/api", tags=["Trace"])

@app.get("/")
async def root():
    return {"message": "Walmart AI Fraud Prevention Platform API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": os.getenv("ENVIRONMENT", "development")}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )