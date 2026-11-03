import urllib.request
import re
import json
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_station_timetable(station_code, line_code, kind):
    url = f"https://transit.yahoo.co.jp/timetable/{station_code}/{line_code}?kind={kind}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        html = res.read().decode('utf-8', errors='ignore')
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">([\s\S]*?)</script>', html)
    data = json.loads(m.group(1))
    return data['props']['pageProps']['timetableItem']

def parse_t(t_str):
    h, m = map(int, t_str.split(':'))
    return (h + 24 if h < 4 else h) * 60 + m

def format_min(m):
    h = (m // 60) % 24
    mm = m % 60
    return f"{h:02d}:{mm:02d}"

def get_skyliners_detailed(kind):
    tt = fetch_station_timetable("22661", "2951", kind)
    skyliners_basic = []
    for h_obj in tt['hourTimeTable']:
        hour = int(h_obj['hour'])
        for m_obj in h_obj['minTimeTable']:
            name = m_obj.get('trainName', '')
            if "スカイライナー" in name or m_obj.get('kindId') == '2':
                minute = int(m_obj['minute'])
                train_id = m_obj.get('trainId')
                skyliners_basic.append({
                    'dep_time': f"{hour:02d}:{minute:02d}",
                    'name': name,
                    'train_id': train_id,
                    'hour': hour,
                    'minute': minute
                })
                
    detailed = []
    print(f"Fetching details for {len(skyliners_basic)} skyliners (kind {kind})...")
    for s in skyliners_basic:
        url = f"https://transit.yahoo.co.jp/timetable/22661/2951/{s['train_id']}?kind={kind}&hh={s['hour']}&mm={s['minute']}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as res:
                html = res.read().decode('utf-8', errors='ignore')
            m = re.search(r'<script id="__NEXT_DATA__" type="application/json">([\s\S]*?)</script>', html)
            data = json.loads(m.group(1))
            t_obj = data['props']['pageProps']['timetableStationTrainResult']['timetable']
            stops = t_obj.get('stopStation', [])
            
            t2_arr = None
            t1_arr = None
            stop_names = []
            for st in stops:
                st_name = st.get('stationName', '')
                stop_names.append(st_name)
                arr_t = st.get('arrivalTime')
                if "第２ビル" in st_name and arr_t:
                    t2_arr = f"{int(arr_t[:2]):02d}:{int(arr_t[2:]):02d}"
                elif "成田空港" in st_name and arr_t:
                    t1_arr = f"{int(arr_t[:2]):02d}:{int(arr_t[2:]):02d}"
                    
            if not t1_arr and t2_arr:
                # Terminal 1 is 3 mins after Terminal 2
                t1_arr = format_min(parse_t(t2_arr) + 3)
            elif not t2_arr and t1_arr:
                t2_arr = format_min(parse_t(t1_arr) - 3)
                
            dep_m = parse_t(s['dep_time'])
            arr_m = parse_t(t1_arr)
            total_min = arr_m - dep_m
            
            # Clean name
            display_name = t_obj.get('displayName', s['name'])
            # e.g. "特急 スカイライナー1号" -> "スカイライナー1号"
            clean_name = display_name.replace("特急", "").strip()
            
            # Intermediate stops description
            # stops except Ueno, Nippori, T2, T1
            intermediate = [st for st in stop_names if st not in ['京成上野', '日暮里', '空港第２ビル(鉄道)', '成田空港(鉄道)']]
            if intermediate:
                via_desc = f"日暮里・{'・'.join(intermediate)}停車"
            else:
                via_desc = "日暮里のみ停車（最速ノンストップ運行）"
                
            dep_h = int(s['dep_time'].split(':')[0])
            if 5 <= dep_h < 10:
                time_band = "morning"
            elif 10 <= dep_h < 16:
                time_band = "day"
            elif 16 <= dep_h < 20:
                time_band = "evening"
            else:
                time_band = "night"
                
            item = {
                'dep_time': s['dep_time'],
                'arr_time': t1_arr,
                't2_arr_time': t2_arr,
                'total_min': total_min,
                'via': '成田スカイアクセス線経由',
                'is_direct': True,
                'is_skyliner': True,
                'train_type': 'スカイライナー',
                'liner_name': clean_name,
                'transfer_station': '直通',
                'connect_train': '直通',
                'transfer_desc': f"{clean_name} 直通（{via_desc}・全席指定）",
                'time_band': time_band,
                'fare_ic': 2572, # 1,272 + 1,300
                'fare_ticket': 2580, # 1,280 + 1,300
                'stations': ['京成上野', '成田空港(鉄道)'],
                'transports': [f"成田スカイアクセス線 {clean_name} 成田空港行"]
            }
            detailed.append(item)
            time.sleep(0.15)
        except Exception as e:
            print(f"Error fetching {s['train_id']}: {e}")
            time.sleep(0.5)
            
    return detailed

w_skyliners_detailed = get_skyliners_detailed(1)
h_skyliners_detailed = get_skyliners_detailed(2)

with open('C:\\Users\\HINOTORI\\.gemini\\antigravity\\scratch\\jikoku_nrt\\skyliners.json', 'w', encoding='utf-8') as f:
    json.dump({
        'weekday': w_skyliners_detailed,
        'weekend': h_skyliners_detailed
    }, f, ensure_ascii=False, indent=2)

print(f"Saved {len(w_skyliners_detailed)} weekday and {len(h_skyliners_detailed)} weekend skyliners!")
