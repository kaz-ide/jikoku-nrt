import json
import re

def parse_t(t_str):
    h, m = map(int, t_str.split(':'))
    return (h + 24 if h < 4 else h) * 60 + m

def format_min(m):
    h = (m // 60) % 24
    mm = m % 60
    return f"{h:02d}:{mm:02d}"

def process_routes(file_name, day_type):
    with open(file_name, 'r', encoding='utf-8') as f:
        routes = json.load(f)
        
    cleaned = []
    for r in routes:
        # 1. Filter out JR/Metro/walking
        is_keisei_only = True
        for t in r['transports']:
            if any(forbidden in t for forbidden in ['ＪＲ', 'メトロ', '都営', '徒歩', 'バス', 'タクシー']):
                is_keisei_only = False
                break
            if not any(allowed in t for allowed in ['京成', '北総', 'スカイアクセス']):
                is_keisei_only = False
                break
        if not is_keisei_only:
            continue
            
        # 2. Exclude next day arrival (total_min >= 150)
        if r['total_min'] >= 150:
            continue
            
        first_t = r['transports'][0]
        train_type = "普通"
        if "アクセス特急" in first_t:
            train_type = "アクセス特急"
        elif "快速特急" in first_t:
            train_type = "快速特急"
        elif "通勤特急" in first_t:
            train_type = "通勤特急"
        elif "特急" in first_t:
            train_type = "特急"
        elif "快速" in first_t:
            train_type = "快速"
        elif "普通" in first_t:
            train_type = "普通"
            
        # Correct via for Access Express starting at Ueno
        via = r['via']
        if train_type == "アクセス特急":
            via = "スカイアクセス線経由"
        if any("アクセス特急" in t or "スカイアクセス" in t for t in r['transports']):
            via = "スカイアクセス線経由"
            
        # Exclude silly Ueno -> Nippori transfers when starting at Ueno
        if len(r['stations']) > 1 and r['stations'][1] == "日暮里":
            continue
            
        # Transfer details
        if r['is_direct']:
            transfer_station = "直通"
            connect_train = "直通"
            transfer_desc = "乗り換えなしで終点まで直通"
        else:
            transfer_station = r['stations'][1] if len(r['stations']) > 1 else "乗換"
            connect_t = r['transports'][1] if len(r['transports']) > 1 else ""
            if "アクセス特急" in connect_t:
                connect_train = "アクセス特急"
            elif "快速特急" in connect_t:
                connect_train = "快速特急"
            elif "特急" in connect_t:
                connect_train = "特急"
            elif "快速" in connect_t:
                connect_train = "快速"
            elif "普通" in connect_t:
                connect_train = "普通"
            else:
                connect_train = "連絡列車"
            transfer_desc = f"{transfer_station}で {connect_train}(成田空港行) に乗換"
            
        # Calculate Terminal 2/3 arrival time (2-3 mins before Terminal 1)
        arr_t_m = parse_t(r['arr_time'])
        t2_arr_m = arr_t_m - (2 if "スカイアクセス" in via else 3)
        t2_arr_time = format_min(t2_arr_m)
        
        # Time band
        dep_h = int(r['dep_time'].split(':')[0])
        if 5 <= dep_h < 10:
            time_band = "morning"
        elif 10 <= dep_h < 16:
            time_band = "day"
        elif 16 <= dep_h < 20:
            time_band = "evening"
        else:
            time_band = "night"
            
        # Fare info
        fare_ic = 1272 if "スカイアクセス" in via else 1057
        fare_ticket = 1280 if "スカイアクセス" in via else 1060
        
        cleaned.append({
            'dep_time': r['dep_time'],
            'arr_time': r['arr_time'],
            't2_arr_time': t2_arr_time,
            'total_min': r['total_min'],
            'via': via,
            'is_direct': r['is_direct'],
            'train_type': train_type,
            'transfer_station': transfer_station,
            'connect_train': connect_train,
            'transfer_desc': transfer_desc,
            'time_band': time_band,
            'fare_ic': fare_ic,
            'fare_ticket': fare_ticket,
            'stations': r['stations'],
            'transports': r['transports']
        })
        
    # Group by (arr_time, via) to keep optimal departures
    groups = {}
    for r in cleaned:
        key = (r['arr_time'], r['via'])
        if key not in groups:
            groups[key] = []
        groups[key].append(r)
        
    final_list = []
    for (arr_time, via), group in groups.items():
        directs = [r for r in group if r['is_direct']]
        transfers = [r for r in group if not r['is_direct']]
        
        # Keep all direct trains
        for d in directs:
            final_list.append(d)
            
        # For transfers, keep the one with latest departure (fastest / least wait)
        if transfers:
            best_transfer = max(transfers, key=lambda r: parse_t(r['dep_time']))
            # Avoid duplicate if direct has exact same dep_time & via
            if not any(d['dep_time'] == best_transfer['dep_time'] and d['via'] == best_transfer['via'] for d in directs):
                final_list.append(best_transfer)
                
    # Sort
    final_list.sort(key=lambda r: (parse_t(r['dep_time']), parse_t(r['arr_time']), 0 if r['is_direct'] else 1))
    
    # Deduplicate exact (dep_time, arr_time, via)
    deduped = []
    seen = set()
    for idx, r in enumerate(final_list, 1):
        k = (r['dep_time'], r['arr_time'], r['via'])
        if k not in seen:
            seen.add(k)
            r['no'] = len(deduped) + 1
            deduped.append(r)
            
    print(f"Processed {day_type}: {len(deduped)} trains")
    return deduped

weekday_final = process_routes('weekday_routes.json', '平日ダイヤ')
weekend_final = process_routes('weekend_routes.json', '土休日ダイヤ')

with open('final_timetable_data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'weekday': weekday_final,
        'weekend': weekend_final
    }, f, ensure_ascii=False, indent=2)

print("Saved to final_timetable_data.json")
