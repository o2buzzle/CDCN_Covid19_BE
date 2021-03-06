import fastapi
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes import ner_routes, ocr_routes

app.include_router(ner_routes.router, prefix="/ner")
app.include_router(ocr_routes.router, prefix="/ocr")
