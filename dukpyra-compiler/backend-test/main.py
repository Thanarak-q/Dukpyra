import dukpyra
app = dukpyra.app()

@app.get("/")
def home():
    return {"message": "Hello from Dukpyra!"}

@app.get("/process-numbers")
def process_numbers(numbers: list):
    return [x * 2 for x in numbers]

@app.get("/filter-users")
def filter_users(users: list):
    return [u.name for u in users if u.active]
