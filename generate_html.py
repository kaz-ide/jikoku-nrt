import os
import json

BASE_DIR = r"C:\Users\HINOTORI\.gemini\antigravity\scratch\jikoku_nrt"
data_path = os.path.join(BASE_DIR, "all_trains_data.json")

with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

weekday_json = json.dumps(data['weekday'], ensure_ascii=False)
weekend_json = json.dumps(data['weekend'], ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>京成上野駅 ➔ 成田空港 時刻表（スカイライナー ＆ 京成在来線）</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* 京成電鉄 スカイライナー新AE形 カラーパレット
       ウインドブルー（ストリームブルー / 藍色・ミッドナイトブルー）: #081a3a / #0d2757
       ストームホワイト（純白・アイボリー）: #ffffff / #f0f4f9
       プラチナシルバー: #cbd5e1
    */
    :root {{
      --bg-page: #f0f4f9;
      --bg-card: #ffffff;
      --border-color: #d1dde9;
      --text-main: #071735;
      --text-muted: #526782;
      --wind-blue: #092048;
      --wind-blue-light: #123472;
      --wind-blue-dark: #051228;
      --storm-white: #ffffff;
      --accent-color: #eaf1f8;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg-page: #050e1c;
        --bg-card: #0c182c;
        --border-color: #1a2f4c;
        --text-main: #f0f5fc;
        --text-muted: #8ea5c4;
        --wind-blue: #143d80;
        --wind-blue-light: #2053a4;
        --wind-blue-dark: #091a38;
        --storm-white: #ffffff;
        --accent-color: #12223a;
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
      background: rgba(9, 32, 72, 0.3);
      border-radius: 4px;
    }}
    .no-scrollbar::-webkit-scrollbar {{
      display: none;
    }}
    .no-scrollbar {{
      -ms-overflow-style: none;
      scrollbar-width: none;
    }}

    /* Active Time Band Tab (新AE形ウインドブルー) */
    .tab-active {{
      background-color: var(--wind-blue) !important;
      color: #ffffff !important;
      font-weight: 800;
      box-shadow: 0 2px 6px rgba(9, 32, 72, 0.35);
    }}

    /* Skyliner Tab Active Special Styling */
    .tab-skyliner-active {{
      background: linear-gradient(135deg, #071735 0%, #163d7e 100%) !important;
      color: #ffffff !important;
      border: 1px solid #6095ea !important;
      font-weight: 800;
      box-shadow: 0 2px 8px rgba(12, 40, 92, 0.45);
    }}

    /* Day Tab Active */
    .day-tab-active {{
      background-color: #ffffff !important;
      color: #081a3a !important;
      font-weight: 900;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }}
    @media (prefers-color-scheme: dark) {{
      .day-tab-active {{
        background-color: #1a4994 !important;
        color: #ffffff !important;
      }}
    }}

    /* Filter button active */
    .filter-btn-active {{
      background-color: #ffffff !important;
      color: #081a3a !important;
      border-color: #ffffff !important;
      font-weight: 800;
    }}
  </style>
</head>
<body class="antialiased p-1.5 sm:p-4 min-h-screen flex flex-col justify-start">
  
  <div class="w-full max-w-lg mx-auto bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl shadow-2xl overflow-hidden flex flex-col">

    <!-- 新AE形フロントノーズ・シルバーアクセントライン -->
    <div class="h-1 w-full bg-gradient-to-r from-sky-400 via-white to-blue-500"></div>

    <!-- Header Section (新AE形 ウインドブルー ＆ ストームホワイト) -->
    <header class="px-3.5 py-3 bg-gradient-to-br from-[#06152f] via-[#0c244f] to-[#081a3a] text-white shadow-lg border-b border-white/15">
      <div class="flex items-center justify-between">
        <div>
          <div class="flex items-center gap-1.5 flex-wrap">
            <span class="inline-block w-2.5 h-2.5 rounded-full bg-sky-400 animate-pulse"></span>
            <h1 class="text-base font-black tracking-tight text-white drop-shadow-sm flex items-center gap-1.5">
              <span>京成上野</span>
              <span class="text-sky-300 font-normal">➔</span>
              <span>成田空港</span>
            </h1>
            <span class="text-[9.5px] px-1.5 py-0.5 rounded font-black bg-white/20 text-sky-100 border border-white/30 tracking-tight">スカイライナー ＆ 一般列車</span>
          </div>
          <p class="text-[11px] text-sky-200 mt-0.5 font-medium flex items-center gap-2">
            <span>🚄 スカイライナー最速41分</span>
            <span class="opacity-40">|</span>
            <span class="text-emerald-300">一般列車 ライナー券不要</span>
          </p>
        </div>

        <!-- Direct Train Toggle Button -->
        <button id="directToggle" onclick="toggleDirectFilter()" class="flex items-center gap-1 px-2.5 py-1.5 rounded-xl border border-white/30 bg-white/10 hover:bg-white/20 transition text-xs font-semibold text-white shadow-xs">
          <span>✨</span>
          <span id="directToggleLabel">直通のみ</span>
        </button>
      </div>

      <!-- Quick Criteria & Legend -->
      <div class="mt-2.5 pt-2 border-t border-white/15 flex flex-wrap gap-x-2.5 gap-y-1 text-[10px] text-sky-100 items-center">
        <span class="text-sky-200 font-bold bg-sky-950/60 px-1.5 py-0.2 rounded border border-sky-400/40">🚄 スカイライナー 41便/日</span>
        <span class="text-emerald-200 font-bold">✅ アクセス特急・本線特急網羅</span>
        <span>❌ 到達不能便除外</span>
      </div>

      <!-- Schedule Type (Weekday / Weekend) Toggle Switch & Via Filter -->
      <div class="mt-2.5 pt-2 border-t border-white/15 flex items-center justify-between gap-2">
        <!-- Day Tab (平日/土休日) -->
        <div class="flex items-center gap-1 bg-black/35 p-1 rounded-xl text-xs flex-1 border border-white/10">
          <button id="btnWeekday" onclick="setDayType('weekday')" class="day-tab flex-1 py-1.5 px-2 rounded-lg text-center transition font-bold text-xs text-sky-100">
            🏢 平日ダイヤ
          </button>
          <button id="btnWeekend" onclick="setDayType('weekend')" class="day-tab flex-1 py-1.5 px-2 rounded-lg text-center transition font-bold text-xs text-sky-100">
            🏖️ 土休日ダイヤ
          </button>
        </div>

        <!-- Via Line Filter Pill -->
        <div class="flex items-center gap-1 text-[11px]">
          <button id="filterViaAll" onclick="setViaFilter('all')" class="filter-via-btn px-2 py-1.5 rounded-lg border border-white/40 bg-white text-[#081a3a] transition text-[10px] font-black filter-btn-active shadow-xs">
            全経由
          </button>
          <button id="filterViaSky" onclick="setViaFilter('sky')" class="filter-via-btn px-2 py-1.5 rounded-lg border border-white/25 bg-black/30 text-orange-200 transition text-[10px] font-medium hover:bg-white/15">
            ✈️アクセス
          </button>
          <button id="filterViaMain" onclick="setViaFilter('main')" class="filter-via-btn px-2 py-1.5 rounded-lg border border-white/25 bg-black/30 text-sky-100 transition text-[10px] font-medium hover:bg-white/15">
            🚃本線
          </button>
        </div>
      </div>
    </header>

    <!-- Time Band Tabs (スカイライナー専用タブ完備) -->
    <nav class="p-1.5 bg-[var(--accent-color)] border-b border-[var(--border-color)] flex items-center gap-1 overflow-x-auto no-scrollbar text-xs">
      <button class="tab-btn flex-1 min-w-[52px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="now" onclick="changeBand('now')">
        ⏱️ 次の便
      </button>
      <button class="tab-btn flex-1 min-w-[70px] py-1.5 px-1 rounded-lg text-center transition font-black text-[11px] text-sky-800 dark:text-sky-300 bg-sky-100 dark:bg-sky-950/60 border border-sky-300 dark:border-sky-700/80 hover:bg-sky-200" data-band="skyliner" onclick="changeBand('skyliner')">
        🚄 ライナー
      </button>
      <button class="tab-btn flex-1 min-w-[48px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="morning" onclick="changeBand('morning')">
        🌅 朝 <span class="opacity-75 text-[9px] block sm:inline">5-9</span>
      </button>
      <button class="tab-btn flex-1 min-w-[48px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="day" onclick="changeBand('day')">
        ☀️ 昼 <span class="opacity-75 text-[9px] block sm:inline">10-15</span>
      </button>
      <button class="tab-btn flex-1 min-w-[48px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="evening" onclick="changeBand('evening')">
        🌇 夕 <span class="opacity-75 text-[9px] block sm:inline">16-19</span>
      </button>
      <button class="tab-btn flex-1 min-w-[48px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="night" onclick="changeBand('night')">
        🌙 夜 <span class="opacity-75 text-[9px] block sm:inline">20-23</span>
      </button>
      <button class="tab-btn py-1.5 px-2 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]" data-band="all" onclick="changeBand('all')">
        全便
      </button>
    </nav>

    <!-- Table Sticky Column Headers -->
    <div class="grid grid-cols-12 px-2.5 sm:px-3 py-2 text-[11px] font-black text-[var(--text-muted)] bg-[var(--bg-card)] border-b border-[var(--border-color)] items-center shadow-xs">
      <div class="col-span-2 text-center text-[#081a3a] dark:text-[#38bdf8]">上野発</div>
      <div class="col-span-3 text-center">種別 / 経由</div>
      <div class="col-span-2 text-center">乗換</div>
      <div class="col-span-3 text-center">
        <span class="text-emerald-700 dark:text-emerald-400">第2ビル</span> / <span class="text-[#092048] dark:text-[#38bdf8]">第1空港</span>
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
        <span class="inline-block w-2 h-2 rounded-full bg-[#092048] dark:bg-[#38bdf8]"></span>
        <span>行タップで詳細(乗換・停車駅・料金)</span>
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

    function getTrainBadgeClass(train) {{
      if (train.is_skyliner) {{
        return 'bg-gradient-to-r from-[#06152f] via-[#0d2757] to-[#163d7e] text-white border border-[#4872b2] shadow-xs';
      }}
      switch(train.train_type) {{
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
        btnH.className = 'day-tab flex-1 py-1.5 px-2 rounded-lg text-center transition font-bold text-xs text-sky-100 hover:text-white';
      }} else {{
        btnH.className = 'day-tab flex-1 py-1.5 px-2 rounded-lg text-center transition font-black text-xs day-tab-active';
        btnW.className = 'day-tab flex-1 py-1.5 px-2 rounded-lg text-center transition font-bold text-xs text-sky-100 hover:text-white';
      }}

      // Update Via Buttons
      ['all', 'sky', 'main'].forEach(v => {{
        const btn = document.getElementById('filterVia' + v.charAt(0).toUpperCase() + v.slice(1));
        if (viaFilter === v) {{
          btn.className = 'filter-via-btn px-2 py-1.5 rounded-lg border border-white bg-white text-[#081a3a] transition text-[10px] font-black shadow-xs';
        }} else {{
          let colorClass = 'text-sky-100';
          if (v === 'sky') colorClass = 'text-orange-200';
          if (v === 'main') colorClass = 'text-sky-100';
          btn.className = `filter-via-btn px-2 py-1.5 rounded-lg border border-white/25 bg-black/30 ${{colorClass}} transition text-[10px] font-medium hover:bg-white/15`;
        }}
      }});

      // Update Band Tabs
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        const b = btn.dataset.band;
        if (b === activeBand) {{
          if (b === 'skyliner') {{
            btn.className = 'tab-btn tab-skyliner-active flex-1 min-w-[70px] py-1.5 px-1 rounded-lg text-center transition font-black text-[11px]';
          }} else {{
            btn.className = 'tab-btn tab-active flex-1 min-w-[48px] py-1.5 px-1 rounded-lg text-center transition font-black text-[11px]';
          }}
        }} else {{
          if (b === 'skyliner') {{
            btn.className = 'tab-btn flex-1 min-w-[70px] py-1.5 px-1 rounded-lg text-center transition font-black text-[11px] text-sky-800 dark:text-sky-300 bg-sky-100 dark:bg-sky-950/60 border border-sky-300 dark:border-sky-700/80 hover:bg-sky-200';
          }} else {{
            btn.className = 'tab-btn flex-1 min-w-[48px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--text-muted)] hover:bg-[var(--bg-card)]';
          }}
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

      // Filter by Band / Skyliner
      const nowMin = getNowMinutes();
      if (activeBand === 'skyliner') {{
        // Dedicated Skyliner tab: show all skyliners of the day
        items = items.filter(t => t.is_skyliner);
      }} else if (activeBand === 'now') {{
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
        const badgeClass = getTrainBadgeClass(train);
        const isSky = train.via.includes('スカイアクセス');
        
        const viaBadge = isSky 
          ? `<span class="inline-block px-1 py-0.2 rounded text-[9px] font-black bg-orange-100 text-orange-800 dark:bg-orange-950/80 dark:text-orange-300 border border-orange-300 dark:border-orange-800 leading-none">SA線</span>`
          : `<span class="inline-block px-1 py-0.2 rounded text-[9px] font-black bg-blue-100 text-blue-800 dark:bg-blue-950/80 dark:text-blue-300 border border-blue-200 dark:border-blue-800 leading-none">本線</span>`;

        // Transfer Badge
        let transferBadge = '';
        if (train.is_skyliner) {{
          transferBadge = `<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-black text-sky-800 bg-sky-50 dark:bg-sky-950/70 dark:text-sky-200 border border-sky-300 dark:border-sky-700 leading-tight">直通(指定)</span>`;
        }} else if (train.is_direct) {{
          transferBadge = `<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10.5px] font-bold text-emerald-700 bg-emerald-50 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-700 leading-tight">直通</span>`;
        }} else {{
          transferBadge = `<span class="inline-flex items-center px-1 py-0.5 rounded text-[10px] font-bold text-amber-700 bg-amber-50 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-300 dark:border-amber-700 leading-tight">${{train.transfer_station}}乗換</span>`;
        }}

        // Row background tint for Skyliner
        const rowBgClass = train.is_skyliner 
          ? (isSelected ? 'bg-sky-100/70 dark:bg-sky-950/50' : 'bg-sky-50/40 dark:bg-sky-950/20 hover:bg-sky-100/50 dark:hover:bg-sky-900/30')
          : (isSelected ? 'bg-[var(--accent-color)]' : 'hover:bg-[var(--accent-color)]/60');

        return `
          <div class="transition-colors ${{rowBgClass}}">
            <div onclick="toggleRow(${{train.no}})" class="grid grid-cols-12 px-2.5 sm:px-3 py-2 items-center cursor-pointer">
              
              <!-- 上野発 (文字拡大: text-[15.5px]〜16.5px) -->
              <div class="col-span-2 text-center">
                <span class="text-[15.5px] sm:text-[16.5px] font-black font-mono tracking-tighter text-[#092048] dark:text-[#38bdf8] leading-none">${{train.dep_time}}</span>
              </div>

              <!-- 種別 / 経由 -->
              <div class="col-span-3 flex flex-col items-center justify-center gap-0.5 leading-none">
                <span class="px-1.5 py-0.5 rounded text-[10px] font-black ${{badgeClass}} text-center leading-none">
                  ${{train.is_skyliner ? (train.liner_name || 'スカイライナー') : train.train_type}}
                </span>
                <div>${{viaBadge}}</div>
              </div>

              <!-- 乗換 -->
              <div class="col-span-2 text-center leading-none">
                ${{transferBadge}}
              </div>

              <!-- 空港着: 第2ビル ＆ 第1空港 両方表示 -->
              <div class="col-span-3 text-center">
                <div class="flex flex-col items-center justify-center leading-[1.15]">
                  <div class="font-mono font-black text-emerald-600 dark:text-emerald-400 text-[12px] sm:text-[13px] tracking-tight">
                    <span class="text-[8px] sm:text-[8.5px] font-bold text-[var(--text-muted)] mr-0.5 tracking-normal">第2</span>${{train.t2_arr_time}}
                  </div>
                  <div class="font-mono font-black text-[#092048] dark:text-[#38bdf8] text-[12px] sm:text-[13px] tracking-tight">
                    <span class="text-[8px] sm:text-[8.5px] font-bold text-[var(--text-muted)] mr-0.5 tracking-normal">第1</span>${{train.arr_time}}
                  </div>
                </div>
              </div>

              <!-- 所要時間 (スカイライナーは最速41-44分!) -->
              <div class="col-span-2 text-right leading-none pr-0.5">
                <span class="text-[14.5px] sm:text-[15.5px] font-black font-mono ${{train.is_skyliner ? 'text-sky-700 dark:text-sky-300' : 'text-[var(--text-main)]'}}">${{train.total_min}}</span><span class="text-[10.5px] font-bold text-[var(--text-muted)] ml-0.5">分</span>
              </div>
            </div>

            <!-- Detail Accordion -->
            ${{isSelected ? `
              <div class="px-4 py-3 bg-[var(--bg-card)] border-t border-[var(--border-color)] text-xs space-y-2.5 animate-fadeIn">
                <div class="flex items-center justify-between pb-1.5 border-b border-[var(--border-color)]/70">
                  <div class="flex items-center gap-1.5">
                    <span class="font-extrabold text-xs text-[#092048] dark:text-[#38bdf8]">#${{train.no}}</span>
                    <span class="font-bold text-xs text-[var(--text-main)]">${{train.is_skyliner ? '🚄 ' + train.liner_name : train.via}}</span>
                  </div>
                  <span class="text-[11px] font-mono font-black ${{train.is_skyliner ? 'text-sky-600 dark:text-sky-400' : 'text-emerald-600 dark:text-emerald-400'}}">
                    成田空港(第1)まで ${{train.total_min}}分 ${{train.is_skyliner ? '⚡ 最速' : ''}}
                  </span>
                </div>

                <!-- 運行ルートと乗換詳細 -->
                <div class="${{train.is_skyliner ? 'bg-sky-50 dark:bg-sky-950/40 border-sky-200 dark:border-sky-800/60' : 'bg-[var(--accent-color)] border-[var(--border-color)]'}} p-2.5 rounded-xl border space-y-1.5 text-[11px]">
                  <div class="flex items-start gap-2">
                    <span class="${{train.is_skyliner ? 'text-sky-700 dark:text-sky-300' : 'text-[#092048] dark:text-[#38bdf8]'}} font-bold shrink-0">🛫 運行概要:</span>
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
                  <div class="p-2 rounded-xl bg-sky-50 dark:bg-sky-950/40 border border-sky-200 dark:border-sky-800/60 shadow-xs">
                    <span class="text-[10px] font-semibold text-sky-800 dark:text-sky-300 block">第1ターミナル</span>
                    <div class="text-xs font-black text-[#092048] dark:text-[#38bdf8] mt-0.5">
                      成田空港 <span class="font-mono text-sm">${{train.arr_time}}</span>着
                    </div>
                  </div>
                </div>

                <!-- 運賃・ライナー券案内 -->
                <div class="flex items-center justify-between text-[11px] pt-1 px-1 text-[var(--text-muted)]">
                  <div class="flex items-center gap-1.5 flex-wrap">
                    <span class="px-1.5 py-0.5 rounded text-[10px] bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold border border-slate-200 dark:border-slate-700">
                      ${{train.is_skyliner ? `乗車券 ${{train.fare_ic - 1300}}円 + ライナー券 1,300円 = 計${{train.fare_ic}}円` : `IC運賃 ${{train.fare_ic}}円 (きっぷ ${{train.fare_ticket}}円)`}}
                    </span>
                  </div>
                  <span class="text-[10px] font-black ${{train.is_skyliner ? 'text-sky-600 dark:text-sky-400' : 'text-emerald-600 dark:text-emerald-400'}}">
                    ${{train.is_skyliner ? '※全席指定席・ライナー券必要' : '特急料金不要(乗車券のみ)'}}
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

index_path = os.path.join(BASE_DIR, "index.html")
index_org_path = os.path.join(BASE_DIR, "index_org.html")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(index_org_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully updated with Skyliners and New AE-shape styling:\n  {index_path}\n  {index_org_path}")
