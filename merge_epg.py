import requests
import gzip
import xml.etree.ElementTree as ET

BASE_URL = "https://epgshare01.online/epgshare01/"

categories = [
    # --- UNITED STATES ---
    "epg_ripper_US1.xml.gz",         
    "epg_ripper_US2.xml.gz",         
    "epg_ripper_US_LOCALS1.xml.gz",  
    "epg_ripper_US_LOCALS2.xml.gz",  
    
    # --- SPORTS ---
    "epg_ripper_US_SPORTS1.xml.gz",  
    "epg_ripper_US_SPORTS2.xml.gz",  
    "epg_ripper_SPORTS1.xml.gz",     
    
    # --- STREAMING & EXTRAS ---
    "epg_ripper_PEACOCK1.xml.gz",    
    
    # --- INTERNATIONAL REGIONS ---
    "epg_ripper_UK1.xml.gz",         
    "epg_ripper_AU1.xml.gz",         
    "epg_ripper_NZ1.xml.gz"          
]

master_root = None
print("🔄 Launching Custom EPG Processing Script...\n")

for filename in categories:
    full_url = f"{BASE_URL}{filename}"
    print(f"📥 Pulling: {filename}")
    try:
        response = requests.get(full_url, timeout=45)
        if response.status_code == 200:
            xml_data = gzip.decompress(response.content)
            root = ET.fromstring(xml_data)
            if master_root is None:
                master_root = root
                print("   ✓ Base XML template established.")
            else:
                channels_added = 0
                programmes_added = 0
                for channel in root.findall('channel'):
                    master_root.append(channel)
                    channels_added += 1
                for programme in root.findall('programme'):
                    master_root.append(programme)
                    programmes_added += 1
                print(f"   ✓ Successfully appended {channels_added} channels & {programmes_added} airings.")
        else:
            print(f"   ❌ Server connection skipped (HTTP Code {response.status_code})")
    except Exception as e:
        print(f"   ❌ Execution block error for {filename}: {e}")

if master_root is not None:
    output_filename = "my_combined_epg.xml.gz"
    print(f"\n💾 Packing and compressing payload into {output_filename}...")
    with gzip.open(output_filename, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(ET.tostring(master_root, encoding='utf-8'))
    print("\n🎉 Custom XMLTV file successfully compiled.")
else:
    print("\n🚨 Build terminated: Data streams returned empty.")
