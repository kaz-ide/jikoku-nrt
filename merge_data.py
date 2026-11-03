import json
import os

BASE_DIR = r"C:\Users\HINOTORI\.gemini\antigravity\scratch\jikoku_nrt"

# Load general trains
with open(os.path.join(BASE_DIR, "final_timetable_data.json"), "r", encoding="utf-8") as f:
    general_data = json.load(f)

# Load skyliners
with open(os.path.join(BASE_DIR, "skyliners.json"), "r", encoding="utf-8") as f:
    skyliners_data = json.load(f)

def parse_t(t_str):
    h, m = map(int, t_str.split(':'))
    return (h + 24 if h < 4 else h) * 60 + m

def merge_and_sort(general_list, skyliner_list):
    combined = []
    # add general (mark is_skyliner: false)
    for g in general_list:
        g_copy = dict(g)
        g_copy['is_skyliner'] = False
        combined.append(g_copy)
        
    # add skyliners
    for s in skyliner_list:
        combined.append(dict(s))
        
    # sort by dep_time, then arr_time
    combined.sort(key=lambda x: (parse_t(x['dep_time']), parse_t(x['arr_time']), 0 if x['is_skyliner'] else 1))
    
    # re-number
    for idx, item in enumerate(combined, 1):
        item['no'] = idx
        
    return combined

merged_weekday = merge_and_sort(general_data['weekday'], skyliners_data['weekday'])
merged_weekend = merge_and_sort(general_data['weekend'], skyliners_data['weekend'])

print(f"Merged Weekday: {len(merged_weekday)} trains (General: {len(general_data['weekday'])}, Skyliner: {len(skyliners_data['weekday'])})")
print(f"Merged Weekend: {len(merged_weekend)} trains (General: {len(general_data['weekend'])}, Skyliner: {len(skyliners_data['weekend'])})")

# Save merged data
with open(os.path.join(BASE_DIR, "all_trains_data.json"), "w", encoding="utf-8") as f:
    json.dump({
        'weekday': merged_weekday,
        'weekend': merged_weekend
    }, f, ensure_ascii=False, indent=2)

print("Saved all_trains_data.json successfully!")
