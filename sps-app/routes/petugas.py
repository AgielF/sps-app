from flask import Blueprint, request, jsonify
import pymysql
from werkzeug.security import generate_password_hash
from config import DB_CONFIG

petugas_bp = Blueprint('petugas', __name__, url_prefix='/api/petugas')


# =========================
# koneksi DB
# =========================
def get_connection():
    return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **DB_CONFIG)


# map status DB → UI frontend
def map_status_for_ui(db_status: str) -> str:
    if db_status == 'menunggu':
        return 'Belum diambil'
    return 'Sudah diambil'


# =========================
# GET semua petugas
# =========================
@petugas_bp.route('/', methods=['GET'], strict_slashes=False)
def get_petugas():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.*, u.username, u.status as user_status 
                FROM petugas p
                LEFT JOIN users u ON p.user_id = u.id
                ORDER BY p.id DESC
            """)
            rows = cursor.fetchall()
            
            # Map status_kerja as status for frontend compatibility
            for row in rows:
                if 'status_kerja' in row:
                    row['status'] = row['status_kerja']
        return jsonify({"success": True, "data": rows}), 200
    except Exception as e:
        print("get_petugas error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()


# =========================
# GET statistik petugas
# =========================
@petugas_bp.route('/statistik/<int:id_petugas>', methods=['GET'])
def get_statistik_petugas(id_petugas):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Hitung total karung dan gaji (estimasi sederhana)
            cursor.execute("""
                SELECT COALESCE(SUM(jumlah_karung), 0) as total_karung 
                FROM riwayat_aktivitas 
                WHERE id_petugas = %s AND status = 'Selesai'
            """, (id_petugas,))
            res = cursor.fetchone()
            total_karung = res['total_karung'] if res else 0
            
            # Asumsi gaji per karung Rp. 5000 (sesuai gaji.py / frontend)
            total_gaji = total_karung * 5000

            data = {
                "total_karung": total_karung,
                "total_gaji": total_gaji
            }
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        print("get_statistik_petugas error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()

# =========================
# CREATE petugas + user
# =========================
@petugas_bp.route('/create', methods=['POST'])
def create_petugas():
    data = request.json or {}
    
    # Map frontend payload keys
    nama_petugas = data.get('nama_lengkap') or data.get('nama_petugas')
    no_telp = data.get('no_telepon') or data.get('no_telp')
    data['nama_petugas'] = nama_petugas
    data['no_telp'] = no_telp
    
    required = ['username', 'password', 'nama_petugas', 'no_telp', 'alamat']

    for field in required:
        if field not in data or data[field] == '':
            return jsonify({"success": False, "message": f"{field} wajib diisi"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            hashed_pass = generate_password_hash(data['password'])
            status_kerja = data.get('status_kerja', 'aktif')
            user_status = 'active' if status_kerja == 'aktif' else 'inactive'
            
            cursor.execute("""
                INSERT INTO users (username, password, role, status)
                VALUES (%s, %s, %s, %s)
            """, (data['username'], hashed_pass, 'petugas', user_status))

            user_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO petugas (user_id, nama_petugas, no_telp, alamat, email, nik, status_kerja, gaji_per_karung)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id, 
                nama_petugas, 
                no_telp, 
                data['alamat'],
                data.get('email'),
                data.get('nik'),
                data.get('status_kerja', 'aktif'),
                data.get('gaji_per_karung', 5000)
            ))

        conn.commit()
        return jsonify({"success": True, "message": "Petugas berhasil dibuat"}), 201
    except pymysql.err.IntegrityError as e:
        conn.rollback()
        if e.args[0] == 1062:
            return jsonify({"success": False, "message": "Username sudah digunakan, silakan pilih username lain."}), 400
        print("create_petugas integrity error:", e)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada database (Duplicate)"}), 400
    except Exception as e:
        conn.rollback()
        print("create_petugas error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()

# =========================
# GET petugas by id
# =========================
@petugas_bp.route('/<int:id>', methods=['GET'])
def get_petugas_by_id(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.*, u.username 
                FROM petugas p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = %s
            """, (id,))
            row = cursor.fetchone()
            if not row:
                return jsonify({"success": False, "message": "Data tidak ditemukan"}), 404
            
            # Map back to what frontend expects
            row['nama_lengkap'] = row.get('nama_petugas')
            row['no_telepon'] = row.get('no_telp')
            
            return jsonify({"success": True, "data": row}), 200
    except Exception as e:
        print("get_petugas_by_id error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()

# =========================
# UPDATE petugas
# =========================
@petugas_bp.route('/<int:id>', methods=['PUT'])
def update_petugas(id):
    data = request.json or {}
    
    # Map frontend payload keys
    nama_petugas = data.get('nama_lengkap') or data.get('nama_petugas')
    no_telp = data.get('no_telepon') or data.get('no_telp')
    data['nama_petugas'] = nama_petugas
    data['no_telp'] = no_telp
    
    required = ['username', 'nama_petugas', 'no_telp', 'alamat']

    for field in required:
        if field not in data or data[field] == '':
            return jsonify({"success": False, "message": f"{field} wajib diisi"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Update petugas
            cursor.execute("""
                UPDATE petugas 
                SET nama_petugas=%s, no_telp=%s, alamat=%s, email=%s, nik=%s, status_kerja=%s, gaji_per_karung=%s
                WHERE id=%s
            """, (
                nama_petugas, 
                no_telp, 
                data['alamat'],
                data.get('email'),
                data.get('nik'),
                data.get('status_kerja', 'aktif'),
                data.get('gaji_per_karung', 5000),
                id
            ))
            
            # Update user info (username + password + status)
            status_kerja = data.get('status_kerja', 'aktif')
            user_status = 'active' if status_kerja == 'aktif' else 'inactive'
            
            if data.get('password'):
                hashed_pass = generate_password_hash(data['password'])
                cursor.execute("""
                    UPDATE users 
                    SET username=%s, password=%s, status=%s 
                    WHERE id=(SELECT user_id FROM petugas WHERE id=%s)
                """, (data['username'], hashed_pass, user_status, id))
            else:
                cursor.execute("""
                    UPDATE users 
                    SET username=%s, status=%s 
                    WHERE id=(SELECT user_id FROM petugas WHERE id=%s)
                """, (data['username'], user_status, id))

        conn.commit()
        return jsonify({"success": True, "message": "Petugas berhasil diupdate"}), 200
    except Exception as e:
        conn.rollback()
        print("update_petugas error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()


# =========================
# DELETE petugas
# =========================
@petugas_bp.route('/<int:id>', methods=['DELETE'])
def delete_petugas(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM petugas WHERE id = %s", (id,))
            conn.commit()

        return jsonify({"success": True, "message": "Petugas dihapus"}), 200
    except Exception as e:
        print("delete_petugas error:", e)
        return jsonify({"success": False, "message": "Gagal menghapus"}), 500
    finally:
        conn.close()


# =========================
# GET petugas by user_id
# =========================
@petugas_bp.route('/by-user/<int:user_id>', methods=['GET'])
def get_petugas_by_user(user_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, user_id, nama_petugas, no_telp, alamat, status
                FROM petugas
                WHERE user_id = %s
                LIMIT 1
            """, (user_id,))
            row = cursor.fetchone()

        if not row:
            return jsonify({"success": False, "message": "Petugas tidak ditemukan"}), 404

        return jsonify({"success": True, "data": row}), 200
    except Exception as e:
        print("get_petugas_by_user error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()


# =========================
# GET tugas petugas
# cocok untuk frontend yg kamu kirim
# =========================
@petugas_bp.route('/tugas', methods=['GET'])
def get_tugas_petugas():
    q_date = request.args.get('date')
    petugas_id = request.args.get('petugas_id')

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            wilayah = None
            if petugas_id and q_date:
                cursor.execute("""
                    SELECT wilayah
                    FROM jadwal
                    WHERE id_petugas = %s AND tanggal = %s AND status = 'aktif'
                    ORDER BY id DESC
                    LIMIT 1
                """, (petugas_id, q_date))
                row = cursor.fetchone()
                wilayah = row["wilayah"] if row else None

            sql = """
                SELECT 
                    ls.id AS id,
                    w.nama_warga AS name,
                    COALESCE(ls.alamat, w.alamat) AS address,
                    ls.status AS status_db,
                    ls.jadwal_pengambilan AS jadwal_pengambilan
                FROM laporan_sampah ls
                JOIN warga w ON w.id = ls.id_warga
                WHERE ls.jadwal_pengambilan IS NOT NULL
            """
            params = []

            if q_date:
                sql += " AND DATE(ls.jadwal_pengambilan) = %s"
                params.append(q_date)

            sql += " AND ls.status IN ('menunggu','dijemput','selesai')"

            if wilayah and wilayah.lower() != 'seluruh':
                sql += " AND (w.lokasi = %s OR COALESCE(ls.alamat, w.alamat) LIKE %s)"
                params.extend([wilayah, f"%{wilayah}%"])

            sql += " ORDER BY ls.jadwal_pengambilan ASC, ls.id DESC"

            cursor.execute(sql, params)
            rows = cursor.fetchall()

        data = []
        for r in rows:
            data.append({
                "id": r["id"],
                "name": r["name"],
                "address": r["address"],
                "status": map_status_for_ui(r["status_db"]),
                "date": r["jadwal_pengambilan"].strftime("%Y-%m-%d") if r["jadwal_pengambilan"] else None,
                "jadwal_pengambilan": r["jadwal_pengambilan"].strftime("%Y-%m-%d %H:%M:%S") if r["jadwal_pengambilan"] else None,
                "status_db": r["status_db"],
            })

        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        print("get_tugas_petugas error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()


# =========================
# update status ambil tugas
# =========================
@petugas_bp.route('/tugas/<int:laporan_id>/ambil', methods=['POST'])
def ambil_tugas(laporan_id):
    data = request.json or {}
    petugas_id = data.get("petugas_id")
    jumlah_karung = data.get("jumlah_karung")

    if not petugas_id:
        return jsonify({"success": False, "message": "petugas_id wajib"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_warga, status FROM laporan_sampah WHERE id = %s", (laporan_id,))
            laporan = cursor.fetchone()
            if not laporan:
                return jsonify({"success": False, "message": "Laporan tidak ditemukan"}), 404

            cursor.execute("""
                UPDATE laporan_sampah
                SET status = 'dijemput'
                WHERE id = %s AND status = 'menunggu'
            """, (laporan_id,))

            cursor.execute("""
                INSERT INTO riwayat_aktivitas (id_warga, id_petugas, jumlah_karung, status)
                VALUES (%s, %s, %s, 'diambil')
            """, (laporan["id_warga"], petugas_id, jumlah_karung))

        conn.commit()
        return jsonify({"success": True, "message": "Status diperbarui menjadi dijemput"}), 200
    except Exception as e:
        conn.rollback()
        print("ambil_tugas error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()

@petugas_bp.route('/rekap', methods=['GET'])
def rekap_pengambilan():
    q_date = request.args.get('date')  # YYYY-MM-DD
    petugas_id = request.args.get('petugas_id')  # opsional

    if not q_date:
        return jsonify({"success": False, "message": "date wajib (YYYY-MM-DD)"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Ambil wilayah (opsional) dari jadwal petugas untuk tanggal tsb
            wilayah = None
            if petugas_id:
                cursor.execute("""
                    SELECT wilayah
                    FROM jadwal
                    WHERE id_petugas = %s AND tanggal = %s AND status = 'aktif'
                    ORDER BY id DESC
                    LIMIT 1
                """, (petugas_id, q_date))
                row = cursor.fetchone()
                wilayah = row["wilayah"] if row else None

            # Filter wilayah: pakai warga.lokasi atau alamat LIKE
            wilayah_sql = ""
            wilayah_params = []
            if wilayah and wilayah.lower() != 'seluruh':
                wilayah_sql = " AND (w.lokasi = %s OR COALESCE(ls.alamat, w.alamat) LIKE %s) "
                wilayah_params = [wilayah, f"%{wilayah}%"]

            # 1) Detail transaksi
            cursor.execute(f"""
                SELECT
                    ls.id AS id_laporan,
                    w.nama_warga AS nama,
                    ls.jumlah_karung,
                    ls.jenis_pembayaran,
                    ls.status AS status_laporan,
                    COALESCE(p.jumlah_pembayaran, 0) AS jumlah_pembayaran,
                    COALESCE(p.kekurangan, 0) AS kekurangan
                FROM laporan_sampah ls
                JOIN warga w ON w.id = ls.id_warga
                LEFT JOIN pemasukan p ON p.id_laporan = ls.id
                WHERE ls.jadwal_pengambilan IS NOT NULL
                  AND DATE(ls.jadwal_pengambilan) = %s
                {wilayah_sql}
                ORDER BY ls.jadwal_pengambilan ASC, ls.id DESC
            """, [q_date] + wilayah_params)

            rows = cursor.fetchall()

            # 2) Ringkasan
            pemasukan_hari_ini = 0.0
            total_tunggak_rp = 0.0
            jumlah_pengambilan = len(rows)
            jumlah_tunggak_kasus = 0

            detail = []
            for r in rows:
                pemasukan_hari_ini += float(r["jumlah_pembayaran"] or 0)
                total_tunggak_rp += float(r["kekurangan"] or 0)
                if float(r["kekurangan"] or 0) > 0:
                    jumlah_tunggak_kasus += 1

                # mapping agar cocok UI kamu
                metode = r["jenis_pembayaran"]
                if metode == 'transfer':
                    metode_ui = 'Transfer bank'
                elif metode == 'saldo':
                    metode_ui = 'Saldo'
                else:
                    metode_ui = 'Cash'

                status_ui = 'Lunas' if float(r["kekurangan"] or 0) == 0 else 'Belum'

                detail.append({
                    "nama": r["nama"],
                    "jumlah_karung": r["jumlah_karung"],
                    "pembayaran": metode_ui,
                    "status": status_ui,
                    "id_laporan": r["id_laporan"],
                    "kekurangan": float(r["kekurangan"] or 0),
                    "jumlah_pembayaran": float(r["jumlah_pembayaran"] or 0),
                })

        return jsonify({
            "success": True,
            "data": {
                "tanggal": q_date,
                "pemasukan_hari_ini": pemasukan_hari_ini,
                "total_tunggak_rp": total_tunggak_rp,
                "total_tunggak_kasus": jumlah_tunggak_kasus,
                "pengambilan_sampah": jumlah_pengambilan,
                "detail": detail
            }
        }), 200

    except Exception as e:
        print("rekap_pengambilan error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()
@petugas_bp.route('/transaksi', methods=['GET', 'OPTIONS'])
def get_petugas_transaksi():
    if request.method == 'OPTIONS': return '', 200
    tanggal = request.args.get('tanggal')
    jenis = request.args.get('jenis')
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # We return a dummy but functional structure since the full financial mapping isn't fully set up for petugas transactions yet
            
            sql = """
                SELECT 
                    id, 
                    created_at as tanggal,
                    'Pemasukan' as jenis,
                    CAST(jumlah_pembayaran AS UNSIGNED) as jumlah,
                    CONCAT('Pembayaran Laporan #', id) as keterangan,
                    'Selesai' as status,
                    'Uang Tunai' as metode_pembayaran,
                    id_petugas as petugas_id,
                    'Petugas' as nama_petugas,
                    id_warga as warga_id,
                    'Warga' as nama_warga
                FROM laporan_sampah
                WHERE id_petugas IS NOT NULL AND status = 'Selesai'
            """
            cursor.execute(sql)
            transactions = cursor.fetchall()
            
            summary = {
                "pemasukan": sum([t['jumlah'] for t in transactions if t['jenis'] == 'Pemasukan']),
                "pengeluaran": 0,
                "saldo": sum([t['jumlah'] for t in transactions if t['jenis'] == 'Pemasukan']),
                "transaksi_saya": len(transactions),
                "pemasukan_saya": sum([t['jumlah'] for t in transactions if t['jenis'] == 'Pemasukan']),
                "total_transaksi": len(transactions),
                "transaksi_lunas": len(transactions),
                "transaksi_pending": 0,
            }

        return jsonify({"success": True, "data": transactions, "summary": summary}), 200
    except Exception as e:
        print("get_petugas_transaksi error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()
