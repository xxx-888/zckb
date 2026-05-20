"""
FastAPI application entry point for the spider service.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router
from app.core.config import settings
from app.core.logger import get_logger, setup_logging

logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    logger.info("Starting up spider service")
    setup_logging()
    yield
    # Shutdown
    logger.info("Shutting down spider service")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Review Spider Service",
        description="Distributed review spider service for multiple e-commerce platforms",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(router)

    return app


# Create application instance
app = create_app()


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "service": "Review Spider Service",
        "version": "0.1.0",
        "docs": "/docs",
    }


def main() -> None:
    """Main entry point for running the application."""
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.log_level == "DEBUG",
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
