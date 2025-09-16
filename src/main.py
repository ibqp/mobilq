from fastapi import FastAPI
from src.api import root_router
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="Telco Products API"
    , docs_url=None     # /docs
    , redoc_url=None    # /redoc
    , openapi_url=None  # /openapi.json
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(root_router)


# uvicorn src.main:app --host 0.0.0.0 --port 8000
# python -m src.main
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
