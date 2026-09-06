from .db_core import DatabaseConnection
from werkzeug.security import generate_password_hash

class WargaRepository:
    @staticmethod
    def get_all():
        sql = """
            SELECT w.id, w.nama_warga, w.alamat, w.lokasi,
                   w.longitude, w.latitude, w.email, w.nik, w.no_telp, w.saldo, w.kelurahan,
                   u.username, u.status, u.role
            FROM warga w
            JOIN users u ON w.user_id = u.id
        """
        return DatabaseConnection.execute_query(sql)

    @staticmethod
    def get_by_id(warga_id):
        sql = """
            SELECT w.id, w.nama_warga, w.alamat, w.lokasi,
                   w.longitude, w.latitude, w.email, w.nik, w.no_telp, w.saldo, w.kelurahan,
                   u.username, u.status, u.role
            FROM warga w
            JOIN users u ON w.user_id = u.id
            WHERE w.id = %s
        """
        return DatabaseConnection.execute_fetchone(sql, (warga_id,))

    @staticmethod
    def get_by_user_id(user_id):
        sql = """
            SELECT w.id, w.nama_warga, w.alamat, w.lokasi,
                   w.longitude, w.latitude, w.email, w.nik, w.no_telp, w.saldo, w.kelurahan,
                   u.username, u.status, u.role
            FROM warga w
            JOIN users u ON w.user_id = u.id
            WHERE w.user_id = %s
            LIMIT 1
        """
        return DatabaseConnection.execute_fetchone(sql, (user_id,))

    @staticmethod
    def create(data):
        hashed_pass = generate_password_hash(data["password"])
        
        # We need a transaction here
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. Insert User
                sql_user = """
                    INSERT INTO users (username, password, role, status)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql_user, (data["username"], hashed_pass, "warga", "active"))
                user_id = cursor.lastrowid
                
                # 2. Insert Warga
                lokasi_gabungan = f"RT {data['rt']} / RW {data['rw']}"
                sql_warga = """
                    INSERT INTO warga (user_id, nama_warga, alamat, lokasi, latitude, longitude, email, nik, no_telp, saldo, kelurahan)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_warga, (
                    user_id,
                    data["nama_warga"],
                    data.get("alamat_lengkap") or data.get("lokasi"),
                    lokasi_gabungan,
                    float(data["latitude"]),
                    float(data["longitude"]),
                    data.get("email"),
                    data.get("nik"),
                    data.get("no_telepon"),
                    data.get("saldo", 0),
                    data.get("kelurahan")
                ))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def update(warga_id, data):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. Update Warga
                lokasi_gabungan = f"RT {data.get('rt', '')} / RW {data.get('rw', '')}"
                # Fallback location if RT/RW not provided
                if lokasi_gabungan == "RT  / RW " or not data.get('rt'):
                    lokasi_gabungan = data.get("lokasi", "")
                
                sql_warga = """
                    UPDATE warga SET nama_warga=%s, alamat=%s, lokasi=%s, latitude=%s, longitude=%s, email=%s, nik=%s, no_telp=%s, saldo=%s, kelurahan=%s
                    WHERE id=%s
                """
                cursor.execute(sql_warga, (
                    data["nama_warga"],
                    data.get("alamat_lengkap") or data.get("lokasi"),
                    lokasi_gabungan,
                    float(data["latitude"]),
                    float(data["longitude"]),
                    data.get("email"),
                    data.get("nik"),
                    data.get("no_telepon"),
                    data.get("saldo", 0),
                    data.get("kelurahan"),
                    warga_id
                ))
                
                # 2. Update User (if password provided)
                if data.get("password"):
                    hashed_pass = generate_password_hash(data["password"])
                    sql_user = "UPDATE users SET password=%s WHERE id=(SELECT user_id FROM warga WHERE id=%s)"
                    cursor.execute(sql_user, (hashed_pass, warga_id))
                    
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
