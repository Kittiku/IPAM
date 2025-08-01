# data_provider.py
import pandas as pd
import ipaddress
from mysql_manager import MySQLManager # สมมติว่าไฟล์ mysql_manager.py ยังอยู่

class DataProvider:
    """
    คลาสศูนย์กลางสำหรับจัดการการเข้าถึงข้อมูล
    พยายามเชื่อมต่อ MySQL ก่อน หากล้มเหลวจะใช้ CSV เป็น Fallback โดยอัตโนมัติ
    """
    def __init__(self):
        self.db_manager = None
        self.csv_data = None
        self.port_data = None
        self.is_db_connected = False
        
        try:
            print("🗄️  Attempting to connect to MySQL database...")
            self.db_manager = MySQLManager()
            if self.db_manager.connection and self.db_manager.connection.is_connected():
                 self.is_db_connected = True
                 print("✅ MySQL database connected successfully.")
            else:
                 raise Exception("MySQL connection object not available or not connected.")
        except Exception as e:
            print(f"❌ Could not connect to MySQL: {e}. Falling back to CSV mode.")
            self._load_csv_fallback()

    def _load_csv_fallback(self):
        """โหลดข้อมูลจากไฟล์ CSV ในกรณีที่เชื่อมต่อ Database ไม่ได้"""
        try:
            print("📥 Loading CSV files as fallback...")
            self.csv_data = pd.read_csv('datalake.Inventory.csv')
            self.port_data = pd.read_csv('datalake.Inventory.port.csv', dtype={'id': 'str'}, low_memory=False)
            print("✅ Loaded CSV fallback data successfully.")
        except FileNotFoundError:
            self.csv_data = pd.DataFrame()
            self.port_data = pd.DataFrame()
            print("❌ Critical Error: Fallback CSV files not found. Data will be empty.")

    def get_network_stats(self):
        """ดึงข้อมูลสถิติเครือข่าย"""
        if self.is_db_connected:
            return self.db_manager.get_network_stats()
        
        # CSV Fallback Logic
        if self.csv_data is not None and not self.csv_data.empty:
            return {
                'total_devices': len(self.csv_data),
                'active_devices': len(self.csv_data[self.csv_data['status'] != 'DOWN']),
                'domains': self.csv_data['domain'].nunique(),
                'subnets': 189,  # Estimated for CSV
                'vendor_distribution': dict(self.csv_data['vendor'].value_counts().head(8))
            }
        # Default data if all fails
        return {'total_devices': 0, 'active_devices': 0, 'domains': 0, 'subnets': 0, 'vendor_distribution': {}}

    def get_network_tree(self):
        """ดึงโครงสร้าง Network Tree"""
        if self.is_db_connected:
            return self.db_manager.get_network_tree()
        
        # CSV Fallback Logic
        if self.csv_data is None or self.csv_data.empty:
            return {"name": "IPAM Network", "type": "root", "children": [], "count": 0}

        df = self.csv_data.copy()
        domain_mapping = {
            'CORE/AGGREGATION': 'Core Network', 'ACCESS': 'Access Network', 
            'DATACENTER': 'Data Center', 'WAN': 'WAN Network', 'CAMPUS': 'Campus Network',
            'METRO': 'Metro Network', 'CUSTOMER': 'Customer Premise', 'MGMT': 'Management Network'
        }
        tree = {"name": "IPAM Network", "type": "root", "id": "root", "children": [], "count": len(df)}
        
        categories = {}
        for _, row in df.iterrows():
            domain = row.get('domain', 'Unknown')
            if pd.isna(domain) or domain == '-': domain = "Unknown"
            category = domain_mapping.get(domain, "Network Equipment")
            if category not in categories:
                categories[category] = {"count": 0}
            categories[category]["count"] += 1

        for category_name, data in categories.items():
            tree["children"].append({
                "name": category_name, "type": "category", 
                "id": category_name.lower().replace(' ', '_'), "count": data["count"], "children": []
            })
        return tree


    def get_ip_conflicts(self):
        """ดึงข้อมูล IP Conflict"""
        if self.is_db_connected:
            return self.db_manager.get_ip_conflicts()
        # No conflict analysis for CSV fallback
        return {'total_conflicts': 0, 'conflicts': []}

    def get_port_analysis(self):
        """วิเคราะห์ IP จาก Port"""
        if self.is_db_connected:
            return self.db_manager.get_port_analysis()
            
        # CSV Fallback Logic
        if self.port_data is None or self.port_data.empty:
            return {'subnets': []}
        
        valid_ips = self.port_data[self.port_data['ifIP'].notna() & (self.port_data['ifIP'] != '-') & (self.port_data['ifIP'] != '')].copy()
        
        # ใช้ Vectorized operation แทนการวนลูป (เร็วกว่า)
        def get_subnet(ip):
            try:
                return str(ipaddress.IPv4Network(f"{ip}/24", strict=False))
            except:
                return None
        
        valid_ips['subnet'] = valid_ips['ifIP'].apply(get_subnet)
        valid_ips = valid_ips.dropna(subset=['subnet'])

        subnet_counts = valid_ips.groupby('subnet').size().reset_index(name='ip_count')
        subnet_list = subnet_counts.sort_values('ip_count', ascending=False).head(20).to_dict('records')
        
        # เพิ่มข้อมูลเปล่าๆ เข้าไปเพื่อให้โครงสร้าง response เหมือนกัน
        for item in subnet_list:
            item['device_count'] = 0 # CSV mode does not calculate this

        return {'subnets': subnet_list}