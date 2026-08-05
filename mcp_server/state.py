import math
import threading
import time
from typing import Any, Dict, List


class RobocarState:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._state: Dict[str, Any] = {
            "x": 0.0,
            "y": 0.0,
            "heading": 0.0,
            "speed": 0.0,
            "battery": 100.0,
        }
        self._commands: List[Dict[str, Any]] = []
        self._next_id = 1

    def get_state(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._state)

    def apply_command(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            if tool_name == "move_forward":
                distance = float(params.get("distance", 0))
                rad = math.radians(self._state["heading"])
                self._state["x"] += distance * math.cos(rad)
                self._state["y"] += distance * math.sin(rad)
                self._state["speed"] = distance
                self._state["battery"] = max(0.0, self._state["battery"] - distance * 0.5)
            elif tool_name == "move_backward":
                distance = float(params.get("distance", 0))
                rad = math.radians(self._state["heading"])
                self._state["x"] -= distance * math.cos(rad)
                self._state["y"] -= distance * math.sin(rad)
                self._state["speed"] = -distance
                self._state["battery"] = max(0.0, self._state["battery"] - distance * 0.5)
            elif tool_name == "turn_left":
                degree = float(params.get("degree", 0))
                self._state["heading"] = (self._state["heading"] + degree) % 360
            elif tool_name == "turn_right":
                degree = float(params.get("degree", 0))
                self._state["heading"] = (self._state["heading"] - degree) % 360
            elif tool_name == "stop":
                self._state["speed"] = 0.0
            elif tool_name == "get_status":
                pass
            else:
                raise ValueError(f"Unknown tool: {tool_name}")

            entry = {
                "id": self._next_id,
                "timestamp": time.time(),
                "tool": tool_name,
                "params": params,
                "result_state": dict(self._state),
            }
            self._commands.append(entry)
            self._next_id += 1
            return entry

    def get_commands_since(self, since_id: int = 0) -> List[Dict[str, Any]]:
        with self._lock:
            return [c for c in self._commands if c["id"] > since_id]


robocar_state = RobocarState()
