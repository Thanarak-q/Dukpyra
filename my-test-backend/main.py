# Dukpyra Example - Request Body Support
import dukpyra

app = dukpyra.app()

class CreateUser:
    name: str
    email: str
    age: int

class UpdateProduct:
    title: str
    price: float

@app.get("/")
def home():
    return {"message": "Dukpyra with Request Bodies!"}

@app.post("/users")
def create_user(body: CreateUser):
    return {"created": True, "name": body.name, "email": body.email}

@app.put("/products/{id}")
def update_product(id: int, body: UpdateProduct):
    return {"id": id, "title": body.title, "price": body.price, "updated": True}

@app.get("/health")
def health():
    return {"status": "ok"}
