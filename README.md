# ♻️ SPS App (Smart Payment System for Waste Management)

![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=flat-square&logo=vue.js)
![Quasar](https://img.shields.io/badge/Quasar-Framework-1976D2?style=flat-square&logo=quasar)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-API-000000?style=flat-square&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=flat-square&logo=mysql)
![Netlify](https://img.shields.io/badge/Netlify-Deployed-00C7B7?style=flat-square&logo=netlify)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

## 📖 Project Overview

The **SPS App (Smart Payment System for Waste Management)** is a comprehensive, full-stack platform designed to modernize and digitize waste collection. This repository contains the complete unified workspace, composed of two distinct services:
1. **Frontend (`Frontend-Apk-Sampah-Ifter`)**: A responsive, cross-platform web application built with Vue 3 and Quasar Framework.
2. **Backend (`sps-app`)**: A robust RESTful API built with Python and Flask.

The system connects citizens ("Warga"), waste collection officers ("Petugas"), and administrators. It facilitates reporting waste ready for pickup, scheduling operations, visualizing geographic locations, managing digital payments, and calculating officer compensation.

## ✨ Key Features

- **Role-Based Access Control (RBAC):** Secure JWT-based authentication tailoring the UI and API access for Admins, Citizens, and Officers.
- **Geographic Waste Tracking:** Integration with Leaflet maps to pinpoint waste pickup locations visually on the frontend.
- **Dynamic Dashboards:** Interactive data visualization using Chart.js and ApexCharts for reporting income, expenses, and operational metrics.
- **Automated Workflows:** Complete lifecycle tracking from citizen waste reports to officer pickup, automated salary calculation, and system notifications.
- **Decoupled Architecture:** Clean separation of concerns between the SPA frontend and the REST API backend.

## 📂 Folder Structure

```text
.
├── Frontend-Apk-Sampah-Ifter/  # Frontend Application (Vue.js / Quasar)
│   ├── src/                    # Source code (Components, Pages, Pinia Stores, Router)
│   ├── public/                 # Static assets
│   ├── quasar.config.js        # Quasar build and configuration parameters
│   ├── netlify.toml            # Netlify CI/CD configuration for production
│   └── package.json            # Node.js dependencies and scripts
│
└── sps-app/                    # Backend API Application (Python / Flask)
    ├── config.py               # Database and application configurations
    ├── app.py                  # Main Flask application entry point
    ├── routes/                 # API controllers (Flask Blueprints: auth, warga, petugas, dll)
    └── spsdb.sql               # MySQL database schema and seed data
```

## 🏗 System Architecture (Local/Development)

In a local development environment, the frontend runs on a Node.js development server and proxies/communicates via HTTP REST to the Flask backend running on a local Python server. The backend connects directly to a local MySQL instance.

```mermaid
flowchart TD
    Browser([Developer Browser]) <-->|HTTP :9000| Quasar[Vue/Quasar Dev Server\n(Frontend)]
    Quasar <-->|HTTP REST / JSON| Flask[Flask API\n(Backend)]
    
    subgraph Backend Services
        Flask <--> Auth[Auth Blueprint]
        Flask <--> Operations[Operations Blueprints]
    end
    
    Backend Services <-->|PyMySQL| MySQL[(Local MySQL DB\nspsdb)]
```

## ☁️ System Architecture (Cloud/Production)

Based on the environment variables and configuration files (`netlify.toml`, `.env`), the production architecture utilizes managed cloud services. The frontend is hosted statically on Netlify, while the backend API targets a cloud Python host (e.g., PythonAnywhere).

```mermaid
flowchart TD
    User([End User / Client]) <-->|HTTPS| Netlify[Netlify CDN\n(Hosts compiled SPA)]
    User <-->|HTTPS REST| PythonAnywhere[Cloud Flask API\n(e.g., PythonAnywhere)]
    
    PythonAnywhere <-->|SQL| CloudDB[(Cloud MySQL Database)]
```

## 🗄 Database Table Relationship Diagram (TRD/ERD)

The backend relies on a relational MySQL database. The following diagram illustrates the complete table schema, fields, and relationships defined in `spsdb.sql`:

```mermaid
erDiagram
    users {
        int id PK
        varchar username
        varchar password
        enum role "admin, petugas, warga"
        enum status "active, inactive"
        datetime created_at
    }

    warga {
        int id PK
        int user_id FK
        varchar nama_warga
        text alamat
        varchar lokasi
        float longitude
        float latitude
    }

    petugas {
        int id PK
        int user_id FK
        varchar nama_petugas
    }

    jadwal {
        int id PK
        date tanggal
        time jam_mulai
        time jam_selesai
        varchar wilayah
        int id_petugas FK
        enum status "aktif, nonaktif"
    }

    laporan_sampah {
        int id PK
        int id_warga FK
        text alamat
        tinyint sudah_dipilah
        int jumlah_karung
        enum jenis_pembayaran "cash, saldo, transfer"
        datetime jadwal_pengambilan
        enum status "menunggu, dijemput, selesai"
        datetime created_at
    }

    gaji_petugas {
        int id PK
        int id_petugas FK
        int jumlah_sampah
        float total_gaji
        datetime tanggal
    }

    pemasukan {
        int id PK
        int id_warga FK
        int id_laporan FK
        int jumlah_karung
        float jumlah_pembayaran
        float kekurangan
        float kelebihan
        datetime tanggal
    }

    pengeluaran {
        int id PK
        enum jenis_pengeluaran "operasional, gaji, lainnya"
        varchar nama_pengeluaran
        float jumlah_pengeluaran
        datetime tanggal
    }

    transaksi {
        int id PK
        int id_pemasukan FK
        int id_pengeluaran FK
        int jumlah_karung
        datetime tanggal
    }

    notifikasi {
        int id PK
        int user_id FK
        varchar judul
        text isi
        enum kategori "jadwal, pembayaran, laporan, gaji"
        enum status "belum_dibaca, dibaca"
        datetime tanggal
    }

    riwayat_aktivitas {
        int id PK
        int id_warga FK
        int id_petugas FK
        datetime tanggal
        int jumlah_karung
        enum status "diambil, selesai, batal"
    }
    
    migrations {
        int id PK
        varchar migration
        int batch
    }

    users ||--o| warga : "1:1 (user_id)"
    users ||--o| petugas : "1:1 (user_id)"
    users ||--o{ notifikasi : "1:N (user_id)"
    petugas ||--o{ jadwal : "1:N (id_petugas)"
    petugas ||--o{ gaji_petugas : "1:N (id_petugas)"
    petugas ||--o{ riwayat_aktivitas : "1:N (id_petugas)"
    warga ||--o{ laporan_sampah : "1:N (id_warga)"
    warga ||--o{ pemasukan : "1:N (id_warga)"
    warga ||--o{ riwayat_aktivitas : "1:N (id_warga)"
    laporan_sampah ||--o| pemasukan : "1:1 (id_laporan)"
    pemasukan ||--o{ transaksi : "1:N (id_pemasukan)"
    pengeluaran ||--o{ transaksi : "1:N (id_pengeluaran)"
```

## 🛠 Tech Stack

**Frontend**
- **Framework:** Vue.js 3, Quasar Framework
- **State Management:** Pinia
- **HTTP Client:** Axios
- **Data Visualization:** Chart.js, ApexCharts (`vue3-apexcharts`)
- **Mapping:** Leaflet, `leaflet.awesome-markers`

**Backend**
- **Framework:** Python 3, Flask, Flask-CORS
- **Authentication:** PyJWT, Werkzeug (Password Hashing)
- **Database Driver:** PyMySQL

**Database & Infrastructure**
- **Database:** MySQL / MariaDB
- **DevOps:** Netlify (Frontend Hosting)

## 🚀 Getting Started / Installation

You must run both the frontend and backend services simultaneously to use the application locally.

### 1. Backend Setup (`sps-app`)
1. Ensure Python 3 and MySQL are installed on your machine.
2. Navigate to the backend directory:
   ```bash
   cd sps-app
   ```
3. Create a local MySQL database named `spsdb` and import the schema:
   ```bash
   mysql -u root -p spsdb < spsdb.sql
   ```
4. Update `config.py` with your MySQL credentials.
5. Install Python dependencies:
   ```bash
   pip install Flask Flask-Cors PyMySQL PyJWT Werkzeug
   ```
6. Start the Flask API:
   ```bash
   python app.py
   ```
   *The backend will run on `http://127.0.0.1:5000`.*

### 2. Frontend Setup (`Frontend-Apk-Sampah-Ifter`)
1. Ensure Node.js (v20+) and npm are installed.
2. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd Frontend-Apk-Sampah-Ifter
   ```
3. Install Node modules:
   ```bash
   npm install
   ```
4. Verify that the `.env` file points to your local backend (if testing locally, change `VITE_API_URL` to `http://127.0.0.1:5000`, otherwise it points to production).
5. Start the Quasar development server:
   ```bash
   npm run dev
   ```
   *The frontend will open in your browser automatically.*

## 🔄 CI/CD & Deployment

- **Frontend Pipeline:** The frontend utilizes Netlify for CI/CD. The `netlify.toml` file automatically triggers `quasar build` on deployment, publishing the `dist/spa` directory and handling SPA routing redirects.
- **Backend Pipeline:** Continuous Integration/Deployment is not explicitly configured in the repository (e.g., no GitHub Actions or Dockerfiles). Deployment requires manual setup of a WSGI environment or a managed cloud platform capable of running Python Flask applications.

## 📄 License

*License not specified in the repository. Please contact the repository owner for licensing information.*
