# Simple API Example

@app.get("/")
def home():
    return {"message": "Welcome to Dukpyra API", "version": "1.0"}

@app.get("/users")
def list_users():
    return {"users": ["Alice", "Bob", "Charlie"], "count": 3}

@app.post("/users")
def create_user():
    return {"id": 1, "name": "New User", "created": "true"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "uptime": 12345}
