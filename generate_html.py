import os
import json

BASE_DIR = r"C:\Users\SAKURA\.gemini\antigravity\scratch\jikoku_nrt"
data_path = os.path.join(BASE_DIR, "final_timetable_data.json")

with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

weekday_json = json.dumps(data['weekday'], ensure_ascii=False)
weekend_json = json.dumps(data['weekend'], ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>京成上野駅 ➔ 成田空港 時刻表（在来線・一般列車限定）</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* 京成電鉄 公式カラーパレット
       京成ブルー: #004098
       京成レッド: #e60012
       スカイアクセスオレンジ: #f39700
    */
    :root {{
      --bg-page: #eaf1f8;
      --bg-card: #ffffff;
      --border-color: #cbdbe9;
      --text-main: #0c1a2e;
      --text-muted: #536b88;
      --keisei-blue: #004098;
      --keisei-blue-hover: #003074;
      --keisei-red: #e60012;
      --accent-color: #edf4fa;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg-page: #070d18;
        --bg-card: #0f1a2c;
        --border-color: #1e3352;
        --text-main: #f0f5fc;
        --text-muted: #94abcb;
        --keisei-blue: #165ec7;
        --keisei-blue-hover: #2670dd;
        --keisei-red: #f83244;
        --accent-color: #16243a;
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
      width: 4px;
      height: 4px;
    }}
    ::-webkit-scrollbar-thumb {{
      background: rgba(0, 64, 152, 0.25);
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
      background-color: var(--keisei-blue) !important;
      color: #ffffff !important;
      font-weight: 700;
      box-shadow: 0 2px 4px rgba(0, 64, 152, 0.3);
    }}

    /* Day Tab Active */
    .day-tab-active {{
      background-color: #ffffff !important;
      color: #004098 !important;
      font-weight: 800;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
    }}
    @media (prefers-color-scheme: dark) {{
      .day-tab-active {{
        background-color: #165ec7 !important;
        color: #ffffff !important;
      }}
    }}

    /* Filter button active */
    .filter-btn-active {{
      background-color: var(--keisei-blue) !important;
      color: #ffffff !important;
      border-color: var(--keisei-blue) !important;
      font-weight: 700;
    }}
  </style>
</head>
<body class="antialiased p-1.5 sm:p-4 min-h-screen flex flex-col justify-start">
  
  <div class="w-full max-w-lg mx-auto bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl shadow-2xl overflow-hidden flex flex-col">

    <!-- 京成レッドのブランドアクセントバー -->
    <div class="h-1.5 w-full bg-[#e60012]"></div>

    <!-- Header Section (京成ブルー調の駅名標風デザイン) -->
    <header class="px-3.5 py-3 bg-[#004098] text-white shadow-md">
      <div class="flex items-center justify-between">
        <div>
          <div class="flex items-center gap-1.5 flex-wrap">
            <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <h1 class="text-base font-extrabold tracking-tight text-white drop-shadow-sm">京成上野 ➔ 成田空港</h1>
            <span class="text-[10px] px-1.5 py-0.5 rounded font-bold bg-white/20 text-white border border-white/30 backdrop-blur-xs">普通乗車券のみ</span>
          </div>
          <p class="text-[11px] text-blue-100 mt-0.5">
            京成本線 ＆ 成田スカイアクセス線経由 <span class="font-bold text-amber-300">ライナー券不要</span>
          </p>
        </div>

        <!-- Direct Train Toggle Button -->
        <button id="directToggle" onclick="toggleDirectFilter()" class="flex items-center gap-1 px-2.5 py-1.5 rounded-xl border border-white/30 bg-white/10 hover:bg-white/20 transition text-xs font-semibold text-white shadow-xs">
          <span>✨</span>
          <span id="directToggleLabel">直通のみ</span>
        </button>
      </div>

      <!-- Criteria Note & Legend -->
      <div class="mt-2.5 pt-2 border-t border-white/20 flex flex-wrap gap-x-2.5 gap-y-1 text-[10px] text-blue-100 items-center">
        <span class="text-rose-200 font-bold bg-rose-950/40 px-1 py-0.2 rounded border border-rose-400/30">❌ ライナー(有料特急)除外</span>
        <span>❌ 到達不能・途中止まり除外</span>
        <span class="text-emerald-200 font-bold">✅ 最速接続便網羅</span>
      </div>

      <!-- Schedule Type (Weekday / Weekend) Toggle Switch & Via Filter -->
      <div class="mt-2.5 pt-2 border-t border-white/20 flex items-center justify-between gap-2">
        <!-- Day Tab -->
        <div class="flex items-center gap-1 bg-black/25 p-1 rounded-xl text-xs flex-1">
          <button id="btnWeekday" onclick="setDayType('weekday')" class="day-tab flex-1 py-1.5 px-2 rounded-lg text-center transition font-semibold text-xs text-blue-100">
            🏢 平日ダイヤ
          </button>
          <button id="btnWeekend" onclick="setDayType('weekend')" class="day-tab flex-1 py-1.5 px-2 rounded-lg text-center transition font-semibold text-xs text-blue-100">
            🏖️ 土休日ダイヤ
          </button>
        </div>

        <!-- Via Line Filter Pill -->
        <div class="flex items-center gap-1 text-[11px]">
          <button id="filterViaAll" onclick="setViaFilter('all')" class="filter-via-btn px-2 py-1.5 rounded-lg border border-white/30 bg-white text-[#004098] transition text-[10px] font-bold filter-btn-active">
            全経由
          </button>
          <button id="filterViaSky" onclick="setViaFilter('sky')" class="filter-via-btn px-2 py-1.5 rounded-lg border border-white/30 bg-black/20 text-orange-200 transition text-[10px] font-medium hover:bg-white/10">
            ✈️アクセス
          </button>
          <button id="filterViaMain" onclick="setViaFilter('main')" class="filter-via-btn px-2 py-1.5 rounded-lg border border-white/30 bg-black/20 text-blue-100 transition text-[10px] font-medium hover:bg-white/10">
            🚃本線
          </button>
        </div>
      </div>
    </header>

    <!-- Time Band Tabs (Mobile Optimized) -->
    <nav class="p-1.5 bg-[var(--accent-color)] border-b border-[var(--border-color)] flex items-center gap-1 overflow-x-auto no-scrollbar text-xs">
      <button class="tab-btn flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="now" onclick="changeBand('now')">
        ⏱️ 次の便
      </button>
      <button class="tab-btn flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="morning" onclick="changeBand('morning')">
        🌅 朝 <span class="opacity-75 text-[9px] block sm:inline">5-9時</span>
      </button>
      <button class="tab-btn flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="day" onclick="changeBand('day')">
        ☀️ 昼 <span class="opacity-75 text-[9px] block sm:inline">10-15時</span>
      </button>
      <button class="tab-btn flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="evening" onclick="changeBand('evening')">
        🌇 夕 <span class="opacity-75 text-[9px] block sm:inline">16-19時</span>
      </button>
      <button class="tab-btn flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="night" onclick="changeBand('night')">
        🌙 夜 <span class="opacity-75 text-[9px] block sm:inline">20-23時</span>
      </button>
      <button class="tab-btn py-1.5 px-2 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="all" onclick="changeBand('all')">
        全便
      </button>
    </nav>

    <!-- Table Sticky Column Headers -->
    <div class="grid grid-cols-12 px-3 py-2 text-[11px] font-extrabold text-[var(--text-muted)] bg-[var(--bg-card)] border-b border-[var(--border-color)] items-center shadow-xs">
      <div class="col-span-2 text-center text-[#004098] dark:text-[#38bdf8]">上野発</div>
      <div class="col-span-3 text-center">種別 / 経由</div>
      <div class="col-span-2 text-center">乗換</div>
      <div class="col-span-3 text-center">
        <span class="text-emerald-700 dark:text-emerald-400">第2ビル</span> / <span class="text-blue-700 dark:text-blue-400">第1空港</span>
      </div>
      <div class="col-span-2 text-right">所要</div>
    </div>

    <!-- Main List Container -->
    <main id="timetableContainer" class="divide-y divide-[var(--border-color)] overflow-y-auto max-h-[58vh] sm:max-h-[600px] text-xs">
      <!-- Injected by JavaScript -->
    </main>

    <!-- Footer Notice -->
    <footer class="px-3.5 py-2.5 bg-[var(--accent-color)] border-t border-[var(--border-color)] flex items-center justify-between text-[11px] text-[var(--text-muted)]">
      <div class="flex items-center gap-1.5">
        <span class="inline-block w-2 h-2 rounded-full bg-[#004098] dark:bg-[#38bdf8]"></span>
        <span>行タップで詳細(乗換駅・路線・運賃)</span>
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
    let isDirectFilter = false;
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

    function toggleDirectFilter() {{
      isDirectFilter = !isDirectFilter;
      selectedTrainNo = null;
      const btn = document.getElementById('directToggle');
      const label = document.getElementById('directToggleLabel');
      if (isDirectFilter) {{
        btn.classList.add('bg-emerald-600', 'text-white', 'border-emerald-400');
        btn.classList.remove('bg-white/10', 'text-white');
        label.innerText = '直通中';
      }} else {{
        btn.classList.remove('bg-emerald-600', 'text-white', 'border-emerald-400');
        btn.classList.add('bg-white/10', 'text-white');
        label.innerText = '直通のみ';
      }}
      render();
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
        btnW.className = 'day-tab flex-1 py-1.5 px-2 rounded-lg text-center transition font-black text-xs day-tab-active';
        btnH.className = 'day-tab flex-1 py-1.5 px-2 rounded-lg text-center transition font-semibold text-xs text-blue-100 hover:text-white';
      }} else {{
        btnH.className = 'day-tab flex-1 py-1.5 px-2 rounded-lg text-center transition font-black text-xs day-tab-active';
        btnW.className = 'day-tab flex-1 py-1.5 px-2 rounded-lg text-center transition font-semibold text-xs text-blue-100 hover:text-white';
      }}

      // Update Via Buttons
      ['all', 'sky', 'main'].forEach(v => {{
        const btn = document.getElementById('filterVia' + v.charAt(0).toUpperCase() + v.slice(1));
        if (viaFilter === v) {{
          btn.className = 'filter-via-btn px-2 py-1.5 rounded-lg border border-white bg-white text-[#004098] transition text-[10px] font-black shadow-xs';
        }} else {{
          let colorClass = 'text-blue-100';
          if (v === 'sky') colorClass = 'text-orange-200';
          if (v === 'main') colorClass = 'text-blue-100';
          btn.className = `filter-via-btn px-2 py-1.5 rounded-lg border border-white/30 bg-black/20 ${{colorClass}} transition text-[10px] font-medium hover:bg-white/10`;
        }}
      }});

      // Update Band Tabs
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        if (btn.dataset.band === activeBand) {{
          btn.className = 'tab-btn tab-active flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-bold text-[11px]';
        }} else {{
          btn.className = 'tab-btn flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]';
        }}
      }});

      // Get current items
      let items = TIMETABLE_DATA[currentDayType] || [];

      // Filter by Via
      if (viaFilter === 'sky') {{
        items = items.filter(t => t.via.includes('スカイアクセス'));
      }} else if (viaFilter === 'main') {{
        items = items.filter(t => t.via.includes('京成本線'));
      }}

      // Filter by Direct
      if (isDirectFilter) {{
        items = items.filter(t => t.is_direct);
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
          <div class="py-12 px-4 text-center text-[var(--text-muted)]">
            <p class="text-sm font-bold">条件に合う列車がありません</p>
            <p class="text-xs mt-1">「直通のみ」を解除するか、経由や時間帯を変更してください。</p>
          </div>
        `;
        return;
      }}

      container.innerHTML = items.map(train => {{
        const isSelected = (selectedTrainNo === train.no);
        const badgeClass = getTrainBadgeClass(train.train_type);
        const isSky = train.via.includes('スカイアクセス');
        
        const viaBadge = isSky 
          ? `<span class="inline-block px-1 py-0.2 rounded text-[9px] font-black bg-orange-100 text-orange-800 dark:bg-orange-950/80 dark:text-orange-300 border border-orange-300 dark:border-orange-800 leading-none">SA線</span>`
          : `<span class="inline-block px-1 py-0.2 rounded text-[9px] font-black bg-blue-100 text-blue-800 dark:bg-blue-950/80 dark:text-blue-300 border border-blue-200 dark:border-blue-800 leading-none">本線</span>`;

        const transferBadge = train.is_direct
          ? `<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10.5px] font-bold text-emerald-700 bg-emerald-50 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-700 leading-tight">直通</span>`
          : `<span class="inline-flex items-center px-1 py-0.5 rounded text-[10px] font-bold text-amber-700 bg-amber-50 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-300 dark:border-amber-700 leading-tight">${{train.transfer_station}}乗換</span>`;

        return `
          <div class="transition-colors hover:bg-[var(--accent-color)]/60 ${{isSelected ? 'bg-[var(--accent-color)]' : ''}}">
            <div onclick="toggleRow(${{train.no}})" class="grid grid-cols-12 px-2.5 sm:px-3 py-2 items-center cursor-pointer">
              
              <!-- 上野発 (文字拡大: text-[15.5px], font-mono tracking-tighter leading-none) -->
              <div class="col-span-2 text-center">
                <span class="text-[15.5px] sm:text-[16.5px] font-black font-mono tracking-tighter text-[#004098] dark:text-[#38bdf8] leading-none">${{train.dep_time}}</span>
              </div>

              <!-- 種別 / 経由 -->
              <div class="col-span-3 flex flex-col items-center justify-center gap-0.5 leading-none">
                <span class="px-1.5 py-0.5 rounded text-[10px] font-extrabold shadow-2xs ${{badgeClass}} text-center leading-none">
                  ${{train.train_type}}
                </span>
                <div>${{viaBadge}}</div>
              </div>

              <!-- 乗換 -->
              <div class="col-span-2 text-center leading-none">
                ${{transferBadge}}
              </div>

              <!-- 空港着: 第2ビル ＆ 第1空港 両方表示 (文字拡大: text-[12.5px]〜13px, leading-tight) -->
              <div class="col-span-3 text-center">
                <div class="flex flex-col items-center justify-center leading-[1.15]">
                  <div class="font-mono font-black text-emerald-600 dark:text-emerald-400 text-[12px] sm:text-[13px] tracking-tight">
                    <span class="text-[8px] sm:text-[8.5px] font-bold text-[var(--text-muted)] mr-0.5 tracking-normal">第2</span>${{train.t2_arr_time}}
                  </div>
                  <div class="font-mono font-black text-[#004098] dark:text-[#38bdf8] text-[12px] sm:text-[13px] tracking-tight">
                    <span class="text-[8px] sm:text-[8.5px] font-bold text-[var(--text-muted)] mr-0.5 tracking-normal">第1</span>${{train.arr_time}}
                  </div>
                </div>
              </div>

              <!-- 所要時間 (文字拡大: text-[14.5px], 分はtext-[10.5px] leading-none) -->
              <div class="col-span-2 text-right leading-none pr-0.5">
                <span class="text-[14.5px] sm:text-[15.5px] font-black font-mono text-[var(--text-main)]">${{train.total_min}}</span><span class="text-[10.5px] font-bold text-[var(--text-muted)] ml-0.5">分</span>
              </div>
            </div>

            <!-- Detail Accordion -->
            ${{isSelected ? `
              <div class="px-4 py-3 bg-[var(--bg-card)] border-t border-[var(--border-color)] text-xs space-y-2.5 animate-fadeIn">
                <div class="flex items-center justify-between pb-1.5 border-b border-[var(--border-color)]/70">
                  <div class="flex items-center gap-1.5">
                    <span class="font-extrabold text-xs text-[#004098] dark:text-[#38bdf8]">#${{train.no}}</span>
                    <span class="font-bold text-xs text-[var(--text-main)]">${{train.via}}</span>
                  </div>
                  <span class="text-[11px] font-mono font-bold text-emerald-600 dark:text-emerald-400">成田空港(第1)まで ${{train.total_min}}分</span>
                </div>

                <!-- 運行ルートと乗換詳細 -->
                <div class="bg-[var(--accent-color)] p-2.5 rounded-xl border border-[var(--border-color)] space-y-1.5 text-[11px]">
                  <div class="flex items-start gap-2">
                    <span class="text-[#004098] dark:text-[#38bdf8] font-bold shrink-0">🛫 運行概要:</span>
                    <span class="font-medium text-[var(--text-main)]">${{train.transfer_desc}}</span>
                  </div>
                  <div class="flex items-start gap-2 text-[10px] text-[var(--text-muted)] pt-1 border-t border-[var(--border-color)]/50">
                    <span class="font-bold text-[var(--text-main)]">利用路線:</span>
                    <span>${{train.transports.join(' ➔ ')}}</span>
                  </div>
                </div>

                <!-- ターミナル別到着時刻案内 -->
                <div class="grid grid-cols-2 gap-2 text-center">
                  <div class="p-2 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 shadow-xs">
                    <span class="text-[10px] font-semibold text-emerald-800 dark:text-emerald-300 block">第2・第3ターミナル</span>
                    <div class="text-xs font-black text-emerald-700 dark:text-emerald-300 mt-0.5">
                      空港第２ビル <span class="font-mono text-sm">${{train.t2_arr_time}}</span>着
                    </div>
                  </div>
                  <div class="p-2 rounded-xl bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800/60 shadow-xs">
                    <span class="text-[10px] font-semibold text-blue-800 dark:text-blue-300 block">第1ターミナル</span>
                    <div class="text-xs font-black text-[#004098] dark:text-[#38bdf8] mt-0.5">
                      成田空港 <span class="font-mono text-sm">${{train.arr_time}}</span>着
                    </div>
                  </div>
                </div>

                <!-- 運賃・ライナー券不要案内 -->
                <div class="flex items-center justify-between text-[11px] pt-1 px-1 text-[var(--text-muted)]">
                  <div class="flex items-center gap-1.5">
                    <span class="px-1.5 py-0.5 rounded text-[10px] bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold border border-slate-200 dark:border-slate-700">
                      IC運賃 ${{train.fare_ic}}円 (きっぷ ${{train.fare_ticket}}円)
                    </span>
                  </div>
                  <span class="text-[10px] font-bold text-emerald-600 dark:text-emerald-400">特急料金・ライナー券 不要</span>
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

index_path = os.path.join(BASE_DIR, "index.html")
index_org_path = os.path.join(BASE_DIR, "index_org.html")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(index_org_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully updated with enlarged text:\n  {index_path}\n  {index_org_path}")
