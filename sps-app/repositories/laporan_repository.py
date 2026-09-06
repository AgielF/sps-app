from .db_core import DatabaseConnection
from datetime import datetime

class LaporanRepository:
    @staticmethod
    def get_all(status=None, id_warga=None):
        sql = """
            SELECT l.id, l.id_warga, w.nama_warga,
                   l.alamat, l.sudah_dipilah,
                   l.jumlah_karung, l.jenis_sampah, l.jenis_pembayaran,
                   l.jadwal_pengambilan, l.status,
                   l.created_at
            FROM laporan_sampah l
            JOIN warga w ON l.id_warga = w.id
            WHERE 1=1
        """
        params = []
        if status:
            sql += " AND l.status = %s"
            params.append(status)
        if id_warga:
            sql += " AND l.id_warga = %s"
            params.append(id_warga)
        sql += " ORDER BY l.created_at DESC"
        
        return DatabaseConnection.execute_query(sql, params)

    @staticmethod
    def get_by_petugas(id_petugas):
        sql = """
            SELECT l.id, l.id_warga, w.nama_warga,
                   l.alamat, l.sudah_dipilah,
                   l.jumlah_karung as estimasi_volume, l.jenis_sampah, l.jenis_pembayaran,
                   l.jadwal_pengambilan, l.status,
                   l.created_at
            FROM laporan_sampah l
            JOIN warga w ON l.id_warga = w.id
            WHERE l.status IN ('menunggu', 'diproses')
            ORDER BY l.created_at DESC
        """
        return DatabaseConnection.execute_query(sql)

    @staticmethod
    def get_by_id(laporan_id):
        sql = """
            SELECT l.id, l.id_warga, w.nama_warga,
                   l.alamat, l.sudah_dipilah,
                   l.jumlah_karung, l.jenis_sampah, l.jenis_pembayaran,
                   l.jadwal_pengambilan, l.status,
                   l.created_at
            FROM laporan_sampah l
            JOIN warga w ON l.id_warga = w.id
            WHERE l.id = %s
        """
        return DatabaseConnection.execute_fetchone(sql, (laporan_id,))

    @staticmethod
    def create(data):
        user_id = data.get('user_id')
        alamat = data.get('alamat')
        sudah_dipilah = 1 if data.get('sudah_dipilah', 0) else 0
        jumlah_karung = data.get('jumlah_karung')
        jenis_pembayaran = data.get('jenis_pembayaran')
        tanggal_pengambilan = data.get('tanggal_pengambilan')
        jam_pengambilan = data.get('jam_pengambilan')
        jenis_sampah = data.get('jenis_sampah')

        if jam_pengambilan:
            if len(jam_pengambilan) == 5:
                jam_pengambilan += ":00"
            jadwal_dt = datetime.strptime(f"{tanggal_pengambilan} {jam_pengambilan}", "%Y-%m-%d %H:%M:%S")
        else:
            jadwal_dt = datetime.strptime(f"{tanggal_pengambilan} 08:00:00", "%Y-%m-%d %H:%M:%S")

        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, alamat FROM warga WHERE user_id = %s", (user_id,))
                warga = cursor.fetchone()
                if not warga:
                    raise ValueError("Data warga tidak ditemukan")
                
                id_warga = warga['id']
                if not alamat:
                    alamat = warga['alamat']

                sql = """
                    INSERT INTO laporan_sampah
                    (id_warga, alamat, sudah_dipilah, jumlah_karung,
                     jenis_pembayaran, jadwal_pengambilan, jenis_sampah, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 'menunggu')
                """
                cursor.execute(sql, (id_warga, alamat, sudah_dipilah, jumlah_karung,
                                     jenis_pembayaran, jadwal_dt, jenis_sampah))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def update_status(laporan_id, new_status, id_petugas):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, id_warga, jumlah_karung, status FROM laporan_sampah WHERE id=%s", (laporan_id,))
                laporan = cursor.fetchone()
                if not laporan:
                    raise ValueError("Data laporan tidak ditemukan")
                if laporan['status'] == 'selesai' and new_status != 'selesai':
                    raise ValueError("Laporan yang sudah selesai tidak bisa diubah")

                cursor.execute("UPDATE laporan_sampah SET status=%s WHERE id=%s", (new_status, laporan_id))

                riwayat_status = None
                if new_status == 'dijemput':
                    riwayat_status = 'diambil'
                elif new_status == 'selesai':
                    riwayat_status = 'selesai'

                if riwayat_status:
                    petugas_id_val = int(id_petugas) if id_petugas not in (None, '', 0, '0') else None
                    sql_riwayat = """
                        INSERT INTO riwayat_aktivitas
                        (id_warga, id_petugas, jumlah_karung, status)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(sql_riwayat, (laporan['id_warga'], petugas_id_val, laporan['jumlah_karung'], riwayat_status))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def delete(laporan_id):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT status FROM laporan_sampah WHERE id=%s", (laporan_id,))
                laporan = cursor.fetchone()
                if not laporan:
                    raise ValueError("Data laporan tidak ditemukan")
                if laporan['status'] != 'menunggu':
                    raise ValueError("Hanya laporan yang berstatus menunggu yang bisa dibatalkan")
                
                cursor.execute("DELETE FROM laporan_sampah WHERE id=%s", (laporan_id,))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
