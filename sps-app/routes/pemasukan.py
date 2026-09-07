# routes/pemasukan.py
from flask import Blueprint, request, jsonify
import pymysql
from config import DB_CONFIG

pemasukan_bp = Blueprint('pemasukan', __name__, url_prefix='/api/pemasukan')

def get_connection():
    return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **DB_CONFIG)


# =========================================
# GET /api/pemasukan
# Opsional filter:
#   - ?id_warga=3
#   - ?id_laporan=4
# =========================================
@pemasukan_bp.route('/', methods=['GET'], strict_slashes=False)
def get_all_pemasukan():
    id_warga = request.args.get('id_warga')
    id_laporan = request.args.get('id_laporan')

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT p.id, p.tanggal, p.jumlah_karung,
                       p.jumlah_pembayaran AS jumlah, p.kekurangan, p.kelebihan,
                       p.kategori, p.keterangan,
                       w.nama_warga,
                       ls.id AS id_laporan
                FROM pemasukan p
                LEFT JOIN warga w ON p.id_warga = w.id
                LEFT JOIN laporan_sampah ls ON p.id_laporan = ls.id
                WHERE 1=1
            """
            params = []

            if id_warga:
                sql += " AND p.id_warga = %s"
                params.append(id_warga)
            if id_laporan:
                sql += " AND p.id_laporan = %s"
                params.append(id_laporan)

            sql += " ORDER BY p.tanggal DESC, p.id DESC"

            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            for r in rows:
                if r.get("tanggal"):
                    r["tanggal"] = r["tanggal"].strftime("%Y-%m-%d %H:%M:%S")

        return jsonify({"success": True, "data": rows}), 200
    except Exception as e:
        print("get_all_pemasukan error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()


# =========================================
# GET /api/pemasukan/<id>
# Detail satu pemasukan
# =========================================
@pemasukan_bp.route('/<int:pemasukan_id>', methods=['GET'])
def get_pemasukan_by_id(pemasukan_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT p.id, p.tanggal, p.jumlah_karung,
                       p.jumlah_pembayaran AS jumlah, p.kekurangan, p.kelebihan,
                       p.kategori, p.keterangan,
                       p.id_warga, w.nama_warga,
                       p.id_laporan
                FROM pemasukan p
                LEFT JOIN warga w ON p.id_warga = w.id
                WHERE p.id = %s
            """
            cursor.execute(sql, (pemasukan_id,))
            row = cursor.fetchone()

        if not row:
            return jsonify({"success": False, "message": "Data pemasukan tidak ditemukan"}), 404

        return jsonify({"success": True, "data": row}), 200
    except Exception as e:
        print("get_pemasukan_by_id error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()


# =========================================
# POST /api/pemasukan
# Catat pembayaran dari warga
# Body contoh:
# {
#   "id_warga": 3,
#   "id_laporan": 4,
#   "jumlah_karung": 5,
#   "jumlah_pembayaran": 50000,
#   "kekurangan": 0,
#   "kelebihan": 0
# }
# =========================================
@pemasukan_bp.route('/', methods=['POST'], strict_slashes=False)
def create_pemasukan():
    data = request.json or {}

    id_warga = data.get('id_warga')
    id_warga = id_warga if id_warga not in ('', None) else None
    
    id_laporan = data.get('id_laporan')
    id_laporan = id_laporan if id_laporan not in ('', None) else None
    
    jumlah_karung = data.get('jumlah_karung')
    jumlah_karung = jumlah_karung if jumlah_karung not in ('', None) else None
    
    jumlah_pembayaran = data.get('jumlah_pembayaran')
    if jumlah_pembayaran is None:
        jumlah_pembayaran = data.get('jumlah')
        
    kekurangan = data.get('kekurangan', 0)
    kelebihan = data.get('kelebihan', 0)

    kategori = data.get('kategori')
    keterangan = data.get('keterangan')

    # ===== Validasi dasar =====
    if jumlah_pembayaran is None:
        return jsonify({"success": False, "message": "jumlah_pembayaran wajib diisi"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Jika ada id_warga, cek keberadaan warga
            if id_warga:
                cursor.execute("SELECT id FROM warga WHERE id = %s", (id_warga,))
                warga = cursor.fetchone()
                if not warga:
                    return jsonify({"success": False, "message": "Data warga tidak ditemukan"}), 404

            # Jika ada id_laporan, cek laporan & konsistensi
            if id_laporan:
                cursor.execute(
                    "SELECT id, id_warga, status, jumlah_karung FROM laporan_sampah WHERE id = %s",
                    (id_laporan,)
                )
                laporan = cursor.fetchone()
                if not laporan:
                    return jsonify({"success": False, "message": "Data laporan tidak ditemukan"}), 404

                if id_warga and laporan['id_warga'] != int(id_warga):
                    return jsonify({
                        "success": False,
                        "message": "id_warga pada pemasukan tidak sesuai dengan id_warga di laporan"
                    }), 400

                # (Opsional tapi rapi) hanya izinkan pemasukan jika laporan sudah selesai
                if laporan['status'] != 'selesai':
                    return jsonify({
                        "success": False,
                        "message": "Pemasukan hanya bisa dicatat untuk laporan yang sudah berstatus 'selesai'"
                    }), 400

                # Kalau jumlah_karung tidak diisi → pakai dari laporan
                if not jumlah_karung:
                    jumlah_karung = laporan['jumlah_karung']

            sql = """
                INSERT INTO pemasukan
                    (id_warga, id_laporan, jumlah_karung,
                     jumlah_pembayaran, kekurangan, kelebihan, kategori, keterangan)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                id_warga,
                id_laporan,
                jumlah_karung,
                jumlah_pembayaran,
                kekurangan,
                kelebihan,
                kategori,
                keterangan
            ))
            conn.commit()
            new_id = cursor.lastrowid

        return jsonify({
            "success": True,
            "message": "Data pemasukan berhasil dicatat",
            "pemasukan_id": new_id
        }), 201

    except Exception as e:
        print("create_pemasukan error:", e)
        conn.rollback()
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()

@pemasukan_bp.route('/<int:pemasukan_id>', methods=['DELETE'])
def delete_pemasukan(pemasukan_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Check if exists
            cursor.execute("SELECT id FROM pemasukan WHERE id = %s", (pemasukan_id,))
            if not cursor.fetchone():
                return jsonify({"success": False, "message": "Data pemasukan tidak ditemukan"}), 404
                
            cursor.execute("DELETE FROM pemasukan WHERE id = %s", (pemasukan_id,))
            conn.commit()
            
        return jsonify({"success": True, "message": "Data pemasukan berhasil dihapus"}), 200
    except Exception as e:
        print("delete_pemasukan error:", e)
        conn.rollback()
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()

@pemasukan_bp.route('/<int:pemasukan_id>', methods=['PUT'])
def update_pemasukan(pemasukan_id):
    data = request.json or {}

    id_warga = data.get('id_warga')
    id_warga = id_warga if id_warga not in ('', None) else None
    
    id_laporan = data.get('id_laporan')
    id_laporan = id_laporan if id_laporan not in ('', None) else None
    
    jumlah_karung = data.get('jumlah_karung')
    jumlah_karung = jumlah_karung if jumlah_karung not in ('', None) else None
    
    jumlah_pembayaran = data.get('jumlah_pembayaran')
    if jumlah_pembayaran is None:
        jumlah_pembayaran = data.get('jumlah')
        
    kekurangan = data.get('kekurangan', 0)
    kelebihan = data.get('kelebihan', 0)

    kategori = data.get('kategori')
    keterangan = data.get('keterangan')

    if jumlah_pembayaran is None:
        return jsonify({"success": False, "message": "jumlah_pembayaran wajib diisi"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Check if exists
            cursor.execute("SELECT id FROM pemasukan WHERE id = %s", (pemasukan_id,))
            if not cursor.fetchone():
                return jsonify({"success": False, "message": "Data pemasukan tidak ditemukan"}), 404
                
            # Validasi id_warga
            if id_warga:
                cursor.execute("SELECT id FROM warga WHERE id = %s", (id_warga,))
                if not cursor.fetchone():
                    return jsonify({"success": False, "message": "Data warga tidak ditemukan"}), 404

            # Validasi id_laporan
            if id_laporan:
                cursor.execute(
                    "SELECT id, id_warga, status, jumlah_karung FROM laporan_sampah WHERE id = %s",
                    (id_laporan,)
                )
                laporan = cursor.fetchone()
                if not laporan:
                    return jsonify({"success": False, "message": "Data laporan tidak ditemukan"}), 404
                if id_warga and laporan['id_warga'] != int(id_warga):
                    return jsonify({
                        "success": False,
                        "message": "id_warga pada pemasukan tidak sesuai dengan id_warga di laporan"
                    }), 400

                if not jumlah_karung:
                    jumlah_karung = laporan['jumlah_karung']

            sql = """
                UPDATE pemasukan
                SET id_warga = %s, id_laporan = %s, jumlah_karung = %s,
                    jumlah_pembayaran = %s, kekurangan = %s, kelebihan = %s,
                    kategori = %s, keterangan = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                id_warga, id_laporan, jumlah_karung, jumlah_pembayaran,
                kekurangan, kelebihan, kategori, keterangan, pemasukan_id
            ))
            conn.commit()

        return jsonify({
            "success": True,
            "message": "Data pemasukan berhasil diupdate"
        }), 200

    except Exception as e:
        print("update_pemasukan error:", e)
        conn.rollback()
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        conn.close()
