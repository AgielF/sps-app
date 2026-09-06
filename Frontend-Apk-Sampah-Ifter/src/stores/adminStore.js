import { ref } from 'vue';

// Data Dummy Petugas & User (untuk Dashboard/Data)
export const petugasList = ref([
    { id: 1, name: 'Jokowi', phone: '098765542312', address: 'Jl. Merdeka No. 1', status: 'Aktif' },
    { id: 2, name: 'Sahrani', phone: '087855423212', address: 'Jl. Pelajar No. 2', status: 'Non aktif' },
    { id: 3, name: 'Bahli', phone: '089855423212', address: 'Jl. Veteran No. 3', status: 'Aktif' },
]);

export const userList = ref([
    { id: 101, name: 'James', phone: '098638723735', address: 'Jl. Cikutra No. 9' },
    { id: 102, name: 'Budi', phone: '085738723735', address: 'Jl. Cikutra No. 9' },
    { id: 103, name: 'Sisca', phone: '081234567890', address: 'Jl. Dago Atas No. 10' },
]);

// Data Dummy Riwayat Transaksi/Aktivitas
export const riwayatAdminList = ref([
    // Tanggal Hari Ini (2025-10-19)
    { id: 1, type: 'Pemasukan', source: 'Pembayaran Sampah', desc: 'Transfer dari User James (4 Karung)', amount: 20000, date: '2025-10-19', status: 'Lunas' },
    { id: 2, type: 'Pemasukan', source: 'Pembayaran Sampah', desc: 'Cash dari User Tono (1 Karung)', amount: 5000, date: '2025-10-19', status: 'Lunas' },
    { id: 3, type: 'Pengeluaran', source: 'Komisi Petugas', desc: 'Komisi Petugas Jokowi (Shift Pagi)', amount: 50000, date: '2025-10-19', status: 'Selesai' },
    { id: 4, type: 'Aktivitas', source: 'Manajemen Petugas', desc: 'Petugas Bahli diaktifkan kembali.', amount: 0, date: '2025-10-19', status: 'Info' },
    
    // Tanggal Kemarin (2025-10-18)
    { id: 5, type: 'Pemasukan', source: 'Pembayaran Sampah', desc: 'Transfer dari User Budi (5 Karung)', amount: 25000, date: '2025-10-18', status: 'Lunas' },
    { id: 6, type: 'Pengeluaran', source: 'Operasional', desc: 'Pembelian 100 kantong sampah besar', amount: 120000, date: '2025-10-18', status: 'Selesai' },
    { id: 7, type: 'Aktivitas', source: 'Manajemen User', desc: 'User Sisca berhasil diverifikasi.', amount: 0, date: '2025-10-18', status: 'Info' },
    { id: 8, type: 'Pengeluaran', source: 'Gaji Bulanan', desc: 'Gaji Admin Bulan Oktober', amount: 500000, date: '2025-10-17', status: 'Selesai' },
]);

// Saldo Awal Simulasi
export const currentBalance = ref(525000); 

// Fungsi CRUD (dibersihkan dari unused vars)
export function addPetugas(newPetugas) { 
    const newId = petugasList.value.length + 1;
    petugasList.value.push({ id: newId, status: 'Aktif', ...newPetugas });
}
export function addUser(newUser) { 
    const newId = userList.value.length + 101;
    userList.value.push({ id: newId, ...newUser });
}
export function deletePetugas(id) { 
    const index = petugasList.value.findIndex(p => p.id === id);
    if (index !== -1) {
        petugasList.value.splice(index, 1);
        return true;
    }
    return false;
}
export function deleteUser(id) { 
    const index = userList.value.findIndex(u => u.id === id);
    if (index !== -1) {
        userList.value.splice(index, 1);
        return true;
    }
    return false;
}