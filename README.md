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
flowchart LR
    %% Components
    Browser(["🌐 Developer Browser"])
    Quasar["💻 Vue/Quasar Dev Server<br/>(Frontend :9000)"]
    Flask["⚙️ Flask API Server<br/>(Backend :5000)"]
    MySQL[("🗄️ Local MySQL DB<br/>(spsdb)")]

    %% Data Flow
    Browser <==>|HTTP| Quasar
    Quasar <==>|REST API / JSON| Flask
    Flask <==>|PyMySQL| MySQL

    %% Subgraph Architecture
    subgraph Backend [Flask Backend Architecture]
        Flask
        Auth["Auth Blueprint"]
        Ops["Operations Blueprints"]
        Flask --- Auth
        Flask --- Ops
    end

    %% Styles
    style Browser fill:#f9f,stroke:#333,stroke-width:2px
    style Quasar fill:#4FC08D,stroke:#333,color:#fff
    style Flask fill:#000,stroke:#333,color:#fff
    style MySQL fill:#4479A1,stroke:#333,color:#fff
```

## ☁️ System Architecture (Cloud/Production)

Based on the environment variables and configuration files (`netlify.toml`, `.env`), the production architecture utilizes managed cloud services. The frontend is hosted statically on Netlify, while the backend API targets a cloud Python host (e.g., PythonAnywhere).

```mermaid
flowchart LR
    %% Components
    User(["📱 End User / Client"])
    Netlify["⚡ Netlify CDN<br/>(Static SPA Hosting)"]
    CloudAPI["☁️ Cloud Flask API<br/>(e.g. PythonAnywhere)"]
    CloudDB[("☁️ Cloud MySQL DB")]

    %% Data Flow
    User <==>|HTTPS (Static Assets)| Netlify
    User <==>|HTTPS REST API| CloudAPI
    CloudAPI <==>|Secure SQL Connection| CloudDB

    %% Styles
    style User fill:#f9f,stroke:#333,stroke-width:2px
    style Netlify fill:#00C7B7,stroke:#333,color:#000
    style CloudAPI fill:#3776AB,stroke:#333,color:#fff
    style CloudDB fill:#4479A1,stroke:#333,color:#fff
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

You must run both the frontend and backend services simultaneously to use the application locally. We have provided a convenient `start.sh` script to launch both automatically.

### Prerequisites
1. **Python 3** and **Node.js (v20+)** must be installed on your machine.
2. **MySQL** / MariaDB must be installed and running.
3. **Database Setup:** 
   - Create a local MySQL database named `spsdb` and import the schema:
     ```bash
     cd sps-app
     mysql -u root -p spsdb < spsdb.sql
     ```
   - Update `sps-app/config.py` with your local MySQL credentials.
4. **Python Dependencies:** The `start.sh` script automatically handles setting up a Python virtual environment (`venv`) and installing dependencies from `requirements.txt`. You do not need to install them manually.

### Running the Application

To start both the frontend and backend simultaneously, simply run the `start.sh` script from the project root:

```bash
./start.sh
```

**What this script does:**
1. Starts the **Flask API (Backend)** on `http://127.0.0.1:5000`.
2. Automatically installs NPM dependencies (if they don't exist) and starts the **Vue/Quasar Server (Frontend)**.
3. Automatically stops both servers gracefully when you press `CTRL+C`.

## 🔄 CI/CD & Deployment

- **Frontend Pipeline:** The frontend utilizes Netlify for CI/CD. The `netlify.toml` file automatically triggers `quasar build` on deployment, publishing the `dist/spa` directory and handling SPA routing redirects.
- **Backend Pipeline:** Continuous Integration/Deployment is not explicitly configured in the repository (e.g., no GitHub Actions or Dockerfiles). Deployment requires manual setup of a WSGI environment or a managed cloud platform capable of running Python Flask applications.

## 📄 License

*License not specified in the repository. Please contact the repository owner for licensing information.*
