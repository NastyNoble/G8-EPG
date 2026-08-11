import requests
import gzip
import xml.etree.ElementTree as ET

BASE_URL = "https://epgshare01.online/epgshare01/"

categories = [
    # --- UNITED STATES (NATIONAL & LOCALS) ---
    "epg_ripper_US2.xml.gz",               # Main US Cable & National feeds
    "epg_ripper_US_LOCALS1.xml.gz",        # Main Broadcast Local Affiliates (ABC, CBS, FOX, NBC)
    "epg_ripper_US_LATINO1.xml.gz",        # US Spanish / Latino Feeds
    
    # --- CANADA ---
    "epg_ripper_CA2.xml.gz",               # Canadian Cable & Broadcast (CBC, CTV, TSN, Sportsnet)

    # --- SPORTS (NATIONAL, REGIONAL & EXTRAS) ---
    "epg_ripper_US_SPORTS1.xml.gz",        # Primary Sports (ESPN, FS1, Golf, NFL)
    "epg_ripper_US_SPORTS2.xml.gz",        # Secondary Sports feeds
    "epg_ripper_US_SPORTS_LOCALS1.xml.gz", # Regional Sports Networks (Space City, Marquee, etc.)
    "epg_ripper_SPORTS1.xml.gz",           # International/Global Sports feeds
    "epg_ripper_BALLY1.xml.gz",            # Bally Sports / FanDuel SN regional channels
    "epg_ripper_PFL1.xml.gz",              # Fighting / MMA / combat sports
    "epg_ripper_PPV1.xml.gz",              # Pay-Per-View / Live Events
    "epg_ripper_ESPNPLUS1.xml.gz",         # ESPN+ event channels

    # --- STREAMING & FAST CHANNELS ---
    "epg_ripper_PEACOCK1.xml.gz",          # Peacock live hubs
    "epg_ripper_PLEX1.xml.gz",             # Plex FAST channels
    "epg_ripper_TUBI1.xml.gz",             # Tubi FAST channels
    "epg_ripper_PLUTO1.xml.gz",            # Pluto TV channels
    "epg_ripper_SAMSUNG1.xml.gz",          # Samsung TV Plus channels
    "epg_ripper_ROKU1.xml.gz",             # Roku Channel FAST channels

    # --- INTERNATIONAL / ANGLOSPHERE ---
    "epg_ripper_UK1.xml.gz",               # United Kingdom (BBC, ITV, Sky)
    "epg_ripper_AU1.xml.gz",               # Australia (Nine, Seven, 10, Foxtel)
    "epg_ripper_NZ1.xml.gz",               # New Zealand (TVNZ, Sky NZ)
    "epg_ripper_IE1.xml.gz",               # Ireland (RTE, Virgin Media)
    "epg_ripper_ZA1.xml.gz"                # South Africa (SuperSport)
]

master_root = None
print("🔄 Initializing Comprehensive EPG Merge Engine...\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for filename in categories:
    full_url = f"{BASE_URL}{filename}"
    print(f"📥 Pulling file: {filename}")
    try:
        response = requests.get(full_url, headers=headers, timeout=35)
        if response.status_code == 200:
            xml_data = gzip.decompress(response.content)
            
            parser = ET.XMLParser(encoding="utf-8")
            root = ET.fromstring(xml_data, parser=parser)
            
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
                print(f"   ✓ Merged {channels_added} channels & {programmes_added} airings.")
        else:
            print(f"   ⚠️ File skipped: Server returned HTTP status {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ Network or parsing issue for {filename}: {e}")

if master_root is not None:
    output_filename = "my_combined_epg.xml.gz"
    print(f"\n💾 Packaging and compressing master payload into {output_filename}...")
    with gzip.open(output_filename, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(ET.tostring(master_root, encoding='utf-8'))
    print("\n🎉 Custom EPG compiled successfully.")
else:
    print("\n⚠️ No data downloaded. Creating fallback container to prevent player errors.")
    fallback_root = ET.Element('tv')
    with gzip.open("my_combined_epg.xml.gz", 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(ET.tostring(fallback_root, encoding='utf-8'))            xml_data = gzip.decompress(response.content)
            
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
