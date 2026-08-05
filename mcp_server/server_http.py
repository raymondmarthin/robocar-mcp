import contextlib
import os

import uvicorn

from .api import api
from .tools import mcp

mcp_app = mcp.streamable_http_app()
api.mount("/mcp-app", mcp_app)

_original_lifespan = api.router.lifespan_context


@contextlib.asynccontextmanager
async def _combined_lifespan(app):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp_app.router.lifespan_context(mcp_app))
        async with _original_lifespan(app):
            yield


api.router.lifespan_context = _combined_lifespan

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(api, host="0.0.0.0", port=port)
