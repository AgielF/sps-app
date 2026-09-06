#!/bin/bash

# Warna untuk output terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Menjalankan SPS App (Frontend & Backend) ===${NC}\n"

# Load NVM otomatis jika ada, agar NPM terdeteksi di dalam script ini
if [ -d "$HOME/.config/nvm" ]; then
    export NVM_DIR="$HOME/.config/nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
elif [ -d "$HOME/.nvm" ]; then
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi

# Fungsi untuk mengecek ketersediaan perintah (command)
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. Deteksi Python (python3 atau python)
if command_exists python3; then
    PY_CMD="python3"
elif command_exists python; then
    PY_CMD="python"
else
    echo -e "${RED}[ERROR] Python tidak ditemukan! Harap instal Python terlebih dahulu.${NC}"
    exit 1
fi

# Variabel untuk menampung PID proses
BACKEND_PID=""
FRONTEND_PID=""

# 2. Jalankan Backend
echo -e "${BLUE}[BACKEND] Menjalankan API Flask...${NC}"
cd sps-app || exit

# Setup venv jika belum ada
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[BACKEND] Membuat virtual environment (venv)...${NC}"
    $PY_CMD -m venv venv
    echo -e "${YELLOW}[BACKEND] Menginstal dependensi Python...${NC}"
    
    # OS dinamis (Windows vs Linux/Mac)
    if [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    pip install -r requirements.txt
else
    if [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
fi

$PY_CMD app.py &
BACKEND_PID=$!
cd ..

# 3. Cek dependensi Frontend (NPM)
if command_exists npm; then
    echo -e "${GREEN}[FRONTEND] Menjalankan Server Quasar/Vue...${NC}"
    cd Frontend-Apk-Sampah-Ifter || exit
    
    # Cek apakah node_modules sudah ada
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}[FRONTEND] Menginstal dependensi NPM...${NC}"
        npm install
    fi
    
    npm run dev &
    FRONTEND_PID=$!
    cd ..
else
    echo -e "\n${RED}[WARNING] NPM tidak ditemukan! Frontend gagal dijalankan.${NC}"
    echo -e "${RED}Silakan instal Node.js dan NPM (misalnya via nvm) untuk menjalankan Frontend.${NC}"
fi

echo -e "\n${YELLOW}>> Proses telah dimulai. Tekan CTRL+C untuk menghentikan semuanya. <<${NC}\n"

# 4. Fungsi untuk mematikan proses saat CTRL+C
cleanup() {
    echo -e "\n${YELLOW}Mematikan proses yang berjalan...${NC}"
    if [ -n "$BACKEND_PID" ]; then kill $BACKEND_PID 2>/dev/null; fi
    if [ -n "$FRONTEND_PID" ]; then kill $FRONTEND_PID 2>/dev/null; fi
    exit
}

trap cleanup SIGINT SIGTERM

# Tunggu proses selesai
if [ -n "$BACKEND_PID" ] && [ -n "$FRONTEND_PID" ]; then
    wait $BACKEND_PID $FRONTEND_PID
elif [ -n "$BACKEND_PID" ]; then
    wait $BACKEND_PID
elif [ -n "$FRONTEND_PID" ]; then
    wait $FRONTEND_PID
fi
