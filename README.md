# RoboCar MCP Server

MCP Server untuk RoboCar berbasis simulasi — tanpa integrasi hardware fisik. AI host (Claude Desktop / MCP Inspector) memanggil tools lewat MCP protocol, lalu sebuah client simulator merepresentasikan device robocar dan menampilkan pergerakannya secara visual di browser.

## Fitur

- 6 tools MCP: `move_forward`, `move_backward`, `turn_left`, `turn_right`, `stop`, `get_status`
- REST API buat client narik state/command
- Dashboard visual real-time di browser (canvas, jejak lintasan, info posisi)
- Client simulator berbasis polling, merepresentasikan device tanpa hardware asli

## Deploy ke Endpoint Publik (Render.com)

Kalau butuh endpoint yang bisa diakses dari luar (misal buat dosen/penilai tanpa share repo), lihat `docs/deploy-render.md` — pakai tier gratis Render, tinggal push ke GitHub (boleh private) dan connect lewat dashboard Render.

## Struktur Proyek

```
robocar-mcp/
├── mcp_server/
│   ├── state.py       # state + command log (in-memory)
│   ├── tools.py        # definisi tools MCP
│   ├── api.py           # REST API (FastAPI) + endpoint dashboard
│   ├── dashboard.py     # HTML+JS dashboard, disajikan lewat GET /
│   ├── server.py       # entrypoint lokal (MCP stdio + API bareng)
│   └── server_http.py  # entrypoint deployment (MCP streamable-http + API, satu port)
├── client_simulator/
│   └── simulator.py    # device pengganti, polling API
├── docs/
│   ├── architecture.md
│   └── deploy-render.md
├── robocar_mcp_colab.ipynb
├── render.yaml
├── requirements.txt
└── README.md
```

## Instalasi

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Cara Menjalankan

Server ini pakai transport stdio, jadi harus di-spawn langsung oleh MCP host (Inspector atau Claude Desktop) — bukan dijalankan manual di terminal terpisah.

### Skenario A — Testing pakai MCP Inspector

```bash
npx @modelcontextprotocol/inspector python -m mcp_server.server
```

Buka tab **Tools** di Inspector, panggil tool yang diinginkan. Opsional, jalankan client simulator di terminal lain buat log tambahan:

```bash
python -m client_simulator.simulator
```

### Skenario B — Connect ke Claude Desktop

Tambahkan ke `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "robocar": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/absolut/ke/robocar-mcp"
    }
  }
}
```

Restart Claude Desktop, lalu minta AI panggil tool robocar lewat chat.

## Dashboard Visual

Selagi salah satu skenario di atas jalan, buka browser ke:

```
http://127.0.0.1:8000
```

Canvas menampilkan posisi robocar real-time (segitiga hijau) beserta jejak lintasan dan info posisi/heading/battery.

## Daftar Tools MCP

| Tool | Parameter | Keterangan |
|---|---|---|
| `move_forward` | `distance: float` | Maju sejauh `distance` |
| `move_backward` | `distance: float` | Mundur sejauh `distance` |
| `turn_left` | `degree: float` | Belok kiri `degree` derajat |
| `turn_right` | `degree: float` | Belok kanan `degree` derajat |
| `stop` | - | Berhenti |
| `reset` | - | Kembalikan ke posisi awal (x=0, y=0, heading=0, battery=100) |
| `get_status` | - | Ambil state terkini |

## Endpoint REST API

| Endpoint | Keterangan |
|---|---|
| `GET /` | Dashboard visual |
| `GET /state` | State terbaru robocar |
| `GET /commands?since_id=<int>` | Command baru sejak `since_id` |

## Troubleshooting

| Gejala | Penyebab | Solusi |
|---|---|---|
| Dashboard/simulator gak ke-update | Ada 2 proses server jalan bersamaan | Pastikan cuma satu skenario (A atau B) yang aktif |
| Port 8000 bentrok | Proses lama masih jalan di background | Tutup semua proses `mcp_server.server`, ulang dari satu skenario |
| `ModuleNotFoundError` | venv belum aktif / dependency belum terinstall | Aktifkan venv, `pip install -r requirements.txt` |

## Catatan

Tidak ada integrasi hardware fisik. Semua "gerakan" robocar berupa perubahan state (x, y, heading, battery) yang direpresentasikan lewat dashboard dan client simulator.
