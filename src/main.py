from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import traceback

app = FastAPI(
    title="Dirt2Dollar Framework",
    version="1.0.0"
)

logger = logging.getLogger(__name__)


@app.get("/")
def root():
    return {
        "message": "Dirt2Dollar Framework Running Successfully"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all FastAPI exception handler.

    DB logging is already done at the workflow level;
    this just ensures a clean HTTP 500 response and console log.
    """
    tb_str = "".join(
        traceback.format_exception(type(exc), exc, exc.__traceback__)
    )
    logger.error(
        "Unhandled error on %s %s: %s",
        request.method,
        request.url.path,
        tb_str,
    )

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )