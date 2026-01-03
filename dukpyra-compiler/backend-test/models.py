import dukpyra
app = dukpyra.app()

class User:
    id: int
    name: str
    email: str
    active: bool

class Post:
    id: int
    title: str
    content: str
    author_id: int

class Comment:
    id: int
    post_id: int
    user_id: int
    text: str

class Product:
    id: int
    name: str
    price: float
    in_stock: bool
    category: str

class Order:
    id: int
    user_id: int
    total: float
    paid: bool

class Customer:
    id: int
    name: str
    email: str
    phone: str

@app.post("/api/v2/users")
def create_user_v2(user: User):
    return {"id": 1, "name": "Created User", "email": "user@example.com", "active": True, "message": "User created successfully"}

@app.post("/api/v2/posts")
def create_post_v2(post: Post):
    return {"id": 100, "title": "Created Post", "author_id": 1, "created": True}

@app.put("/api/v2/products/{id}")
def update_product(id: int, product: Product):
    return {"id": id, "name": "Updated Product", "price": 99.99, "updated": True}

@app.post("/api/v2/orders")
def create_order(order: Order):
    return {"id": 1, "user_id": 1, "total": 299.99, "paid": True, "created": True}

@app.post("/api/v2/customers")
def create_customer(customer: Customer):
    return {"id": 1, "name": "New Customer", "email": "customer@example.com", "registered": True}

@app.post("/api/v2/users/{user_id}/posts")
def create_user_post(user_id: int, post: Post):
    return {"user_id": user_id, "post_id": 1, "title": "New User Post", "created": True}

@app.put("/api/v2/customers/{customer_id}")
def update_customer(customer_id: int):
    return {"id": customer_id, "name": "Updated Customer", "updated": True}
