from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.testclient import TestClient

from mcp.server.fastmcp import FastMCP


def exercise_routes() -> None:
    """Log basic transport responses for sanity checks."""
    mcp = FastMCP("Taiga MCP", sse_path="/", streamable_http_path="/")
    app = Starlette(
        routes=[
            Route("/", lambda request: None),
            Mount("/sse", app=mcp.sse_app(mount_path="/sse")),
            Mount("/mcp", app=mcp.streamable_http_app()),
        ]
    )

    client = TestClient(app)

    resp = client.get("/sse", headers={"accept": "text/event-stream"})
    print("GET /sse ->", resp.status_code, "history", [r.status_code for r in resp.history])

    head = client.head("/sse", headers={"accept": "text/event-stream"})
    print("HEAD /sse ->", head.status_code, "history", [r.status_code for r in head.history])

    post = client.post("/mcp", json={})
    print("POST /mcp ->", post.status_code, "history", [r.status_code for r in post.history])


if __name__ == "__main__":
    exercise_routes()
