from flask import Blueprint, request, jsonify, make_response
import sys
import os

# Ensure repositories path is accessible
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from repositories.laporan_repository import LaporanRepository

laporan_bp = Blueprint('laporan', __name__, url_prefix='/api/laporan')

@laporan_bp.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,PATCH,DELETE,OPTIONS'
        return response

@laporan_bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,PATCH,DELETE,OPTIONS'
    return response

@laporan_bp.route('/', methods=['GET'], strict_slashes=False)
def get_all_laporan():
    status = request.args.get('status')
    id_warga = request.args.get('id_warga')
    try:
        rows = LaporanRepository.get_all(status, id_warga)
        return jsonify({"success": True, "data": rows}), 200
    except Exception as e:
        print("get_all_laporan error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

@laporan_bp.route('/by-petugas/<int:id_petugas>', methods=['GET'])
def get_laporan_by_petugas(id_petugas):
    try:
        rows = LaporanRepository.get_by_petugas(id_petugas)
        return jsonify({"success": True, "data": rows}), 200
    except Exception as e:
        print("get_laporan_by_petugas error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

@laporan_bp.route('/<int:laporan_id>', methods=['GET'])
def get_laporan_by_id(laporan_id):
    try:
        row = LaporanRepository.get_by_id(laporan_id)
        if not row:
            return jsonify({"success": False, "message": "Data laporan tidak ditemukan"}), 404
        return jsonify({"success": True, "data": row}), 200
    except Exception as e:
        print("get_laporan_by_id error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

@laporan_bp.route('', methods=['POST'], strict_slashes=False)
def create_laporan():
    data = request.json or {}
    required = ['user_id', 'jumlah_karung', 'jenis_pembayaran', 'tanggal_pengambilan', 'jenis_sampah']
    for field in required:
        if data.get(field) is None or data.get(field) == '':
            return jsonify({"success": False, "message": f"{field} wajib diisi"}), 400

    try:
        new_id = LaporanRepository.create(data)
        return jsonify({"success": True, "message": "Laporan sampah berhasil dibuat", "laporan_id": new_id}), 201
    except ValueError as ve:
        return jsonify({"success": False, "message": str(ve)}), 400
    except Exception as e:
        print("create_laporan error:", e)
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

@laporan_bp.route('/<int:laporan_id>/status', methods=['PATCH'])
def update_laporan_status(laporan_id):
    data = request.json or {}
    new_status = data.get('status')
    id_petugas = data.get('id_petugas')

    if not new_status:
        return jsonify({"success": False, "message": "status wajib diisi"}), 400

    new_status = new_status.lower()
    allowed_status = ['menunggu', 'dijemput', 'selesai']
    if new_status not in allowed_status:
        return jsonify({"success": False, "message": "Status tidak valid"}), 400

    try:
        LaporanRepository.update_status(laporan_id, new_status, id_petugas)
        return jsonify({"success": True, "message": f"Status laporan berhasil diubah menjadi '{new_status}'"}), 200
    except ValueError as ve:
        return jsonify({"success": False, "message": str(ve)}), 400
    except Exception as e:
        print("update_laporan_status error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

@laporan_bp.route('/<int:laporan_id>', methods=['DELETE'])
def delete_laporan(laporan_id):
    try:
        LaporanRepository.delete(laporan_id)
        return jsonify({"success": True, "message": "Laporan berhasil dibatalkan/dihapus"}), 200
    except ValueError as ve:
        return jsonify({"success": False, "message": str(ve)}), 400
    except Exception as e:
        print("delete_laporan error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

