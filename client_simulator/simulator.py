import time

import httpx

API_BASE = "http://127.0.0.1:8000"
POLL_INTERVAL = 1.0


def render_state(state: dict) -> None:
    print(
        f"[simulator] pos=({state['x']:.2f}, {state['y']:.2f}) "
        f"heading={state['heading']:.1f} speed={state['speed']} "
        f"battery={state['battery']:.1f}%"
    )


def main() -> None:
    last_id = 0
    print(f"[simulator] Menyambung ke {API_BASE} ...")
    with httpx.Client(timeout=5.0) as client:
        while True:
            try:
                resp = client.get(f"{API_BASE}/commands", params={"since_id": last_id})
                resp.raise_for_status()
                commands = resp.json()
                for cmd in commands:
                    print(f"[simulator] Command #{cmd['id']}: {cmd['tool']}({cmd['params']})")
                    render_state(cmd["result_state"])
                    last_id = cmd["id"]
            except httpx.HTTPError as e:
                print(f"[simulator] Gagal konek ke MCP Server API: {e}")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
