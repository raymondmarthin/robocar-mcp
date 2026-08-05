from mcp.server import MCPServer

from .state import robocar_state

mcp = MCPServer("robocar-mcp")


@mcp.tool()
def move_forward(distance: float) -> dict:
    """Gerakkan robocar maju sejauh `distance` unit."""
    entry = robocar_state.apply_command("move_forward", {"distance": distance})
    return entry["result_state"]


@mcp.tool()
def move_backward(distance: float) -> dict:
    """Gerakkan robocar mundur sejauh `distance` unit."""
    entry = robocar_state.apply_command("move_backward", {"distance": distance})
    return entry["result_state"]


@mcp.tool()
def turn_left(degree: float) -> dict:
    """Putar robocar ke kiri (berlawanan arah jarum jam) sejauh `degree` derajat."""
    entry = robocar_state.apply_command("turn_left", {"degree": degree})
    return entry["result_state"]


@mcp.tool()
def turn_right(degree: float) -> dict:
    """Putar robocar ke kanan (searah jarum jam) sejauh `degree` derajat."""
    entry = robocar_state.apply_command("turn_right", {"degree": degree})
    return entry["result_state"]


@mcp.tool()
def stop() -> dict:
    """Hentikan robocar (speed = 0)."""
    entry = robocar_state.apply_command("stop", {})
    return entry["result_state"]


@mcp.tool()
def get_status() -> dict:
    """Ambil state terkini robocar (posisi, arah, speed, baterai)."""
    entry = robocar_state.apply_command("get_status", {})
    return entry["result_state"]
