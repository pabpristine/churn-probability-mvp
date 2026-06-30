from fastapi import FastAPI

app = FastAPI(
    title="Dirt2Dollar Framework",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Dirt2Dollar Framework Running Successfully"
    }