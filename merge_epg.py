import requests
import gzip
import xml.etree.ElementTree as ET

BASE_URL = "https://epgshare01.online/epgshare01/"

categories = [
    # --- UNITED STATES & PLATFORMS ---
    "epg_ripper_US_LOCALS1.xml.gz",  
    "epg_ripper_US_LOCALS2.xml.gz",  
    "epg_ripper_US_SPORTS1.xml.gz",  # National Sports (ESPN, FS1, NFL Network)
    "epg_ripper_US_SPORTS2.xml.gz",  
    "epg_ripper_US_SPORTS_LOCALS1.xml.gz", # Regional Sports (Space City, Bally, etc.)
    "epg_ripper_SPORTS1.xml.gz",     
    "epg_ripper_PEACOCK1.xml.gz",    
    
    # --- INTERNATIONAL REGIONS ---
    "epg_ripper_UK1.xml.gz",         
    "epg_ripper_AU1.xml.gz",         
    "epg_ripper_NZ1.xml.gz"          
]

master_root = None
print("🔄 Initializing EPG Merge Core Engine...\n")

# Browser headers to ensure smooth downloads without server rejection
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for filename in categories:
    full_url = f"{BASE_URL}{filename}"
    print(f"📥 Pulling file: {filename}")
    try:
        response = requests.get(full_url, headers=headers, timeout=30)
        if response.status_code == 200:
            xml_data = gzip.decompress(response.content)
            
            # Safe parsing strategy to ignore malformed characters across regions
            parser = ET.XMLParser(encoding="utf-8")
            root = ET.fromstring(xml_data, parser=parser)
            
            if master_root is None:
                master_root = root
                print("   ✓ Root XML tree template set.")
            else:
                channels_added = 0
                programmes_added = 0
                for channel in root.findall('channel'):
                    master_root.append(channel)
                    channels_added += 1
                for programme in root.findall('programme'):
                    master_root.append(programme)
                    programmes_added += 1
                print(f"   ✓ Added {channels_added} channels & {programmes_added} timeline events.")
        else:
            print(f"   ⚠️ File skipped: Server returned status {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ Network/Parsing skip for {filename}: {e}")

# Save strategy: Always output the file as long as we successfully grabbed at least one source
if master_root is not None:
    output_filename = "my_combined_epg.xml.gz"
    print(f"\n💾 Compressing and packaging feed into {output_filename}...")
    with gzip.open(output_filename, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(ET.tostring(master_root, encoding='utf-8'))
    print("\n🎉 Custom EPG compiled perfectly!")
else:
    print("\n⚠️ No data downloaded. Creating a blank template file to prevent player crash.")
    fallback_root = ET.Element('tv')
    with gzip.open("my_combined_epg.xml.gz", 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(ET.tostring(fallback_root, encoding='utf-8'))
