# Dukpyra Example - Python Web API
import dukpyra

app = dukpyra.app()

@app.get("/")
def home():
    return {"message": "Hello from Dukpyra!", "version": "1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": 1234567890}

@app.post("/api/users")
def create_user():
    return {"id": 1, "name": "John Doe", "created": "true"}
