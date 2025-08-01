"""
Test IP Analysis API
ทดสอบ API ที่เกี่ยวข้องกับ IP Management
"""

import requests
import json

def test_api():
    """ทดสอบ API endpoints"""
    base_url = "http://127.0.0.1:5005"
    
    apis = [
        "/api/ipam/stats",
        "/api/ipam/port-ips", 
        "/api/ipam/ip-conflicts",
        "/api/ipam/tree-data"
    ]
    
    for api in apis:
        try:
            print(f"\n🔍 Testing {api}...")
            response = requests.get(f"{base_url}{api}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"📊 Response: {json.dumps(data, indent=2)[:300]}...")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"🔍 Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error testing {api}: {e}")

if __name__ == "__main__":
    test_api()
