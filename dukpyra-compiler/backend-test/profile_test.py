# ============================================================================
# Dukpyra Runtime Type Collection Test
# ============================================================================
# This file demonstrates the FastAPI profiling feature

import dukpyra

app = dukpyra.app()

# Simple routes for testing runtime type collection

@app.get("/profile/user/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe"}

@app.post("/profile/create")
def create_item():
    return {"id": 1, "created": True}

@app.get("/profile/list")
def get_items():
    return {"items": [1, 2, 3, 4, 5]}
