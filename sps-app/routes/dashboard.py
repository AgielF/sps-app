# routes/dashboard.py
from flask import Blueprint, jsonify, request, make_response
import sys
import os

# Ensure repositories path is accessible
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from repositories.dashboard_repository import DashboardRepository

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,PATCH,DELETE,OPTIONS'
    return response

@dashboard_bp.route('/quick-stats', methods=['GET', 'OPTIONS'])
def get_quick_stats():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = {
            "today": DashboardRepository.get_today_pemasukan(),
            "month": DashboardRepository.get_month_pemasukan(),
            "petugas_stats": DashboardRepository.get_total_petugas(),
            "active_petugas": {"count": DashboardRepository.get_total_petugas().get('total_petugas', 0)},
            "today_schedule_count": DashboardRepository.get_today_schedule_count()
        }
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        print("get_quick_stats error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

@dashboard_bp.route('/summary', methods=['GET', 'OPTIONS'])
def get_dashboard_summary():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = {
            "today_schedule": DashboardRepository.get_today_schedule(),
            "recent_transactions": DashboardRepository.get_recent_transactions(8),
            "monthly_stats": DashboardRepository.get_monthly_stats(),
            "chart_data": DashboardRepository.get_chart_data(7),
            "top_petugas": DashboardRepository.get_top_petugas(5),
            "transaction_by_type": [] # Optional, UI might not even use it based on template inspection
        }
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("get_dashboard_summary error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
