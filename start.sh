#!/bin/bash

# Warna untuk output terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Menjalankan SPS App (Frontend & Backend) ===${NC}\n"

# 1. Jalankan Backend
echo -e "${BLUE}[BACKEND] Menjalankan API Flask...${NC}"
cd sps-app

# Setup venv jika belum ada
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[BACKEND] Membuat virtual environment (venv)...${NC}"
    python3 -m venv venv
    echo -e "${YELLOW}[BACKEND] Menginstal dependensi Python...${NC}"
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

python3 app.py &
BACKEND_PID=$!
cd ..

# 2. Jalankan Frontend
echo -e "${GREEN}[FRONTEND] Menjalankan Server Quasar/Vue...${NC}"
cd Frontend-Apk-Sampah-Ifter
# Cek apakah node_modules sudah ada, jika belum otomatis install
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}[FRONTEND] Menginstal dependensi NPM...${NC}"
    npm install
fi
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "\n${YELLOW}>> Kedua server sedang berjalan. Tekan CTRL+C untuk menghentikan semuanya. <<${NC}\n"

# Fungsi untuk mematikan kedua proses saat user menekan CTRL+C
cleanup() {
    echo -e "\n${YELLOW}Mematikan server frontend dan backend...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Tangkap signal interrupt (CTRL+C)
trap cleanup SIGINT SIGTERM

# Tunggu proses selesai (infinite loop sampai diclose user)
wait $BACKEND_PID $FRONTEND_PID
