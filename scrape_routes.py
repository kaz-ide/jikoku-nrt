import urllib.request
import urllib.parse
import re
import json
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def search_routes_for_date(date_str, output_file):
    y = date_str[:4]
    m = date_str[4:6]
    d = date_str[6:8]
    
    all_routes = []
    seen_keys = set()
    
    # hours 5 to 23
    for hh in range(5, 24):
        print(f"Searching hour {hh} for date {date_str}...")
        # Check every 10 or 15 mins to catch all connections
        for mm in [0, 10, 20, 30, 40, 50]:
            params = {
                'from': '京成上野',
                'to': '成田空港(鉄道)',
                'y': y,
                'm': m,
                'd': d,
                'hh': str(hh),
                'm1': str(mm // 10),
                'm2': str(mm % 10),
                'type': '1',
                'ticket': 'ic',
                'ws': '3',
                's': '0',
                'al': '0',
                'shin': '0',
                'ex': '0', # no liner!
                'hb': '0',
                'lb': '0',
                'sr': '0',
            }
            url = f"https://transit.yahoo.co.jp/search/result?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req) as res:
                    html = res.read().decode('utf-8', errors='ignore')
            except Exception as e:
                print(f"Error {hh}:{mm}: {e}")
                time.sleep(1)
                continue
            
            # parse route01, route02, route03
            route_divs = re.findall(r'<div id="route0\d"[\s\S]*?(?=<div id="route0\d"|<!-- /#route|\s*<div class="navRoute">|$)', html)
            for r_html in route_divs:
                time_m = re.search(r'<li class="time">([\s\S]*?)</li>', r_html)
                if not time_m:
                    continue
                time_text = re.sub(r'<[^>]+>', '', time_m.group(1)).strip()
                times = re.findall(r'(\d{2}:\d{2})発→(\d{2}:\d{2})着', time_text)
                if not times:
                    continue
                dep_time, arr_time = times[0]
                
                # Check hour of dep_time, should be roughly around search time
                dep_h = int(dep_time.split(':')[0])
                if dep_h < 4:
                    dep_h += 24
                # ignore if wrapped to next day
                if dep_h > 24:
                    continue
                    
                total_time_m = re.search(r'(\d+)時間(\d+)分', time_text)
                if total_time_m:
                    total_min = int(total_time_m.group(1)) * 60 + int(total_time_m.group(2))
                else:
                    only_min = re.search(r'(\d+)分', time_text)
                    total_min = int(only_min.group(1)) if only_min else 0
                    
                stations_raw = re.findall(r'<div class="station">[\s\S]*?<dt>([\s\S]*?)</dt>[\s\S]*?</div>', r_html)
                stations = [re.sub(r'\s+', '', re.sub(r'<[^>]+>', '', s)) for s in stations_raw]
                
                # Only interested if starting at 京成上野 and ending at 成田空港(鉄道)
                if not stations or stations[0] != "京成上野" or "成田空港" not in stations[-1]:
                    continue
                    
                transports_raw = re.findall(r'<li class="transport">[\s\S]*?<div>([\s\S]*?)</div>', r_html)
                transports = [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)).strip() for t in transports_raw]
                
                # Determine route type
                full_text = " ".join(transports)
                is_skyaccess = "スカイアクセス" in full_text or "北総" in full_text
                via = "スカイアクセス線経由" if is_skyaccess else "京成本線経由"
                
                is_direct = len(stations) <= 2
                
                # key to deduplicate
                route_key = (dep_time, arr_time, via, is_direct, tuple(stations), tuple(transports))
                if route_key in seen_keys:
                    continue
                seen_keys.add(route_key)
                
                all_routes.append({
                    'dep_time': dep_time,
                    'arr_time': arr_time,
                    'total_min': total_min,
                    'via': via,
                    'is_direct': is_direct,
                    'stations': stations,
                    'transports': transports
                })
            time.sleep(0.3)
            
    # Sort by dep_time
    all_routes.sort(key=lambda r: (int(r['dep_time'].split(':')[0]) if int(r['dep_time'].split(':')[0]) >= 4 else int(r['dep_time'].split(':')[0]) + 24, int(r['dep_time'].split(':')[1]), r['total_min']))
    print(f"Total unique routes found for {date_str}: {len(all_routes)}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_routes, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    search_routes_for_date('20241106', 'weekday_routes.json')
    search_routes_for_date('20241109', 'weekend_routes.json')
