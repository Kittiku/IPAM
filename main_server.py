# main_server.py
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from data_provider import DataProvider # <-- Import คลาสใหม่

# ================== FLASK APP INITIALIZATION ==================
app = Flask(__name__)
CORS(app)

# ================== DATA PROVIDER INITIALIZATION ==================
print("\n" + "="*60)
print("🚀 Initializing IPAM System Data Provider...")
data_provider = DataProvider() # <-- สร้าง instance ของ DataProvider แค่ครั้งเดียว
print("="*60)


# ================== CENTRALIZED ERROR HANDLER ==================
@app.errorhandler(Exception)
def handle_exception(e):
    """
    จัดการ error ทั้งหมดที่เกิดขึ้นใน application และส่ง response เป็น JSON
    """
    import traceback
    traceback.print_exc() # พิมพ์ error stack ออกมาใน console เพื่อ debug
    return jsonify(error=f"An internal server error occurred: {e}"), 500


# ================== WEB ROUTES ==================
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('main_dashboard.html')

@app.route('/ip-management')
def ip_management():
    """IP Management page"""
    return render_template('ip_management_complete.html')


# ================== API ROUTES (REFACTORED) ==================
# โค้ดใน API routes จะสะอาดขึ้นมาก ไม่มีการเช็ค if/else ซ้ำซ้อน

@app.route('/api/ipam/stats')
def get_stats():
    """Return network statistics"""
    return jsonify(data_provider.get_network_stats())

@app.route('/api/ipam/tree-data')
def get_tree_data():
    """Return network tree structure"""
    return jsonify(data_provider.get_network_tree())

@app.route('/api/ipam/ip-conflicts')
def get_ip_conflicts():
    """Return IP address conflicts"""
    return jsonify(data_provider.get_ip_conflicts())

@app.route('/api/ipam/port-ips')
def get_port_ips():
    """Return port IP analysis"""
    return jsonify(data_provider.get_port_analysis())

@app.route('/api/ipam/refresh-cache')
def refresh_cache():
    """Refresh database cache (ถ้ามี)"""
    if data_provider.is_db_connected and hasattr(data_provider.db_manager, 'clear_cache'):
        data_provider.db_manager.clear_cache()
        return jsonify({"message": "Cache refreshed successfully"})
    else:
        return jsonify({"message": "No database cache to refresh (Running in CSV mode)"})

# ================== MAIN EXECUTION ==================
if __name__ == '__main__':
    print(f"\n📊 System Status:")
    if data_provider.is_db_connected:
        print(f"   Database: MySQL Connected ✅")
    else:
        print(f"   Database: CSV Fallback ⚠️")
    
    print(f"\n🌐 Server starting, access URLs:")
    print(f"   Dashboard: http://127.0.0.1:5005")
    print(f"   IP Management:  http://127.0.0.1:5005/ip-management")
    
    print(f"\n" + "="*60)
    print("✅ Server ready and waiting for connections...")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5005)