import contextlib
import os

import uvicorn
from mcp.server.transport_security import TransportSecuritySettings

from .api import api
from .tools import mcp

# enable_dns_rebinding_protection=False: server ini memang sengaja di-deploy
# publik (Render/Colab), jadi proteksi DNS-rebinding (yang didesain buat
# server dev lokal) perlu dimatikan supaya client dari domain manapun
# (misal web-based MCP Inspector) bisa connect.
mcp_app = mcp.streamable_http_app(
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False)
)
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
