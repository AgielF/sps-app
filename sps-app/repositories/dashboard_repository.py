from .db_core import DatabaseConnection

class DashboardRepository:
    @staticmethod
    def get_today_pemasukan():
        sql = """
            SELECT COALESCE(SUM(jumlah_pembayaran), 0) as total, COUNT(id) as transaksi
            FROM pemasukan
            WHERE DATE(tanggal) = CURDATE()
        """
        return DatabaseConnection.execute_fetchone(sql)

    @staticmethod
    def get_month_pemasukan():
        sql = """
            SELECT COALESCE(SUM(jumlah_pembayaran), 0) as total, COUNT(id) as transaksi
            FROM pemasukan
            WHERE MONTH(tanggal) = MONTH(CURDATE()) AND YEAR(tanggal) = YEAR(CURDATE())
        """
        return DatabaseConnection.execute_fetchone(sql)

    @staticmethod
    def get_total_petugas():
        sql = "SELECT COUNT(id) as total_petugas FROM petugas"
        return DatabaseConnection.execute_fetchone(sql)

    @staticmethod
    def get_today_schedule_count():
        sql = """
            SELECT COUNT(id) as count 
            FROM jadwal 
            WHERE tanggal = CURDATE()
        """
        return DatabaseConnection.execute_fetchone(sql)

    @staticmethod
    def get_today_schedule():
        sql = """
            SELECT id, wilayah, 
                   TIME_FORMAT(jam_mulai, '%%H:%%i') as jam_mulai, 
                   TIME_FORMAT(jam_selesai, '%%H:%%i') as jam_selesai, 
                   status as keterangan
            FROM jadwal 
            WHERE tanggal = CURDATE()
            ORDER BY jam_mulai ASC
        """
        return DatabaseConnection.execute_query(sql)

    @staticmethod
    def get_monthly_stats():
        sql_pem = "SELECT COALESCE(SUM(jumlah_pembayaran), 0) as total FROM pemasukan WHERE MONTH(tanggal) = MONTH(CURDATE()) AND YEAR(tanggal) = YEAR(CURDATE())"
        sql_peng = "SELECT COALESCE(SUM(jumlah_pengeluaran), 0) as total FROM pengeluaran WHERE MONTH(tanggal) = MONTH(CURDATE()) AND YEAR(tanggal) = YEAR(CURDATE())"
        
        pem = DatabaseConnection.execute_fetchone(sql_pem)
        peng = DatabaseConnection.execute_fetchone(sql_peng)
        
        total_pem = float(pem['total']) if pem else 0
        total_peng = float(peng['total']) if peng else 0
        
        return {
            "pemasukan_bulan_ini": total_pem,
            "pengeluaran_bulan_ini": total_peng,
            "saldo_bulan_ini": total_pem - total_peng
        }

    @staticmethod
    def get_recent_transactions(limit=8):
        sql = """
            (SELECT id, 'pemasukan' as jenis, kategori as keterangan, 'Pemasukan' as kategori, jumlah_pembayaran as jumlah, tanggal as time
             FROM pemasukan
             ORDER BY tanggal DESC LIMIT %s)
            UNION ALL
            (SELECT id, 
                CASE 
                    WHEN jenis_pengeluaran = 'gaji' THEN 'gaji'
                    ELSE 'pengeluaran' 
                END as jenis, 
                nama_pengeluaran as keterangan, 
                jenis_pengeluaran as kategori, 
                jumlah_pengeluaran as jumlah, 
                tanggal as time
             FROM pengeluaran
             ORDER BY tanggal DESC LIMIT %s)
            ORDER BY time DESC LIMIT %s
        """
        # Convert date to string for JSON serialization
        results = DatabaseConnection.execute_query(sql, (limit, limit, limit))
        for row in results:
            if row.get('time'):
                row['time'] = row['time'].strftime('%Y-%m-%d %H:%M:%S')
        return results

    @staticmethod
    def get_chart_data(days=7):
        sql = """
            SELECT 
                DATE(tanggal) as date,
                SUM(CASE WHEN type = 'pemasukan' THEN jumlah ELSE 0 END) as total_pemasukan,
                SUM(CASE WHEN type = 'pengeluaran' THEN jumlah ELSE 0 END) as total_pengeluaran
            FROM (
                SELECT tanggal, jumlah_pembayaran as jumlah, 'pemasukan' as type FROM pemasukan WHERE tanggal >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
                UNION ALL
                SELECT tanggal, jumlah_pengeluaran as jumlah, 'pengeluaran' as type FROM pengeluaran WHERE tanggal >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            ) as combined
            GROUP BY DATE(tanggal)
            ORDER BY date ASC
        """
        results = DatabaseConnection.execute_query(sql, (days-1, days-1))
        
        from datetime import datetime, timedelta
        
        # Build array of last N days
        today = datetime.now().date()
        date_list = [today - timedelta(days=x) for x in range(days-1, -1, -1)]
        
        # Map DB results by date
        db_map = {}
        for row in results:
            db_map[row['date']] = row
            
        labels = []
        pemasukan = []
        pengeluaran = []
        
        for d in date_list:
            if d == today:
                labels.append('Hari ini')
            elif d == today - timedelta(days=1):
                labels.append('H-1')
            else:
                diff = (today - d).days
                labels.append(f'H-{diff}')
                
            day_data = db_map.get(d, {})
            pemasukan.append(float(day_data.get('total_pemasukan', 0)))
            pengeluaran.append(float(day_data.get('total_pengeluaran', 0)))
            
        return {
            "labels": labels,
            "pemasukan": pemasukan,
            "pengeluaran": pengeluaran
        }

    @staticmethod
    def get_top_petugas(limit=5):
        sql = """
            SELECT 
                p.nama_petugas as nama_lengkap, 
                p.no_telp as no_telepon, 
                COALESCE(SUM(g.total_gaji), 0) as total_transaksi,
                COUNT(g.id) as jumlah_transaksi
            FROM petugas p
            JOIN gaji_petugas g ON p.id = g.id_petugas
            GROUP BY p.id
            ORDER BY total_transaksi DESC
            LIMIT %s
        """
        return DatabaseConnection.execute_query(sql, (limit,))
