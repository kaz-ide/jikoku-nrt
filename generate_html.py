import os
import json

BASE_DIR = r"C:\Users\HINOTORI\.gemini\antigravity\scratch\jikoku_nrt"
data_path = os.path.join(BASE_DIR, "merged_timetable_data.json")

with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Format liner names in the dataset: ensure '特急 ' is removed and 'スカイライナーX号' is clean
for day in ['weekday', 'weekend']:
    for item in data[day]:
        if item.get('is_liner'):
            raw_name = item.get('liner_name', '')
            clean_name = raw_name.replace('特急', '').strip()
            if not clean_name:
                clean_name = item.get('train_type', 'スカイライナー')
            item['liner_name_clean'] = clean_name

weekday_json = json.dumps(data['weekday'], ensure_ascii=False)
weekend_json = json.dumps(data['weekend'], ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>京成上野駅 ➔ 成田空港 時刻表（スカイライナー＆一般特急・快速）</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* 京成スカイライナー (AE形) カラーパレット
       ウインドブルー (Wind Blue): #001e44, #0a1c38
       ストリームホワイト (Stream White): #ffffff, #f1f5fa
       シルバーアクセント: #cbd5e1, #94a3b8
       京成レッド: #e60012
       スカイアクセスオレンジ: #f39700
    */
    :root {{
      --bg-page: #f1f5fa;
      --bg-card: #ffffff;
      --border-color: #cbd7e6;
      --text-main: #061224;
      --text-muted: #526782;
      --ae-windblue: #001e44;
      --ae-windblue-hover: #0a2955;
      --ae-windblue-light: #0d3266;
      --keisei-blue: #004098;
      --accent-color: #eaf1f8;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg-page: #060d19;
        --bg-card: #0b1526;
        --border-color: #172a45;
        --text-main: #f0f4fa;
        --text-muted: #8fa6c5;
        --ae-windblue: #001e44;
        --ae-windblue-hover: #0d2a54;
        --ae-windblue-light: #16427d;
        --keisei-blue: #297be6;
        --accent-color: #111f36;
      }}
    }}

    body {{
      background-color: var(--bg-page);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Meiryo", sans-serif;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
      user-select: none;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-thumb {{
      background: rgba(0, 30, 68, 0.28);
      border-radius: 4px;
    }}
    .no-scrollbar::-webkit-scrollbar {{
      display: none;
    }}
    .no-scrollbar {{
      -ms-overflow-style: none;
      scrollbar-width: none;
    }}

    /* Active Time Band Tab */
    .tab-active {{
      background-color: #001e44 !important;
      color: #ffffff !important;
      font-weight: 700;
      box-shadow: 0 2px 5px rgba(0, 30, 68, 0.35);
    }}
    @media (prefers-color-scheme: dark) {{
      .tab-active {{
        background-color: #1a4580 !important;
      }}
    }}

    /* Day Tab Active */
    .day-tab-active {{
      background-color: #ffffff !important;
      color: #001e44 !important;
      font-weight: 800;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }}
    @media (prefers-color-scheme: dark) {{
      .day-tab-active {{
        background-color: #184178 !important;
        color: #ffffff !important;
      }}
    }}

    /* Filter button active */
    .filter-btn-active {{
      background-color: #001e44 !important;
      color: #ffffff !important;
      border-color: #001e44 !important;
      font-weight: 700;
    }}
    @media (prefers-color-scheme: dark) {{
      .filter-btn-active {{
        background-color: #1a4580 !important;
        border-color: #1a4580 !important;
      }}
    }}

    /* AE形 車両ストライプ装飾 */
    .ae-stripe {{
      background: linear-gradient(90deg, #001e44 0%, #0d366e 65%, #1a4b91 85%, #e60012 85%, #e60012 100%);
    }}
  </style>
</head>
<body class="antialiased p-1.5 sm:p-4 md:p-6 lg:p-8 min-h-screen flex flex-col justify-start items-center">
  
  <!-- Responsive container: max-w-lg on mobile, max-w-2xl on tablet, max-w-4xl on desktop -->
  <div class="w-full max-w-lg md:max-w-2xl lg:max-w-4xl mx-auto bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl md:rounded-3xl shadow-2xl overflow-hidden flex flex-col transition-all duration-200">

    <!-- スカイライナーAE形 ウインドブルー＆レッドのツインストライプ -->
    <div class="h-2 md:h-2.5 w-full ae-stripe"></div>

    <!-- Header Section (AE形ウインドブルー基調デザイン) -->
    <header class="px-3.5 py-3 md:px-6 md:py-4 bg-[#001e44] text-white shadow-md">
      <div class="flex items-center justify-between">
        <div>
          <div class="flex items-center gap-1.5 md:gap-2.5 flex-wrap">
            <span class="inline-block w-2.5 h-2.5 md:w-3 md:h-3 rounded-full bg-cyan-400 animate-pulse"></span>
            <h1 class="text-base sm:text-lg md:text-xl lg:text-2xl font-extrabold tracking-tight text-white drop-shadow-sm">京成上野 ➔ 成田空港</h1>
            <span class="text-[10px] md:text-xs px-1.5 md:px-2 py-0.5 rounded font-bold bg-white/15 text-cyan-200 border border-cyan-400/30 backdrop-blur-xs">全便対応</span>
          </div>
          <p class="text-[11px] md:text-xs lg:text-sm text-slate-300 mt-0.5 md:mt-1">
            成田スカイアクセス線 ＆ 京成本線 <span class="font-bold text-cyan-300">スカイライナー</span> ＆ 一般特急・快速
          </p>
        </div>

        <!-- Train Type Filter Toggle (全列車 / 一般のみ / ライナー) -->
        <button id="linerToggle" onclick="cycleLinerFilter()" class="flex items-center gap-1 md:gap-1.5 px-2.5 py-1.5 md:px-3.5 md:py-2 rounded-xl border border-white/30 bg-white/10 hover:bg-white/20 transition text-xs md:text-sm font-semibold text-white shadow-xs">
          <span id="linerToggleIcon">⚡</span>
          <span id="linerToggleLabel">全列車</span>
        </button>
      </div>

      <!-- Quick Route Note -->
      <div class="mt-2.5 md:mt-3 pt-2 md:pt-2.5 border-t border-white/15 flex flex-wrap gap-x-2.5 md:gap-x-4 gap-y-1 text-[10px] md:text-xs text-slate-300 items-center">
        <span class="font-bold text-cyan-300">✈️ スカイライナー 最速41分</span>
        <span class="font-medium text-emerald-300">🚃 アクセス特急 最速60分</span>
        <span class="font-medium text-blue-300">🚃 本線特急 約75分</span>
      </div>

      <!-- Schedule Type (Weekday / Weekend) Toggle Switch & Via Filter -->
      <div class="mt-2.5 md:mt-3 pt-2 md:pt-2.5 border-t border-white/15 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2 md:gap-3">
        <!-- Day Tab -->
        <div class="flex items-center gap-1 md:gap-1.5 bg-black/35 p-1 md:p-1.5 rounded-xl text-xs md:text-sm flex-1">
          <button id="btnWeekday" onclick="setDayType('weekday')" class="day-tab flex-1 py-1.5 md:py-2 px-2 md:px-3 rounded-lg text-center transition font-semibold text-xs md:text-sm text-slate-200">
            🏢 平日ダイヤ
          </button>
          <button id="btnWeekend" onclick="setDayType('weekend')" class="day-tab flex-1 py-1.5 md:py-2 px-2 md:px-3 rounded-lg text-center transition font-semibold text-xs md:text-sm text-slate-200">
            🏖️ 土休日ダイヤ
          </button>
        </div>

        <!-- Via Line Filter Pill -->
        <div class="flex items-center gap-1 md:gap-1.5 text-[11px] md:text-xs self-end sm:self-auto">
          <button id="filterViaAll" onclick="setViaFilter('all')" class="filter-via-btn px-2.5 md:px-3 py-1.5 md:py-2 rounded-lg border border-white/30 bg-white text-[#001e44] transition text-[10px] md:text-xs font-bold filter-btn-active">
            全経由
          </button>
          <button id="filterViaSky" onclick="setViaFilter('sky')" class="filter-via-btn px-2.5 md:px-3 py-1.5 md:py-2 rounded-lg border border-white/30 bg-black/25 text-orange-200 transition text-[10px] md:text-xs font-medium hover:bg-white/10">
            ✈️アクセス
          </button>
          <button id="filterViaMain" onclick="setViaFilter('main')" class="filter-via-btn px-2.5 md:px-3 py-1.5 md:py-2 rounded-lg border border-white/30 bg-black/25 text-blue-200 transition text-[10px] md:text-xs font-medium hover:bg-white/10">
            🚃本線
          </button>
        </div>
      </div>
    </header>

    <!-- Time Band Tabs (Responsive) -->
    <nav class="p-1.5 md:p-2.5 bg-[var(--accent-color)] border-b border-[var(--border-color)] flex items-center gap-1 md:gap-1.5 overflow-x-auto no-scrollbar text-xs md:text-sm">
      <button class="tab-btn flex-1 min-w-[54px] md:min-w-[70px] py-1.5 md:py-2.5 px-1 md:px-2 rounded-lg text-center transition font-medium text-[11px] md:text-xs lg:text-sm text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="now" onclick="changeBand('now')">
        ⏱️ 次の便
      </button>
      <button class="tab-btn flex-1 min-w-[54px] md:min-w-[70px] py-1.5 md:py-2.5 px-1 md:px-2 rounded-lg text-center transition font-medium text-[11px] md:text-xs lg:text-sm text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="morning" onclick="changeBand('morning')">
        🌅 朝 <span class="opacity-75 text-[9px] md:text-[10px] lg:text-[11px] block sm:inline">5-9時</span>
      </button>
      <button class="tab-btn flex-1 min-w-[54px] md:min-w-[70px] py-1.5 md:py-2.5 px-1 md:px-2 rounded-lg text-center transition font-medium text-[11px] md:text-xs lg:text-sm text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="day" onclick="changeBand('day')">
        ☀️ 昼 <span class="opacity-75 text-[9px] md:text-[10px] lg:text-[11px] block sm:inline">10-15時</span>
      </button>
      <button class="tab-btn flex-1 min-w-[54px] md:min-w-[70px] py-1.5 md:py-2.5 px-1 md:px-2 rounded-lg text-center transition font-medium text-[11px] md:text-xs lg:text-sm text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="evening" onclick="changeBand('evening')">
        🌇 夕 <span class="opacity-75 text-[9px] md:text-[10px] lg:text-[11px] block sm:inline">16-19時</span>
      </button>
      <button class="tab-btn flex-1 min-w-[54px] md:min-w-[70px] py-1.5 md:py-2.5 px-1 md:px-2 rounded-lg text-center transition font-medium text-[11px] md:text-xs lg:text-sm text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="night" onclick="changeBand('night')">
        🌙 夜 <span class="opacity-75 text-[9px] md:text-[10px] lg:text-[11px] block sm:inline">20-23時</span>
      </button>
      <button class="tab-btn py-1.5 md:py-2.5 px-2 md:px-3 rounded-lg text-center transition font-medium text-[11px] md:text-xs lg:text-sm text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="all" onclick="changeBand('all')">
        全便
      </button>
    </nav>

    <!-- Table Sticky Column Headers -->
    <div class="grid grid-cols-12 px-3 md:px-5 py-2 md:py-3 text-[11px] md:text-xs lg:text-sm font-extrabold text-[var(--text-muted)] bg-[var(--bg-card)] border-b border-[var(--border-color)] items-center shadow-xs">
      <div class="col-span-2 text-center text-[#001e44] dark:text-cyan-300">上野発</div>
      <div class="col-span-3 text-center">種別 / 列車名</div>
      <div class="col-span-2 text-center">乗換</div>
      <div class="col-span-3 text-center tracking-tight">
        <span class="text-emerald-700 dark:text-emerald-400">第2ビル</span> <span class="text-[var(--text-muted)] font-normal">/</span> <span class="text-blue-700 dark:text-blue-400">成田空港</span>
      </div>
      <div class="col-span-2 text-right">所要</div>
    </div>

    <!-- Main List Container: Responsive max-height -->
    <main id="timetableContainer" class="divide-y divide-[var(--border-color)] overflow-y-auto max-h-[58vh] md:max-h-[64vh] lg:max-h-[68vh] text-xs md:text-sm">
      <!-- Injected by JavaScript -->
    </main>

    <!-- Footer Notice -->
    <footer class="px-3.5 md:px-6 py-2.5 md:py-3.5 bg-[var(--accent-color)] border-t border-[var(--border-color)] flex items-center justify-between text-[11px] md:text-xs lg:text-sm text-[var(--text-muted)]">
      <div class="flex items-center gap-1.5 md:gap-2">
        <span class="inline-block w-2 h-2 md:w-2.5 md:h-2.5 rounded-full bg-[#001e44] dark:bg-cyan-400"></span>
        <span>行タップで詳細(車両・乗換・運賃内訳)</span>
      </div>
      <span id="listCountLabel" class="font-mono font-bold text-[var(--text-main)]">--便</span>
    </footer>

  </div>

  <script>
    // 判定処理 (オリジナルを引き継ぎ)
    (function() {{
      const host = location.hostname;
      const path = decodeURIComponent(location.pathname);
      const isAllowedWeb = ["kaz-ide.github.io"].includes(host);
      const isAllowedLocal = location.protocol === "file:" && (
        path.includes("/SAKURA/.gemini/antigravity/") ||
        path.includes("/HINOTORI/.gemini/antigravity/")
      );
      if (!isAllowedWeb && !isAllowedLocal) {{
        document.body.innerHTML = "";
        throw new Error();
      }}
    }})();

    const TIMETABLE_DATA = {{
      weekday: {weekday_json},
      weekend: {weekend_json}
    }};

    // State
    let currentDayType = detectInitialDayType();
    let activeBand = detectInitialBand();
    let linerFilter = 'all'; // 'all' (全列車) | 'general' (一般のみ) | 'liner' (スカイライナーのみ)
    let viaFilter = 'all'; // 'all' | 'sky' | 'main'
    let selectedTrainNo = null;

    function detectInitialDayType() {{
      const d = new Date().getDay();
      return (d === 0 || d === 6) ? 'weekend' : 'weekday';
    }}

    function detectInitialBand() {{
      const h = new Date().getHours();
      if (h >= 5 && h < 10) return 'morning';
      if (h >= 10 && h < 16) return 'day';
      if (h >= 16 && h < 20) return 'evening';
      if (h >= 20 && h < 24) return 'night';
      return 'now';
    }}

    function setDayType(dayType) {{
      currentDayType = dayType;
      selectedTrainNo = null;
      render();
    }}

    function changeBand(band) {{
      activeBand = band;
      selectedTrainNo = null;
      render();
    }}

    function cycleLinerFilter() {{
      // 'all' -> 'general' -> 'liner' -> 'all'
      if (linerFilter === 'all') {{
        linerFilter = 'general';
      }} else if (linerFilter === 'general') {{
        linerFilter = 'liner';
      }} else {{
        linerFilter = 'all';
      }}
      selectedTrainNo = null;
      updateLinerToggleButton();
      render();
    }}

    function updateLinerToggleButton() {{
      const btn = document.getElementById('linerToggle');
      const label = document.getElementById('linerToggleLabel');
      const icon = document.getElementById('linerToggleIcon');
      if (linerFilter === 'general') {{
        btn.className = 'flex items-center gap-1 md:gap-1.5 px-2.5 py-1.5 md:px-3.5 md:py-2 rounded-xl border border-emerald-400 bg-emerald-700/80 hover:bg-emerald-700 transition text-xs md:text-sm font-bold text-white shadow-xs';
        label.innerText = '一般のみ';
        icon.innerText = '🚃';
      }} else if (linerFilter === 'liner') {{
        btn.className = 'flex items-center gap-1 md:gap-1.5 px-2.5 py-1.5 md:px-3.5 md:py-2 rounded-xl border border-cyan-400 bg-cyan-700/80 hover:bg-cyan-700 transition text-xs md:text-sm font-bold text-white shadow-xs';
        label.innerText = 'ライナー';
        icon.innerText = '✈️';
      }} else {{
        btn.className = 'flex items-center gap-1 md:gap-1.5 px-2.5 py-1.5 md:px-3.5 md:py-2 rounded-xl border border-white/30 bg-white/10 hover:bg-white/20 transition text-xs md:text-sm font-semibold text-white shadow-xs';
        label.innerText = '全列車';
        icon.innerText = '⚡';
      }}
    }}

    function setViaFilter(via) {{
      viaFilter = via;
      selectedTrainNo = null;
      render();
    }}

    function toggleRow(no) {{
      selectedTrainNo = (selectedTrainNo === no) ? null : no;
      render();
    }}

    function getNowMinutes() {{
      const now = new Date();
      return now.getHours() * 60 + now.getMinutes();
    }}

    function parseMin(timeStr) {{
      const [h, m] = timeStr.split(':').map(Number);
      return (h < 4 ? h + 24 : h) * 60 + m;
    }}

    function getTrainBadgeClass(type) {{
      switch(type) {{
        case 'スカイライナー':
          return 'bg-[#001e44] text-cyan-200 border border-cyan-400/80 shadow-xs';
        case 'アクセス特急':
          return 'bg-[#f39700] text-white border border-[#d68400]';
        case '快速特急':
          return 'bg-[#00965e] text-white border border-[#007a4c]';
        case '特急':
          return 'bg-[#e60012] text-white border border-[#c2000f]';
        case '通勤特急':
          return 'bg-[#0099d9] text-white border border-[#007fb4]';
        case '快速':
          return 'bg-[#e4007f] text-white border border-[#bf006a]';
        case '普通':
        default:
          return 'bg-[#004098] text-white border border-[#002d6b]';
      }}
    }}

    function render() {{
      // Update Day Type Tabs
      const btnW = document.getElementById('btnWeekday');
      const btnH = document.getElementById('btnWeekend');
      if (currentDayType === 'weekday') {{
        btnW.className = 'day-tab flex-1 py-1.5 md:py-2 px-2 md:px-3 rounded-lg text-center transition font-black text-xs md:text-sm day-tab-active';
        btnH.className = 'day-tab flex-1 py-1.5 md:py-2 px-2 md:px-3 rounded-lg text-center transition font-semibold text-xs md:text-sm text-slate-200 hover:text-white';
      }} else {{
        btnH.className = 'day-tab flex-1 py-1.5 md:py-2 px-2 md:px-3 rounded-lg text-center transition font-black text-xs md:text-sm day-tab-active';
        btnW.className = 'day-tab flex-1 py-1.5 md:py-2 px-2 md:px-3 rounded-lg text-center transition font-semibold text-xs md:text-sm text-slate-200 hover:text-white';
      }}

      // Update Via Buttons
      ['all', 'sky', 'main'].forEach(v => {{
        const btn = document.getElementById('filterVia' + v.charAt(0).toUpperCase() + v.slice(1));
        if (viaFilter === v) {{
          btn.className = 'filter-via-btn px-2.5 md:px-3 py-1.5 md:py-2 rounded-lg border border-white bg-white text-[#001e44] transition text-[10px] md:text-xs font-black shadow-xs';
        }} else {{
          let colorClass = 'text-slate-200';
          if (v === 'sky') colorClass = 'text-orange-200';
          if (v === 'main') colorClass = 'text-blue-200';
          btn.className = `filter-via-btn px-2.5 md:px-3 py-1.5 md:py-2 rounded-lg border border-white/30 bg-black/25 ${{colorClass}} transition text-[10px] md:text-xs font-medium hover:bg-white/10`;
        }}
      }});

      // Update Band Tabs
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        if (btn.dataset.band === activeBand) {{
          btn.className = 'tab-btn tab-active flex-1 min-w-[54px] md:min-w-[70px] py-1.5 md:py-2.5 px-1 md:px-2 rounded-lg text-center transition font-bold text-[11px] md:text-xs lg:text-sm';
        }} else {{
          btn.className = 'tab-btn flex-1 min-w-[54px] md:min-w-[70px] py-1.5 md:py-2.5 px-1 md:px-2 rounded-lg text-center transition font-medium text-[11px] md:text-xs lg:text-sm text-[var(--text-muted)] hover:bg-[var(--bg-card)]';
        }}
      }});

      // Get current items
      let items = TIMETABLE_DATA[currentDayType] || [];

      // Filter by Liner
      if (linerFilter === 'general') {{
        items = items.filter(t => !t.is_liner);
      }} else if (linerFilter === 'liner') {{
        items = items.filter(t => t.is_liner);
      }}

      // Filter by Via
      if (viaFilter === 'sky') {{
        items = items.filter(t => t.via.includes('スカイアクセス'));
      }} else if (viaFilter === 'main') {{
        items = items.filter(t => t.via.includes('京成本線'));
      }}

      // Filter by Band
      const nowMin = getNowMinutes();
      if (activeBand === 'now') {{
        const afterNow = items.filter(t => parseMin(t.dep_time) >= nowMin);
        items = afterNow.length >= 6 ? afterNow.slice(0, 8) : items.slice(0, 8);
      }} else if (activeBand !== 'all') {{
        items = items.filter(t => t.time_band === activeBand);
      }}

      document.getElementById('listCountLabel').innerText = `${{items.length}}便 表示中`;

      const container = document.getElementById('timetableContainer');
      if (items.length === 0) {{
        container.innerHTML = `
          <div class="py-12 md:py-16 px-4 text-center text-[var(--text-muted)]">
            <p class="text-sm md:text-base font-bold">条件に合う列車がありません</p>
            <p class="text-xs md:text-sm mt-1">フィルターを「全列車」にするか、経由や時間帯を変更してください。</p>
          </div>
        `;
        return;
      }}

      container.innerHTML = items.map(train => {{
        const isSelected = (selectedTrainNo === train.no);
        const badgeClass = getTrainBadgeClass(train.train_type);
        const isSky = train.via.includes('スカイアクセス');
        const isLiner = !!train.is_liner;
        
        // 列車種別・列車名表示: スカイライナーの場合は「スカイライナーXX号」と表記
        let displayBadgeText = train.train_type;
        if (isLiner) {{
          displayBadgeText = train.liner_name_clean || train.liner_name || 'スカイライナー';
        }}

        // 経由バッジ: スカイライナーの場合は「AE特急」は表示せず不要（アクセス特急との混同防止）
        let viaBadgeHtml = '';
        if (!isLiner) {{
          viaBadgeHtml = isSky 
            ? `<div class="mt-0.5"><span class="inline-block px-1 md:px-2 py-0.2 md:py-0.5 rounded text-[9px] md:text-[11px] lg:text-[12px] font-black bg-orange-100 text-orange-800 dark:bg-orange-950/80 dark:text-orange-300 border border-orange-300 dark:border-orange-800 leading-none">SA線</span></div>`
            : `<div class="mt-0.5"><span class="inline-block px-1 md:px-2 py-0.2 md:py-0.5 rounded text-[9px] md:text-[11px] lg:text-[12px] font-black bg-blue-100 text-blue-800 dark:bg-blue-950/80 dark:text-blue-300 border border-blue-200 dark:border-blue-800 leading-none">本線</span></div>`;
        }}

        const transferBadge = isLiner
          ? `<span class="inline-flex items-center px-1.5 md:px-2.5 py-0.5 md:py-1 rounded text-[10.5px] md:text-xs lg:text-sm font-black text-cyan-700 dark:text-cyan-300 bg-cyan-50 dark:bg-cyan-950/50 border border-cyan-300 dark:border-cyan-700 leading-tight">全席指定</span>`
          : (train.is_direct
              ? `<span class="inline-flex items-center px-1.5 md:px-2.5 py-0.5 md:py-1 rounded text-[10.5px] md:text-xs lg:text-sm font-bold text-emerald-700 bg-emerald-50 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-700 leading-tight">直通</span>`
              : `<span class="inline-flex items-center px-1 md:px-2 py-0.5 md:py-1 rounded text-[10px] md:text-[11.5px] lg:text-xs font-bold text-amber-700 bg-amber-50 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-300 dark:border-amber-700 leading-tight">${{train.transfer_station}}乗換</span>`);

        const rowBg = isLiner 
          ? (isSelected ? 'bg-cyan-500/15' : 'bg-cyan-500/5 hover:bg-cyan-500/10')
          : (isSelected ? 'bg-[var(--accent-color)]' : 'hover:bg-[var(--accent-color)]/60');

        return `
          <div class="transition-colors ${{rowBg}}">
            <div onclick="toggleRow(${{train.no}})" class="grid grid-cols-12 px-2.5 sm:px-3 md:px-5 py-2 md:py-3.5 lg:py-4 items-center cursor-pointer">
              
              <!-- 上野発 -->
              <div class="col-span-2 text-center">
                <span class="text-[15.5px] sm:text-[17px] md:text-[20px] lg:text-[23px] font-black font-mono tracking-tighter ${{isLiner ? 'text-[#001e44] dark:text-cyan-300 font-extrabold' : 'text-[#004098] dark:text-[#38bdf8]'}} leading-none">${{train.dep_time}}</span>
              </div>

              <!-- 種別 / 列車名 (スカイライナーXX号) -->
              <div class="col-span-3 flex flex-col items-center justify-center leading-none">
                <span class="px-1.5 md:px-2.5 py-0.5 md:py-1 rounded text-[9.5px] sm:text-[10.5px] md:text-xs lg:text-[13px] font-extrabold shadow-2xs ${{badgeClass}} text-center leading-none tracking-tighter whitespace-nowrap">
                  ${{displayBadgeText}}
                </span>
                ${{viaBadgeHtml}}
              </div>

              <!-- 乗換 / 指定 -->
              <div class="col-span-2 text-center leading-none">
                ${{transferBadge}}
              </div>

              <!-- 空港着: 1行表示 「hh:mm / hh:mm」 (色分け維持: 第2ビル緑 / 第1空港青) -->
              <div class="col-span-3 text-center whitespace-nowrap">
                <span class="font-mono font-black text-emerald-600 dark:text-emerald-400 text-[12px] sm:text-[13.5px] md:text-[16px] lg:text-[18px] tracking-tight">${{train.t2_arr_time}}</span>
                <span class="text-[var(--text-muted)] mx-0.5 md:mx-1 font-semibold text-[11px] sm:text-[12px] md:text-[14px]">/</span>
                <span class="font-mono font-black text-[#004098] dark:text-[#38bdf8] text-[12px] sm:text-[13.5px] md:text-[16px] lg:text-[18px] tracking-tight">${{train.arr_time}}</span>
              </div>

              <!-- 所要時間 -->
              <div class="col-span-2 text-right leading-none pr-0.5 md:pr-2">
                <span class="text-[14.5px] sm:text-[16px] md:text-[19px] lg:text-[22px] font-black font-mono text-[var(--text-main)]">${{train.total_min}}</span><span class="text-[10.5px] md:text-xs lg:text-sm font-bold text-[var(--text-muted)] ml-0.5">分</span>
              </div>
            </div>

            <!-- Detail Accordion -->
            ${{isSelected ? `
              <div class="px-4 md:px-6 py-3.5 md:py-5 bg-[var(--bg-card)] border-t border-[var(--border-color)] text-xs md:text-sm space-y-2.5 md:space-y-4 animate-fadeIn">
                <div class="flex items-center justify-between pb-1.5 md:pb-2 border-b border-[var(--border-color)]/70">
                  <div class="flex items-center gap-2">
                    <span class="font-extrabold text-xs md:text-sm text-[#001e44] dark:text-cyan-300">#${{train.no}}</span>
                    <span class="font-bold text-xs md:text-sm text-[var(--text-main)]">${{isLiner ? train.liner_name_clean : train.via}}</span>
                  </div>
                  <span class="text-[11px] md:text-xs lg:text-sm font-mono font-bold text-emerald-600 dark:text-emerald-400">成田空港(第1)まで ${{train.total_min}}分</span>
                </div>

                <!-- 運行ルートと乗換詳細 -->
                <div class="bg-[var(--accent-color)] p-2.5 md:p-3.5 rounded-xl border border-[var(--border-color)] space-y-1.5 md:space-y-2 text-[11px] md:text-xs lg:text-sm">
                  <div class="flex items-start gap-2">
                    <span class="text-[#001e44] dark:text-cyan-400 font-bold shrink-0">${{isLiner ? '⚡ 列車案内:' : '🛫 運行概要:'}}</span>
                    <span class="font-medium text-[var(--text-main)]">${{train.transfer_desc}}</span>
                  </div>
                  <div class="flex items-start gap-2 text-[10px] md:text-xs text-[var(--text-muted)] pt-1 border-t border-[var(--border-color)]/50">
                    <span class="font-bold text-[var(--text-main)]">利用路線:</span>
                    <span>${{train.transports.join(' ➔ ')}}</span>
                  </div>
                </div>

                <!-- ターミナル別到着時刻案内 -->
                <div class="grid grid-cols-2 gap-2 md:gap-4 text-center">
                  <div class="p-2.5 md:p-3.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 shadow-xs">
                    <span class="text-[10px] md:text-xs font-semibold text-emerald-800 dark:text-emerald-300 block">第2・第3ターミナル</span>
                    <div class="text-xs md:text-sm lg:text-base font-black text-emerald-700 dark:text-emerald-300 mt-0.5 md:mt-1">
                      空港第２ビル <span class="font-mono text-sm md:text-base lg:text-lg">${{train.t2_arr_time}}</span>着
                    </div>
                  </div>
                  <div class="p-2.5 md:p-3.5 rounded-xl bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800/60 shadow-xs">
                    <span class="text-[10px] md:text-xs font-semibold text-blue-800 dark:text-blue-300 block">第1ターミナル</span>
                    <div class="text-xs md:text-sm lg:text-base font-black text-[#004098] dark:text-[#38bdf8] mt-0.5 md:mt-1">
                      成田空港 <span class="font-mono text-sm md:text-base lg:text-lg">${{train.arr_time}}</span>着
                    </div>
                  </div>
                </div>

                <!-- 運賃・ライナー券案内 -->
                <div class="flex items-center justify-between text-[11px] md:text-xs lg:text-sm pt-1 px-1 text-[var(--text-muted)]">
                  <div class="flex items-center gap-1.5 md:gap-2">
                    <span class="px-2 py-0.5 md:py-1 rounded text-[10px] md:text-xs bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold border border-slate-200 dark:border-slate-700">
                      ${{isLiner ? `合計 ${{train.fare_ic}}円 (運賃1,272円＋ライナー券1,300円)` : `IC運賃 ${{train.fare_ic}}円 (きっぷ ${{train.fare_ticket}}円)`}}
                    </span>
                  </div>
                  <span class="text-[10px] md:text-xs lg:text-sm font-bold ${{isLiner ? 'text-cyan-600 dark:text-cyan-400' : 'text-emerald-600 dark:text-emerald-400'}}">
                    ${{isLiner ? 'ライナー券(全席指定) 必要' : '特急料金不要 (乗車券のみ)'}}
                  </span>
                </div>
              </div>
            ` : ''}}
          </div>
        `;
      }}).join('');
    }}

    // Initial render
    render();
  </script>
</body>
</html>
'''

# Write to HINOTORI directory
hinotori_dir = r"C:\Users\HINOTORI\.gemini\antigravity\scratch\jikoku_nrt"
index_path_h = os.path.join(hinotori_dir, "index.html")
index_org_path_h = os.path.join(hinotori_dir, "index_org.html")

with open(index_path_h, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(index_org_path_h, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated HINOTORI:\n  {index_path_h}\n  {index_org_path_h}")

# Also sync to SAKURA if directory exists
sakura_dir = r"C:\Users\SAKURA\.gemini\antigravity\scratch\jikoku_nrt"
if os.path.exists(sakura_dir):
    with open(os.path.join(sakura_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(html_content)
    with open(os.path.join(sakura_dir, "index_org.html"), 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Synced SAKURA directory")
