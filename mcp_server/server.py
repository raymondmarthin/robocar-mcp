import threading

import uvicorn

from .api import api
from .tools import mcp

API_HOST = "127.0.0.1"
API_PORT = 8000


def run_api() -> None:
    uvicorn.run(api, host=API_HOST, port=API_PORT, log_level="warning")


def main() -> None:
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    print(f"[robocar-mcp] REST API jalan di http://{API_HOST}:{API_PORT}")
    print("[robocar-mcp] MCP server starting (stdio transport)...")
    mcp.run()


if __name__ == "__main__":
    main()
