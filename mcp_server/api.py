from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .dashboard import DASHBOARD_HTML
from .state import robocar_state

api = FastAPI(title="RoboCar MCP API")

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["mcp-session-id"],
)


@api.get("/", response_class=HTMLResponse)
def dashboard():
    return DASHBOARD_HTML


@api.get("/state")
def get_state():
    return robocar_state.get_state()


@api.get("/commands")
def get_commands(since_id: int = Query(0, description="Command dengan id lebih besar dari nilai ini")):
    return robocar_state.get_commands_since(since_id)
