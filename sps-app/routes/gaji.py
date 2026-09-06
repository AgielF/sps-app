# routes/gaji.py
from flask import Blueprint, request, jsonify, make_response
import pymysql
from config import DB_CONFIG

gaji_bp = Blueprint('gaji', __name__, url_prefix='/api/gaji')

@gaji_bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,PATCH,DELETE,OPTIONS'
    return response

def get_connection():
    return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **DB_CONFIG)

@gaji_bp.route('/', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_all_gaji():
    if request.method == 'OPTIONS': return '', 200
    id_petugas = request.args.get('id_petugas')
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT g.id, g.id_petugas, p.nama_petugas,
                       g.jumlah_sampah, g.total_gaji, g.tanggal
                FROM gaji_petugas g
                JOIN petugas p ON g.id_petugas = p.id
                WHERE 1=1
            """
            params = []
            if id_petugas:
                sql += " AND g.id_petugas = %s"
                params.append(id_petugas)
            sql += " ORDER BY g.tanggal DESC"
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        return jsonify({"success": True, "data": rows}), 200
    except Exception as e:
        print("get_all_gaji error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()

@gaji_bp.route('/riwayat', methods=['GET', 'OPTIONS'])
def get_riwayat_gaji():
    if request.method == 'OPTIONS': return '', 200
    return get_all_gaji()

@gaji_bp.route('/jadwal', methods=['GET', 'OPTIONS'])
def get_jadwal_gaji():
    if request.method == 'OPTIONS': return '', 200
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # We return jadwal that are likely to need paying (Selesai status)
            cursor.execute("""
                SELECT id, wilayah, 
                       DATE_FORMAT(tanggal, '%Y-%m-%d') as tanggal, 
                       TIME_FORMAT(jam_mulai, '%H:%i') as jam_mulai,
                       TIME_FORMAT(jam_selesai, '%H:%i') as jam_selesai,
                       status
                FROM jadwal
                ORDER BY tanggal DESC LIMIT 50
            """)
            rows = cursor.fetchall()
        return jsonify({"success": True, "data": rows}), 200
    except Exception as e:
        print("get_jadwal_gaji error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()

@gaji_bp.route('/jadwal/<int:id>/petugas', methods=['GET', 'OPTIONS'])
def get_jadwal_petugas(id):
    if request.method == 'OPTIONS': return '', 200
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Fix string formatting by using %% for literal % when passing parameters
            cursor.execute("SELECT id, wilayah, DATE_FORMAT(tanggal, '%%Y-%%m-%%d') as tanggal, id_petugas FROM jadwal WHERE id = %s", (id,))
            jadwal = cursor.fetchone()
            
            if not jadwal:
                return jsonify({"success": False, "message": "Jadwal tidak ditemukan"}), 404
            
            petugas_id = jadwal.get('id_petugas')
            petugas = []
            
            if petugas_id:
                # Ambil data petugas beserta gaji_per_karung
                cursor.execute("""
                    SELECT p.id, p.nama_petugas as nama_lengkap, p.no_telp as no_telepon, p.nik, p.gaji_per_karung,
                           'Hadir' as status_kehadiran, 0 as total_karung, 0 as estimasi_gaji
                    FROM petugas p
                    WHERE p.id = %s
                """, (petugas_id,))
                petugas = cursor.fetchall()
            
        return jsonify({"success": True, "data": {"jadwal": jadwal, "petugas": petugas}}), 200
    except Exception as e:
        print("get_jadwal_petugas error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()

@gaji_bp.route('/jadwal/<int:id>/cek', methods=['GET', 'OPTIONS'])
def cek_gaji_jadwal(id):
    if request.method == 'OPTIONS': return '', 200
    return jsonify({"success": True, "sudah_ada": False, "data": []}), 200

@gaji_bp.route('/simpan', methods=['POST', 'OPTIONS'])
def simpan_gaji():
    if request.method == 'OPTIONS': return '', 200
    data = request.json
    jadwal_id = data.get('jadwal_id')
    keterangan_umum = data.get('keterangan_umum', '')
    gaji_list = data.get('gaji_list', [])
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            for g in gaji_list:
                cursor.execute("""
                    INSERT INTO gaji_petugas (id_petugas, jumlah_sampah, total_gaji)
                    VALUES (%s, %s, %s)
                """, (g.get('petugas_id'), 0, g.get('gaji', 0)))
            
            # Also insert into pengeluaran
            total_semua = sum([float(g.get('gaji', 0)) for g in gaji_list])
            cursor.execute("""
                INSERT INTO pengeluaran (tanggal, keterangan, jumlah_pengeluaran)
                VALUES (CURDATE(), %s, %s)
            """, (f"Gaji Petugas: {keterangan_umum}", total_semua))
        conn.commit()
        return jsonify({"success": True, "message": "Berhasil menyimpan gaji"}), 200
    except Exception as e:
        conn.rollback()
        print("simpan_gaji error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()

@gaji_bp.route('/petugas/<int:id_petugas>', methods=['GET', 'OPTIONS'])
def get_gaji_petugas(id_petugas):
    if request.method == 'OPTIONS': return '', 200
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Current salary stats for petugas
            cursor.execute("""
                SELECT COALESCE(SUM(total_gaji), 0) as total_dibayar, COUNT(id) as total_transaksi
                FROM gaji_petugas
                WHERE id_petugas = %s
            """, (id_petugas,))
            stats = cursor.fetchone()
            
            cursor.execute("""
                SELECT id, tanggal, total_gaji as jumlah, 'Gaji Dibayarkan' as keterangan
                FROM gaji_petugas
                WHERE id_petugas = %s
                ORDER BY tanggal DESC LIMIT 10
            """, (id_petugas,))
            history = cursor.fetchall()
            
        return jsonify({
            "success": True, 
            "data": {
                "total_gaji": stats['total_dibayar'],
                "riwayat_gaji": history,
                "bulan_ini": stats['total_dibayar'],
                "riwayat_kerja": []
            }
        }), 200
    except Exception as e:
        print("get_gaji_petugas error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()

