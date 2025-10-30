import os
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Taiga MCP", sse_path="/", streamable_http_path="/")
# Prebuild sub-apps so we can wire their lifespans into the parent Starlette app.
sse_subapp = mcp.sse_app(mount_path="/sse")
streamable_http_subapp = mcp.streamable_http_app()
streamable_http_subapp.router.redirect_slashes = False


@streamable_http_subapp.middleware("http")
async def _normalize_blank_path(request, call_next):
    # Starlette mounts strip the trailing slash, leaving an empty path for "/mcp".
    # Ensure the downstream Streamable HTTP route sees the root path.
    if request.scope.get("path") == "":
        request.scope["path"] = "/"
        request.scope["raw_path"] = b"/"
    return await call_next(request)


@mcp.tool()
def echo(message: str) -> str:
    """Echo a message back to the caller."""
    return message


async def healthz(_):
    return PlainTextResponse("ok", status_code=200)


async def root(_):
    return PlainTextResponse("Taiga MCP up", status_code=200)

@asynccontextmanager
async def lifespan(_app):
    # The streamable HTTP transport requires its session manager task group to be running.
    async with mcp.session_manager.run():
        yield


# Mount the MCP streamable app under both /mcp and /mcp/ so proxies that normalize
# paths differently will still carry the session headers through without a redirect.
app = Starlette(
    routes=[
        Route("/", root),
        Route("/healthz", healthz),
        Mount("/sse", app=sse_subapp),
        Mount("/mcp", app=streamable_http_subapp),
    ],
    lifespan=lifespan,
)
app.router.redirect_slashes = False


@app.middleware("http")
async def _rewrite_mcp_path(request, call_next):
    if request.scope.get("path") == "/mcp":
        request.scope["path"] = "/mcp/"
        request.scope["raw_path"] = b"/mcp/"
    return await call_next(request)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))