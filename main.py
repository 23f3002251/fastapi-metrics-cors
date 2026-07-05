import time
import uuid
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. CORS Middleware 
# Strict enforcement: Only the assigned origin gets the Access-Control-Allow-Origin header
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dash-akrvb4.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"], 
    allow_headers=["*"],
)

# 2. Custom Headers Middleware
# This wraps every request (including preflights) to inject the required metrics
@app.middleware("http")
async def add_metrics_headers(request: Request, call_next):
    start_time = time.perf_counter()
    
    # Generate the unique identifier for the request
    request_id = str(uuid.uuid4())
    
    # Process the actual request
    response = await call_next(request)
    
    # Calculate duration
    process_time = time.perf_counter() - start_time
    
    # Inject required headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    
    return response

# 3. The Stats Endpoint
@app.get("/stats")
def get_stats(values: str = Query(...)):
    # Parse the comma-separated integers
    try:
        ints = [int(v.strip()) for v in values.split(",") if v.strip()]
    except ValueError:
        return {"error": "Invalid input. Only comma-separated integers are allowed."}

    count = len(ints)
    total = sum(ints)
    
    return {
        "email": "23f3002251@ds.study.iitm.ac.in", 
        "count": count,
        "sum": total,
        "min": min(ints),
        "max": max(ints),
        "mean": total / count
    }
