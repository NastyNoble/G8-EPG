import requests
import gzip
import xml.etree.ElementTree as ET

BASE_URL = "https://epgshare01.online/epgshare01/"

categories = [
    # --- UNITED STATES (NATIONAL & LOCALS) ---
    "epg_ripper_US2.xml.gz",               # Main US Cable & National feeds
    "epg_ripper_US_LOCALS1.xml.gz",        # Main Broadcast Local Affiliates
    "epg_ripper_US_LATINO1.xml.gz",        # US Spanish / Latino Feeds
    
    # --- CANADA ---
    "epg_ripper_CA2.xml.gz",               # Canadian Cable & Broadcast

    # --- SPORTS (NATIONAL, REGIONAL & EXTRAS) ---
    "epg_ripper_US_SPORTS1.xml.gz",        # Primary Sports
    "epg_ripper_US_SPORTS2.xml.gz",        # Secondary Sports
    "epg_ripper_US_SPORTS_LOCALS1.xml.gz", # Regional Sports Networks (Space City, Marquee)
    "epg_ripper_SPORTS1.xml.gz",           # Global Sports
    "epg_ripper_BALLY1.xml.gz",            # Bally Sports / FanDuel SN
    "epg_ripper_PFL1.xml.gz",              # Fighting / MMA
    "epg_ripper_PPV1.xml.gz",              # Pay-Per-View
    "epg_ripper_ESPNPLUS1.xml.gz",         # ESPN+ events

    # --- STREAMING & FAST CHANNELS ---
    "epg_ripper_PEACOCK1.xml.gz",          # Peacock live hubs
    "epg_ripper_PLEX1.xml.gz",             # Plex FAST channels
    "epg_ripper_TUBI1.xml.gz",             # Tubi FAST channels
    "epg_ripper_PLUTO1.xml.gz",            # Pluto TV
    "epg_ripper_SAMSUNG1.xml.gz",          # Samsung TV Plus
    "epg_ripper_ROKU1.xml.gz",             # Roku Channel

    # --- INTERNATIONAL / ANGLOSPHERE ---
    "epg_ripper_UK1.xml.gz",               # United Kingdom
    "epg_ripper_AU1.xml.gz",               # Australia
    "epg_ripper_NZ1.xml.gz",               # New Zealand
    "epg_ripper_IE1.xml.gz",               # Ireland
    "epg_ripper_ZA1.xml.gz"                # South Africa
]

master_root = None
print("🔄 Initializing Robust EPG Merge Engine...\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for filename in categories:
    full_url = f"{BASE_URL}{filename}"
    print(f"📥 Pulling file: {filename}")
    try:
        response = requests.get(full_url, headers=headers, timeout=30)
        if response.status_code == 200:
            # Safely attempt decompression and XML parsing separately
            try:
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
            except (gzip.BadGzipFile, ET.ParseError) as parse_err:
                print(f"   ⚠️ File corrupted or unparseable: {parse_err}")
        else:
            print(f"   ⚠️ Server returned HTTP status {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ Request failed for {filename}: {e}")

if master_root is not None:
    output_filename = "my_combined_epg.xml.gz"
    print(f"\n💾 Packaging into {output_filename}...")
    with gzip.open(output_filename, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(ET.tostring(master_root, encoding='utf-8'))
    print("\n🎉 Custom EPG compiled successfully.")
else:
    print("\n⚠️ Creating fallback blank container to prevent pipeline exit errors.")
    fallback_root = ET.Element('tv')
    with gzip.open("my_combined_epg.xml.gz", 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(ET.tostring(fallback_root, encoding='utf-8'))
