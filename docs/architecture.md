# Arsitektur — RoboCar MCP Server (Opsi A)

## Ruang Lingkup

Proyek ini membangun MCP Server untuk RoboCar tanpa integrasi hardware
langsung. Validasi dilakukan lewat client simulator yang merepresentasikan
device sebagai data (posisi, arah, baterai), bukan gerakan motor fisik.

## Diagram Alur

```
[AI / MCP Host]
      |  MCP protocol (stdio)
      v
[mcp_server/server.py]
      |
      +-- [mcp_server/tools.py]  --tool call--> [mcp_server/state.py] (RobocarState)
      |                                                 ^
      +-- [mcp_server/api.py] (FastAPI, HTTP) ----------+
                  |  GET /state, GET /commands
                  v
      [client_simulator/simulator.py]  (polling tiap 1 detik)
```

## Komponen

- **state.py** — satu-satunya sumber kebenaran (single source of truth)
  untuk state robocar dan log command. Dipakai bareng oleh `tools.py` dan
  `api.py` lewat singleton `robocar_state`.
- **tools.py** — mendefinisikan tools yang diekspos ke AI host lewat MCP
  protocol. Tiap tool cuma manggil `state.apply_command(...)`, tidak
  nyimpen state sendiri.
- **api.py** — lapisan REST supaya client simulator bisa narik data tanpa
  perlu ngomong MCP protocol langsung.
- **server.py** — entrypoint yang jalanin API (thread terpisah, port 8000)
  dan MCP server (stdio, thread utama) dalam satu proses, supaya keduanya
  share instance `robocar_state` yang sama.
- **simulator.py** — proses terpisah yang berperan sebagai device. Polling
  `GET /commands?since_id=` tiap 1 detik, update representasi lokal, dan
  render ke console.

## Skema Data

State:
```json
{ "x": 0.0, "y": 0.0, "heading": 0.0, "speed": 0.0, "battery": 100.0 }
```

Command log entry:
```json
{
  "id": 1,
  "timestamp": 1234567890.12,
  "tool": "move_forward",
  "params": { "distance": 5 },
  "result_state": { "x": 5.0, "y": 0.0, "heading": 0.0, "speed": 5.0, "battery": 97.5 }
}
```

## Batasan

- Tidak ada koneksi ke hardware fisik (motor, sensor, board robocar).
- State disimpan in-memory — reset tiap kali `server.py` di-restart.
- Testing dilakukan lewat MCP Inspector dan client simulator, bukan device
  asli.
