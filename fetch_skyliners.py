import urllib.request
import re
import json
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_skyliner_details(kind):
    # Get timetable for Ueno
    url = f"https://transit.yahoo.co.jp/timetable/22661/2951?kind={kind}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        html = res.read().decode('utf-8', errors='ignore')
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">([\s\S]*?)</script>', html)
    data = json.loads(m.group(1))
    tt_data = data['props']['pageProps']['timetableItem']
    
    skyliner_items = []
    for h_obj in tt_data['hourTimeTable']:
        hour = int(h_obj['hour'])
        for m_obj in h_obj['minTimeTable']:
            minute = int(m_obj['minute'])
            tname = m_obj.get('trainName', '')
            kind_id = m_obj.get('kindId', '')
            train_id = m_obj.get('trainId', '')
            if "スカイライナー" in tname or kind_id == "2":
                skyliner_items.append({
                    'dep_time': f"{hour:02d}:{minute:02d}",
                    'name': tname,
                    'trainId': train_id,
                    'hh': hour,
                    'mm': minute
                })
                
    results = []
    print(f"Fetching {len(skyliner_items)} Skyliners for kind={kind}...")
    for item in skyliner_items:
        detail_url = f"https://transit.yahoo.co.jp/timetable/22661/2951/{item['trainId']}?kind={kind}&hh={item['hh']}&mm={item['mm']}"
        try:
            req_d = urllib.request.Request(detail_url, headers=headers)
            with urllib.request.urlopen(req_d) as res_d:
                html_d = res_d.read().decode('utf-8', errors='ignore')
            m_d = re.search(r'<script id="__NEXT_DATA__" type="application/json">([\s\S]*?)</script>', html_d)
            if not m_d:
                continue
            d_json = json.loads(m_d.group(1))
            tt_detail = d_json['props']['pageProps']['timetableStationTrainResult']['timetable']
            stops = tt_detail.get('stopStation', [])
            
            t2_arr = None
            nrt_arr = None
            for s in stops:
                st_name = s['stationName']
                if "第２ビル" in st_name or "第2ビル" in st_name:
                    t2_arr = s.get('arrivalTime')
                elif "成田空港" in st_name:
                    nrt_arr = s.get('arrivalTime')
                    
            if not nrt_arr and stops:
                nrt_arr = stops[-1].get('arrivalTime')
            if not t2_arr and nrt_arr:
                # typically 2-3 mins before
                arr_m = int(nrt_arr[:2]) * 60 + int(nrt_arr[2:]) - 3
                t2_arr = f"{arr_m//60:02d}{arr_m%60:02d}"
                
            def fmt_time(t_raw):
                if not t_raw:
                    return ""
                t_str = str(t_raw).zfill(4)
                return f"{t_str[:2]}:{t_str[2:]}"
                
            arr_time_str = fmt_time(nrt_arr)
            t2_time_str = fmt_time(t2_arr)
            
            # calculate total_min
            dep_m = item['hh'] * 60 + item['mm']
            arr_h, arr_min = map(int, arr_time_str.split(':'))
            if arr_h < 4:
                arr_h += 24
            arr_m_calc = arr_h * 60 + arr_min
            total_min = arr_m_calc - dep_m
            
            # Time band
            if 5 <= item['hh'] < 10:
                time_band = "morning"
            elif 10 <= item['hh'] < 16:
                time_band = "day"
            elif 16 <= item['hh'] < 20:
                time_band = "evening"
            else:
                time_band = "night"
                
            results.append({
                'dep_time': item['dep_time'],
                'arr_time': arr_time_str,
                't2_arr_time': t2_time_str,
                'total_min': total_min,
                'via': 'スカイアクセス線経由',
                'is_direct': True,
                'train_type': 'スカイライナー',
                'liner_name': tt_detail.get('displayName', item['name']),
                'transfer_station': '直通',
                'connect_train': '直通',
                'transfer_desc': f"{tt_detail.get('displayName', item['name'])}（全席指定）で空港第2ビル・成田空港へ直通最速",
                'time_band': time_band,
                'fare_ic': 2572, # 1,272 + 1,300
                'fare_ticket': 2580, # 1,280 + 1,300
                'is_liner': True,
                'stations': ['京成上野', '成田空港(鉄道)'],
                'transports': [f"京成成田スカイアクセス線 {tt_detail.get('displayName', item['name'])} 成田空港行"]
            })
            time.sleep(0.15)
        except Exception as e:
            print(f"Error {item['dep_time']}: {e}")
            
    print(f"Fetched {len(results)} Skyliners for kind={kind}")
    return results

w_skyliners = fetch_skyliner_details(1)
h_skyliners = fetch_skyliner_details(2)

with open('skyliner_data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'weekday': w_skyliners,
        'weekend': h_skyliners
    }, f, ensure_ascii=False, indent=2)

print("Saved skyliner_data.json successfully!")
