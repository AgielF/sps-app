import { ref } from 'vue';
import { date } from 'quasar';

// Data Dummy Tugas
export const tasks = ref([
  { id: 1, name: 'Martin', address: 'Jl. Ciwidey no.12', status: 'Belum diambil', bags: 0, payment: null, amount: 0, date: '2025-10-19' },
  { id: 2, name: 'Konho', address: 'Jl. Majalengka no.67', status: 'Belum diambil', bags: 0, payment: null, amount: 0, date: '2025-10-19' },
  { id: 3, name: 'James', address: 'Jl. Cikutra no.67', status: 'Sudah diambil', bags: 4, payment: 'Transfer bank', amount: 20000, date: '2025-10-19' },
  { id: 4, name: 'Jangin', address: 'Jl. Asia Afrika no.1', status: 'Sudah diambil', bags: 2, payment: 'Transfer bank', amount: 10000, date: '2025-10-19' },
  { id: 5, name: 'Tono', address: 'Jl. Pasupati no.55', status: 'Sudah diambil', bags: 1, payment: 'Cash', amount: 5000, date: '2025-10-19' },
  { id: 6, name: 'Budi', address: 'Jl. Setiabudi no.1', status: 'Sudah diambil', bags: 5, payment: 'Cash', amount: 25000, date: '2025-10-18' },
  { id: 7, name: 'Santi', address: 'Jl. Dago no.2', status: 'Belum diambil', bags: 0, payment: null, amount: 0, date: '2025-10-18' },
]);

export function addTask(newTask) {
  const newId = tasks.value.length + 1;
  const today = date.formatDate(Date.now(), 'YYYY-MM-DD');
  
  tasks.value.push({
    id: newId,
    name: newTask.name,
    address: newTask.address,
    status: 'Sudah diambil',
    bags: newTask.bags,
    payment: newTask.paymentMethod === 'cash' ? 'Cash' : 'Transfer bank',
    amount: parseInt(newTask.total.replace(/\./g, '')),
    date: today 
  });
}