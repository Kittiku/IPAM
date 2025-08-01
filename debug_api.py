"""
Test API และ Debug
"""

import requests
import json

def test_port_ips_detailed():
    """ทดสอบ API port-ips แบบละเอียด"""
    try:
        print("🔍 Testing /api/ipam/port-ips...")
        response = requests.get("http://127.0.0.1:5005/api/ipam/port-ips")
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Data Type: {type(data)}")
            print(f"Data Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            if isinstance(data, dict) and len(data) > 0:
                first_key = list(data.keys())[0]
                print(f"First subnet: {first_key}")
                print(f"First subnet data: {data[first_key]}")
            
            print(f"Full Response (first 500 chars): {json.dumps(data, indent=2)[:500]}...")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_all_apis():
    """ทดสอบ API ทั้งหมด"""
    apis = [
        "/api/ipam/stats",
        "/api/ipam/port-ips", 
        "/api/ipam/ip-conflicts"
    ]
    
    for api in apis:
        print(f"\n{'='*50}")
        print(f"Testing: {api}")
        print('='*50)
        
        try:
            response = requests.get(f"http://127.0.0.1:5005{api}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)[:200]}...")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    test_port_ips_detailed()
    print("\n" + "="*60)
    test_all_apis()
