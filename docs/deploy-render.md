# Panduan Deploy Detail — GitHub Private + Render.com

Target akhir: kamu punya **1 URL publik** yang dashboard-nya bisa dibuka siapa saja, dan **1 URL MCP endpoint** yang bisa dipanggil AI/Inspector dari mana saja — tanpa perlu share repo GitHub ke siapa pun.

---

## BAGIAN 1 — Push ke GitHub (Private)

### 1.1 Buat Repo di GitHub

1. Buka [github.com](https://github.com), login.
2. Klik ikon **+** di pojok kanan atas → **New repository**.
3. **Repository name**: `robocar-mcp`.
4. Pilih **Private** (bukan Public).
5. **Jangan** centang "Add a README file" (kode kita sudah punya README sendiri).
6. Klik **Create repository**.
7. Di halaman berikutnya, GitHub kasih URL repo, formatnya:
   ```
   https://github.com/<username-kamu>/robocar-mcp.git
   ```
   Simpan/copy URL ini.

### 1.2 Siapkan Autentikasi (Personal Access Token)

GitHub sudah tidak menerima password biasa buat `git push` lewat HTTPS. Perlu **Personal Access Token (PAT)**:

1. Di GitHub, klik foto profil (kanan atas) → **Settings**.
2. Scroll ke bawah sidebar kiri → **Developer settings**.
3. **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**.
4. **Note**: isi bebas, misal `robocar-mcp-deploy`.
5. **Expiration**: pilih sesuai kebutuhan (misal 90 days).
6. Centang scope **repo** (semua sub-item di bawahnya ikut tercentang otomatis).
7. Klik **Generate token** di bagian bawah.
8. **Copy token yang muncul sekarang juga** — token ini cuma ditampilkan sekali, gak akan kelihatan lagi setelah reload halaman. Simpan sementara di Notepad.

### 1.3 Push Kode dari Terminal

Buka terminal, masuk ke folder `robocar-mcp` hasil extract zip:

```bash
cd path/ke/robocar-mcp
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/<username-kamu>/robocar-mcp.git
git push -u origin main
```

Begitu `git push` dijalankan:
- Kalau diminta **Username**: isi username GitHub kamu.
- Kalau diminta **Password**: isi **token PAT** dari langkah 1.2 (bukan password akun GitHub biasa).

Kalau berhasil, buka `https://github.com/<username-kamu>/robocar-mcp` — kode sudah ada di sana (statusnya **Private**, cuma kamu yang bisa lihat).

**Kalau `git` belum dikenali di terminal**: install dulu dari [git-scm.com/downloads](https://git-scm.com/downloads), restart terminal, ulangi dari `git init`.

---

## BAGIAN 2 — Deploy ke Render.com

### 2.1 Daftar Akun Render

1. Buka [render.com](https://render.com) → **Get Started**.
2. Pilih **Sign up with GitHub** (paling gampang, langsung terhubung).
3. Authorize Render buat akses akun GitHub kamu.
4. Render akan minta izin akses repo — pilih **Only select repositories** → pilih `robocar-mcp` (biar Render gak dikasih akses ke repo lain kamu).

### 2.2 Deploy Lewat Blueprint (`render.yaml`)

Karena repo sudah ada file `render.yaml`, Render bisa baca konfigurasinya otomatis:

1. Di dashboard Render, klik **New +** (kanan atas) → **Blueprint**.
2. Pilih repo `robocar-mcp` dari daftar.
3. Render otomatis mendeteksi `render.yaml` dan menampilkan preview service `robocar-mcp` dengan:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m mcp_server.server_http`
   - **Plan**: Free
4. Klik **Apply** (atau **Create New Resources**, tergantung versi UI Render saat ini).
5. Render mulai proses **build** — bisa dipantau lewat tab **Logs**, biasanya 1-3 menit.

**Kalau Render tidak mendeteksi `render.yaml` otomatis**, deploy manual:
1. **New +** → **Web Service** → pilih repo `robocar-mcp`.
2. **Name**: `robocar-mcp` (bebas).
3. **Runtime**: Python 3.
4. **Build Command**: `pip install -r requirements.txt`.
5. **Start Command**: `python -m mcp_server.server_http`.
6. **Instance Type**: Free.
7. Klik **Create Web Service**.

### 2.3 Cek Build Berhasil

Di tab **Logs**, tunggu sampai muncul baris seperti:
```
==> Your service is live 🎉
```
Kalau muncul error di log (misal `ModuleNotFoundError`), cek apakah `requirements.txt` ada di root repo dan isinya benar (`mcp`, `fastapi`, `uvicorn`, `httpx`).

### 2.4 Ambil URL Publik

Di bagian atas halaman service (dekat nama service), ada URL formatnya:
```
https://robocar-mcp-xxxx.onrender.com
```
(`xxxx` random, sesuai yang di-generate Render). Klik/copy URL itu.

---

## BAGIAN 3 — Verifikasi Endpoint

Buka 3 hal ini buat mastiin semua jalan (ganti `robocar-mcp-xxxx.onrender.com` dengan URL kamu sendiri):

| Cek | URL | Hasil yang diharapkan |
|---|---|---|
| Dashboard | `https://robocar-mcp-xxxx.onrender.com` | Halaman dengan canvas + segitiga hijau |
| State API | `https://robocar-mcp-xxxx.onrender.com/state` | JSON: `{"x":0.0,"y":0.0,...}` |
| MCP endpoint | `https://robocar-mcp-xxxx.onrender.com/mcp-app/mcp` | Response (bukan 404) — ini path yang dipakai MCP client |

**Test manggil tool dari MCP Inspector (dari komputer lokal manapun):**

```bash
npx @modelcontextprotocol/inspector
```

Di Inspector: pilih transport **Streamable HTTP**, isi URL dengan `https://robocar-mcp-xxxx.onrender.com/mcp-app/mcp`, klik **Connect**, buka tab **Tools**, panggil `move_forward` — lalu buka tab dashboard di browser, posisi robocar harus ikut berubah.

**Request pertama bisa lambat (~30-60 detik)** kalau service baru "bangun" dari idle (tier gratis) — ini normal, bukan error, tunggu saja sampai response muncul.

---

## BAGIAN 4 — Update Kode di Kemudian Hari

Setiap ada perubahan kode:
```bash
git add .
git commit -m "update: <deskripsi perubahan>"
git push
```
Render otomatis re-deploy versi terbaru setiap `push` ke branch `main` — tidak perlu setting ulang.

---

## Troubleshooting

| Gejala | Penyebab | Solusi |
|---|---|---|
| `git push` minta password terus ditolak | Pakai password akun, bukan token | Ulangi pakai PAT dari langkah 1.2 |
| Build gagal di Render, `ModuleNotFoundError` | `requirements.txt` tidak lengkap/tidak ke-push | Cek isi `requirements.txt`, pastikan sudah ke-commit dan push |
| URL dashboard error 404 / not found | Build belum selesai, atau start command salah | Cek tab Logs Render, pastikan start command `python -m mcp_server.server_http` |
| Response pertama lambat banget | Cold start (tier gratis idle 15 menit) | Tunggu 30-60 detik, request kedua akan cepat |
| MCP Inspector gagal connect ke URL Render | Salah path, atau lupa `/mcp-app/mcp` di akhir URL | Pastikan URL lengkap sampai `/mcp-app/mcp` |
