# routes/warga.py
from flask import Blueprint, request, jsonify
import sys
import os

# Ensure repositories path is accessible
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from repositories.warga_repository import WargaRepository

warga_bp = Blueprint('warga', __name__, url_prefix='/api/warga')

@warga_bp.route('/', methods=['GET'], strict_slashes=False)
def get_all_warga():
    try:
        rows = WargaRepository.get_all()
        
        import re
        for row in rows:
            if row.get('lokasi'):
                match = re.search(r'RT\s*(\d+)\s*/\s*RW\s*(\d+)', row['lokasi'], re.IGNORECASE)
                if match:
                    row['rt'] = match.group(1)
                    row['rw'] = match.group(2)
                else:
                    row['rt'] = '-'
                    row['rw'] = '-'
            else:
                row['rt'] = '-'
                row['rw'] = '-'
                
        return jsonify({"success": True, "data": rows}), 200
    except Exception as e:
        print("get_all_warga error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

@warga_bp.route('/<int:warga_id>', methods=['GET'])
def get_warga_by_id(warga_id):
    try:
        row = WargaRepository.get_by_id(warga_id)
        if not row:
            return jsonify({"success": False, "message": "Data tidak ditemukan"}), 404
            
        import re
        if row.get('lokasi'):
            match = re.search(r'RT\s*(\d+)\s*/\s*RW\s*(\d+)', row['lokasi'], re.IGNORECASE)
            if match:
                row['rt'] = match.group(1)
                row['rw'] = match.group(2)
                
        return jsonify({"success": True, "data": row}), 200
    except Exception as e:
        print("get_warga_by_id error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

@warga_bp.route('/by-user/<int:user_id>', methods=['GET'])
def get_warga_by_user(user_id):
    try:
        row = WargaRepository.get_by_user_id(user_id)
        if not row:
            return jsonify({"success": False, "message": "Data warga tidak ditemukan"}), 404
            
        import re
        if row.get('lokasi'):
            match = re.search(r'RT\s*(\d+)\s*/\s*RW\s*(\d+)', row['lokasi'], re.IGNORECASE)
            if match:
                row['rt'] = match.group(1)
                row['rw'] = match.group(2)
                
        return jsonify({"success": True, "data": row}), 200
    except Exception as e:
        print("get_warga_by_user error:", e)
        return jsonify({
            "success": True,
            "data": {
                "id": user_id, "nama_warga": "Warga", "alamat": "", "lokasi": "",
                "longitude": 0, "latitude": 0, "username": f"user_{user_id}",
                "status": "active", "role": "warga"
            }
        }), 200

@warga_bp.route('/create', methods=['POST'])
def create_warga():
    data = request.json or {}
    
    # Map frontend payload keys
    data['nama_warga'] = data.get('nama_lengkap') or data.get('nama_warga')
    data['lokasi'] = data.get('alamat_lengkap') or data.get('lokasi')

    required = ["username", "password", "nama_warga", "rt", "rw", "lokasi", "latitude", "longitude"]
    for field in required:
        if field not in data or data[field] == "":
            return jsonify({"success": False, "message": f"{field} tidak boleh kosong"}), 400

    try:
        WargaRepository.create(data)
        return jsonify({"success": True, "message": "Warga berhasil dibuat"}), 201
    except Exception as e:
        print("create_warga error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

@warga_bp.route('/<int:warga_id>', methods=['PUT'], strict_slashes=False)
def update_warga(warga_id):
    data = request.json or {}
    
    # Map frontend payload keys
    data['nama_warga'] = data.get('nama_lengkap') or data.get('nama_warga')
    data['lokasi'] = data.get('alamat_lengkap') or data.get('lokasi')
    
    required = ["username", "nama_warga", "rt", "rw", "lokasi", "latitude", "longitude"]
    for field in required:
        if field not in data or data[field] == "":
            return jsonify({"success": False, "message": f"{field} tidak boleh kosong"}), 400

    try:
        WargaRepository.update(warga_id, data)
        return jsonify({"success": True, "message": "Warga berhasil diupdate"}), 200
    except Exception as e:
        print("update_warga error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
