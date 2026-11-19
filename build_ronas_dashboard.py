"""
Generates groundwater_ai_portal.html with:
1. Larger Map on the main dashboard (height increased from 320px to 520px with crisp viewport and zoom controls).
2. Tonal card hierarchy: Critical cards are grayish-black (#27272a), High Risk cards are medium graphite-slate (#474c56), Moderate cards are soft light gray-slate (#f1f3f7), and Safe cards are crisp white (#ffffff) — getting progressively lighter with decreasing risk!
3. Big, prominent, highlighted "Select Well:" dropdown bar in Predictions Hub styled with a hydro-blue gradient container (#eff6ff, border-2 border-blue-400, large font, prominent badge).
4. Renamed "Cross-Verify" -> "Result Validation" across sidebar, titles, buttons, and metrics.
5. Zero occurrences of "DSS" anywhere.
"""

import json
from pathlib import Path

RESULTS_PATH = Path("trained_model_results.json")
with open(RESULTS_PATH, "r", encoding="utf-8") as f:
    results = json.load(f)

html_template = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AQUORA — AI Groundwater Intelligence & Early Warning Platform</title>
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            app: {
              bg: '#fcfbf9',
              sidebar: '#ffffff',
              card: '#ffffff',
              cardMuted: '#fbfaf7',
              border: '#eeece6',
              borderLight: '#f4f3ef',
              text: '#18181b',
              muted: '#71717a',
              subtle: '#a1a1aa'
            },
            aquora: {
              dark: '#18181b',
              blue: '#2563eb',
              cyan: '#0284c7',
              emerald: '#059669',
              amber: '#d97706',
              rose: '#dc2626'
            }
          },
          fontFamily: {
            sans: ['"Inter"', 'system-ui', '-apple-system', 'sans-serif'],
            display: ['"Plus Jakarta Sans"', '"Inter"', 'sans-serif'],
            mono: ['"DM Mono"', '"Space Mono"', 'monospace'],
          }
        }
      }
    }
  </script>

  <!-- Google Fonts, Leaflet & Chart.js -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    body {
      background-color: #fcfbf9;
      color: #18181b;
      font-family: 'Inter', system-ui, sans-serif;
      letter-spacing: -0.011em;
    }

    .font-display { font-family: 'Plus Jakarta Sans', sans-serif; }
    .mono { font-family: 'DM Mono', monospace; font-variant-numeric: tabular-nums; }

    /* Graduated Tonal Risk Cards */
    .saas-card-critical {
      background-color: #27272a;
      color: #ffffff;
      border: 1px solid #3f3f46;
      border-radius: 14px;
      transition: all 0.2s ease;
    }
    .saas-card-critical:hover {
      background-color: #1f1f23;
      border-color: #52525b;
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }

    .saas-card-high {
      background-color: #4b5058;
      color: #ffffff;
      border: 1px solid #5d636e;
      border-radius: 14px;
      transition: all 0.2s ease;
    }
    .saas-card-high:hover {
      background-color: #3f444c;
      border-color: #6b7280;
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    }

    .saas-card-moderate {
      background-color: #f1f3f7;
      color: #18181b;
      border: 1px solid #e2e5eb;
      border-radius: 14px;
      transition: all 0.2s ease;
    }
    .saas-card-moderate:hover {
      background-color: #e8ecf2;
      border-color: #cbd5e1;
      transform: translateY(-2px);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }

    .saas-card-safe {
      background-color: #ffffff;
      color: #18181b;
      border: 1px solid #eeece6;
      border-radius: 14px;
      transition: all 0.2s ease;
    }
    .saas-card-safe:hover {
      border-color: #dedbd2;
      transform: translateY(-2px);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }

    .saas-card {
      background-color: #ffffff;
      border: 1px solid #eeece6;
      border-radius: 16px;
      transition: all 0.2s ease;
    }
    .saas-card:hover {
      border-color: #dedbd2;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }

    .sidebar-link {
      display: flex;
      items-center;
      gap: 0.75rem;
      padding: 0.625rem 0.875rem;
      border-radius: 12px;
      font-size: 0.8125rem;
      font-weight: 500;
      color: #52525b;
      transition: all 0.15s ease;
      cursor: pointer;
    }
    .sidebar-link:hover {
      color: #18181b;
      background-color: #f4f3ef;
    }
    .sidebar-link.active {
      color: #18181b;
      background-color: #eeece6;
      font-weight: 600;
    }

    /* Views */
    .view-panel {
      display: none;
      animation: fadeIn 0.2s ease-in-out forwards;
    }
    .view-panel.active-view {
      display: block;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(3px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Leaflet popup customization */
    .leaflet-popup-content-wrapper {
      background: #ffffff !important;
      color: #18181b !important;
      border: 1px solid #eeece6 !important;
      border-radius: 14px !important;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08) !important;
      padding: 4px !important;
    }
    .leaflet-popup-tip {
      background: #ffffff !important;
    }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #fcfbf9; }
    ::-webkit-scrollbar-thumb { background: #dedbd2; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #c5c1b5; }
  </style>
</head>
<body class="min-h-screen bg-[#fcfbf9] text-[#18181b] antialiased flex flex-row">

  <!-- LEFT SIDEBAR -->
  <aside class="w-64 min-h-screen bg-white border-r border-[#eeece6] flex flex-col justify-between p-5 sticky top-0 shrink-0 z-40">
    <div class="space-y-7">
      
      <!-- LOGO / BRAND (NO 'DSS') -->
      <div class="flex items-center space-x-2.5 px-2 py-1">
        <div class="w-8 h-8 rounded-xl bg-[#18181b] text-white flex items-center justify-center font-bold text-sm">
          A
        </div>
        <span class="text-xl font-extrabold font-display tracking-tight text-[#18181b]">
          AQUORA
        </span>
      </div>

      <!-- MAIN NAVIGATION LIST (RENAMED TO RESULT VALIDATION) -->
      <nav class="space-y-1">
        <div onclick="switchView('dashboard')" id="nav-dashboard" class="sidebar-link active">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
          <span class="flex-grow">Dashboard</span>
        </div>

        <div onclick="switchView('predictions')" id="nav-predictions" class="sidebar-link">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
          <span class="flex-grow">Predictions</span>
          <span class="text-[10px] font-mono px-1.5 py-0.5 rounded-full bg-[#f4f3ef] text-[#71717a]">174</span>
        </div>

        <!-- RENAMED TO RESULT VALIDATION -->
        <div onclick="switchView('verify')" id="nav-verify" class="sidebar-link">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          <span class="flex-grow">Result Validation</span>
          <span class="text-[10px] font-mono px-1.5 py-0.5 rounded-full bg-[#ecfdf5] text-[#059669]">96.3%</span>
        </div>

        <div onclick="switchView('gis-map')" id="nav-gis-map" class="sidebar-link">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>
          <span class="flex-grow">GIS Map</span>
        </div>

        <div onclick="switchView('benchmarks')" id="nav-benchmarks" class="sidebar-link">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
          <span class="flex-grow">Benchmarks</span>
        </div>

        <div onclick="switchView('explainability')" id="nav-explainability" class="sidebar-link">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/></svg>
          <span class="flex-grow">Explainability</span>
        </div>
      </nav>

      <!-- SECONDARY SECTION: ADMINISTRATIVE BLOCKS -->
      <div class="space-y-2 pt-2">
        <span class="text-[10px] font-mono uppercase tracking-wider text-[#a1a1aa] px-2 block">
          Key Blocks (Jaipur)
        </span>
        <div class="space-y-1">
          <div onclick="filterByBlockFromSidebar('GOVINDGARH')" class="flex items-center justify-between px-2.5 py-1.5 text-xs text-[#52525b] hover:text-[#18181b] hover:bg-[#f4f3ef] rounded-lg cursor-pointer transition">
            <span class="flex items-center space-x-2">
              <span class="w-1.5 h-1.5 rounded-full bg-[#71717a]"></span>
              <span>Govindgarh</span>
            </span>
            <span class="text-[10px] mono text-[#a1a1aa]">12</span>
          </div>
          <div onclick="filterByBlockFromSidebar('SAMBHER')" class="flex items-center justify-between px-2.5 py-1.5 text-xs text-[#52525b] hover:text-[#18181b] hover:bg-[#f4f3ef] rounded-lg cursor-pointer transition">
            <span class="flex items-center space-x-2">
              <span class="w-1.5 h-1.5 rounded-full bg-[#71717a]"></span>
              <span>Sambher</span>
            </span>
            <span class="text-[10px] mono text-[#a1a1aa]">18</span>
          </div>
          <div onclick="filterByBlockFromSidebar('JHOTWARA')" class="flex items-center justify-between px-2.5 py-1.5 text-xs text-[#52525b] hover:text-[#18181b] hover:bg-[#f4f3ef] rounded-lg cursor-pointer transition">
            <span class="flex items-center space-x-2">
              <span class="w-1.5 h-1.5 rounded-full bg-[#71717a]"></span>
              <span>Jhotwara</span>
            </span>
            <span class="text-[10px] mono text-[#a1a1aa]">14</span>
          </div>
          <div onclick="filterByBlockFromSidebar('AMER')" class="flex items-center justify-between px-2.5 py-1.5 text-xs text-[#52525b] hover:text-[#18181b] hover:bg-[#f4f3ef] rounded-lg cursor-pointer transition">
            <span class="flex items-center space-x-2">
              <span class="w-1.5 h-1.5 rounded-full bg-[#71717a]"></span>
              <span>Amer</span>
            </span>
            <span class="text-[10px] mono text-[#a1a1aa]">16</span>
          </div>
        </div>
      </div>
    </div>

    <!-- SIDEBAR USER FOOTER -->
    <div class="border-t border-[#eeece6] pt-4 flex items-center justify-between">
      <div class="flex items-center space-x-2.5">
        <div class="w-8 h-8 rounded-full bg-[#18181b] text-white flex items-center justify-center font-bold text-xs">
          JP
        </div>
        <div>
          <p class="text-xs font-semibold text-[#18181b]">Jaipur Hydro Cell</p>
          <p class="text-[10px] text-[#71717a]">CGWB Monitoring</p>
        </div>
      </div>
      <button class="text-[#a1a1aa] hover:text-[#18181b] transition">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
      </button>
    </div>
  </aside>

  <!-- MAIN WORKSPACE CONTENT -->
  <main class="flex-grow p-6 lg:p-8 space-y-7 overflow-x-hidden">

    <!-- TOP SEARCH & ACTION BAR -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      
      <!-- SEARCH INPUT PILL -->
      <div class="relative flex-grow max-w-md">
        <svg class="w-4 h-4 text-[#a1a1aa] absolute left-3.5 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <input type="text" id="globalSearchInput" placeholder="Search well, village, or block..." class="w-full bg-white border border-[#eeece6] rounded-full pl-9 pr-4 py-2 text-xs text-[#18181b] focus:outline-none focus:border-[#18181b] transition shadow-xs">
      </div>

      <!-- RIGHT ACTIONS PILLS -->
      <div class="flex items-center space-x-2.5 text-xs text-[#52525b]">
        <button onclick="toggleSortDirection()" class="px-3 py-2 rounded-full border border-[#eeece6] bg-white hover:border-[#18181b] transition flex items-center space-x-1.5 shadow-xs">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12"/></svg>
          <span id="sortLabel">Sort by Depth</span>
        </button>

        <div class="relative">
          <select id="mainBlockFilter" onchange="applyGlobalFilters()" class="px-3 py-2 rounded-full border border-[#eeece6] bg-white hover:border-[#18181b] transition appearance-none pr-7 text-xs focus:outline-none shadow-xs">
            <option value="ALL">All Blocks</option>
          </select>
          <svg class="w-3 h-3 text-[#a1a1aa] absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
        </div>

        <div class="px-3 py-2 rounded-full border border-[#eeece6] bg-white text-xs flex items-center space-x-1.5 shadow-xs">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
          <span>Jaipur Cell</span>
        </div>

        <button onclick="switchView('predictions')" class="px-4 py-2 rounded-full bg-[#18181b] text-white font-medium hover:bg-black transition flex items-center space-x-1.5 shadow-sm">
          <span>+ Forecast Well</span>
        </button>
      </div>

    </div>

    <!-- ======================================================== -->
    <!-- VIEW 1: MAIN DASHBOARD (ENLARGED MAP + GRADUATED CARDS) -->
    <!-- ======================================================== -->
    <div id="view-dashboard" class="view-panel active-view space-y-7">
      
      <!-- TOP EXECUTIVE ANALYTICS STRIP -->
      <div class="bg-[#fbfaf7] border border-[#eeece6] rounded-2xl p-5 sm:p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-6 items-center">
        
        <!-- 1. Mini Bar Chart -->
        <div class="lg:col-span-3 space-y-2">
          <div class="flex items-center justify-between text-xs">
            <span class="font-medium text-[#18181b]">Quarterly Observations</span>
            <span class="text-[10px] mono text-[#a1a1aa]">2015–2024</span>
          </div>
          <div class="flex items-end space-x-2 h-16 pt-2">
            <div class="flex-1 flex flex-col items-center gap-1">
              <div class="w-full bg-[#18181b] rounded-t-sm" style="height: 65%;"></div>
              <span class="text-[9px] text-[#71717a] mono">Q1</span>
            </div>
            <div class="flex-1 flex flex-col items-center gap-1">
              <div class="w-full bg-[#18181b] rounded-t-sm" style="height: 85%;"></div>
              <span class="text-[9px] text-[#71717a] mono">Q2</span>
            </div>
            <div class="flex-1 flex flex-col items-center gap-1">
              <div class="w-full bg-[#18181b] rounded-t-sm" style="height: 100%;"></div>
              <span class="text-[9px] text-[#71717a] mono">Q3</span>
            </div>
            <div class="flex-1 flex flex-col items-center gap-1">
              <div class="w-full bg-[#a1a1aa] rounded-t-sm" style="height: 45%;"></div>
              <span class="text-[9px] text-[#71717a] mono">Q4</span>
            </div>
            <div class="flex-1 flex flex-col items-center gap-1">
              <div class="w-full bg-[#18181b] rounded-t-sm" style="height: 75%;"></div>
              <span class="text-[9px] text-[#71717a] mono">Nov</span>
            </div>
          </div>
        </div>

        <!-- 2. Circular Arc Gauge -->
        <div class="lg:col-span-3 flex items-center justify-center space-x-4 border-l border-[#eeece6] pl-6">
          <div class="relative w-20 h-20 flex items-center justify-center">
            <svg class="w-20 h-20 -rotate-90" viewBox="0 0 36 36">
              <path class="text-[#eeece6]" stroke-width="3.5" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              <path class="text-[#18181b]" stroke-dasharray="96.3, 100" stroke-width="3.5" stroke-linecap="round" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            </svg>
            <div class="absolute text-center">
              <span class="text-sm font-bold font-display text-[#18181b] block">96%</span>
            </div>
          </div>
          <div>
            <span class="text-base font-extrabold font-display text-[#18181b] block">96.3%</span>
            <span class="text-[11px] text-[#71717a] block leading-tight">Result Validation Accuracy (within ±0.5m)</span>
          </div>
        </div>

        <!-- 3. Stat Callout -->
        <div class="lg:col-span-3 border-l border-[#eeece6] pl-6 space-y-1">
          <span class="text-2xl font-bold font-display text-[#18181b] block mono">109</span>
          <div class="flex items-center space-x-1.5 text-xs text-[#71717a]">
            <span>Depletion anomalies flagged</span>
            <span class="text-[#18181b]">→</span>
          </div>
          <span class="text-[10px] text-rose-600 block font-medium">70 Critical Surges (>40m)</span>
        </div>

        <!-- 4. Stat Callout -->
        <div class="lg:col-span-3 border-l border-[#eeece6] pl-6 space-y-1">
          <span class="text-2xl font-bold font-display text-[#18181b] block mono">2,426</span>
          <div class="flex items-center space-x-1.5 text-xs text-[#71717a]">
            <span>CGWB Monitoring records</span>
            <span class="text-[#18181b]">→</span>
          </div>
          <span class="text-[10px] text-[#059669] block font-medium">174 Wells in Jaipur</span>
        </div>

      </div>

      <!-- ENLARGED MAP PORTION (HEIGHT INCREASED TO 520PX AS REQUESTED) -->
      <div class="saas-card p-5 space-y-3.5">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#eeece6] pb-3 px-1">
          <div class="flex items-center space-x-2.5">
            <span class="w-2.5 h-2.5 rounded-full bg-blue-600 animate-pulse"></span>
            <h3 class="text-base font-bold font-display text-[#18181b]">Spatial Groundwater Monitoring Map (Jaipur District)</h3>
            <span class="text-xs text-[#71717a] hidden md:inline">• 174 Spatial Monitoring Wells Loaded with Live Telemetry</span>
          </div>
          <div class="flex flex-wrap items-center gap-2.5 text-xs mono">
            <span class="flex items-center space-x-1.5 px-2 py-0.5 rounded-md bg-red-50 border border-red-200 text-red-700 font-medium">
              <span class="w-2.5 h-2.5 rounded-full bg-[#dc2626] inline-block shadow-xs"></span>
              <span>Critical (>50m): <strong>69</strong></span>
            </span>
            <span class="flex items-center space-x-1.5 px-2 py-0.5 rounded-md bg-orange-50 border border-orange-200 text-orange-800 font-medium">
              <span class="w-2.5 h-2.5 rounded-full bg-[#ea580c] inline-block shadow-xs"></span>
              <span>High Risk (30–50m): <strong>41</strong></span>
            </span>
            <span class="flex items-center space-x-1.5 px-2 py-0.5 rounded-md bg-sky-50 border border-sky-200 text-sky-800 font-medium">
              <span class="w-2.5 h-2.5 rounded-full bg-[#0284c7] inline-block shadow-xs"></span>
              <span>Moderate (15–30m): <strong>16</strong></span>
            </span>
            <span class="flex items-center space-x-1.5 px-2 py-0.5 rounded-md bg-emerald-50 border border-emerald-200 text-emerald-800 font-medium">
              <span class="w-2.5 h-2.5 rounded-full bg-[#10b981] inline-block shadow-xs"></span>
              <span>Safe (&lt;15m): <strong>48</strong></span>
            </span>
            <span id="dashMapCountBadge" class="font-bold text-[#18181b] px-2 py-0.5 rounded-md bg-[#f4f3ef] border border-[#eeece6]">174 stations</span>
          </div>
        </div>
        
        <!-- INCREASED HEIGHT TO 520PX -->
        <div id="mainDashboardMap" class="w-full h-[520px] rounded-2xl overflow-hidden border border-[#eeece6]"></div>
      </div>

      <!-- 4-COLUMN WATER-STRESS BOARD (GRADUATED TONAL PALETTE: DARKEST FOR CRITICAL, LIGHTEST FOR SAFE) -->
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-base font-bold font-display text-[#18181b]">Gram Panchayat Water-Stress Risk Tiers</h2>
            <p class="text-xs text-[#71717a] mt-0.5">Tonal shading graduates from grayish-black for critical aquifers down to lighter tones for lower risk</p>
          </div>
          <span class="text-xs text-[#71717a] mono">Classified via Random Forest & XGBoost</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          
          <!-- COLUMN 1: SAFE (<15m) - LIGHTEST TONE (CRISP WHITE) -->
          <div class="space-y-3">
            <div class="flex items-center justify-between text-xs font-semibold text-[#18181b] px-1 pb-1 border-b border-[#eeece6]">
              <span class="flex items-center space-x-1.5">
                <span class="w-2 h-2 rounded-full bg-[#10b981]"></span>
                <span>Safe (<15m)</span>
              </span>
              <div class="flex items-center space-x-1 text-[#71717a] font-mono text-[11px]">
                <span>847</span>
                <span>⇅</span>
              </div>
            </div>
            <div id="col-safe" class="space-y-2.5">
              <!-- Rendered via JS in crisp white (Lightest) -->
            </div>
          </div>

          <!-- COLUMN 2: MODERATE (15–30m) - SOFT LIGHT SLATE/GRAY TONE -->
          <div class="space-y-3">
            <div class="flex items-center justify-between text-xs font-semibold text-[#18181b] px-1 pb-1 border-b border-[#eeece6]">
              <span class="flex items-center space-x-1.5">
                <span class="w-2 h-2 rounded-full bg-[#0284c7]"></span>
                <span>Moderate (15–30m)</span>
              </span>
              <div class="flex items-center space-x-1 text-[#71717a] font-mono text-[11px]">
                <span>267</span>
                <span>⇅</span>
              </div>
            </div>
            <div id="col-moderate" class="space-y-2.5">
              <!-- Rendered via JS in soft light gray-slate -->
            </div>
          </div>

          <!-- COLUMN 3: HIGH RISK (30–50m) - MEDIUM GRAPHITE SLATE TONE -->
          <div class="space-y-3">
            <div class="flex items-center justify-between text-xs font-semibold text-[#18181b] px-1 pb-1 border-b border-[#eeece6]">
              <span class="flex items-center space-x-1.5">
                <span class="w-2 h-2 rounded-full bg-[#ea580c]"></span>
                <span>High Risk (30–50m)</span>
              </span>
              <div class="flex items-center space-x-1 text-[#71717a] font-mono text-[11px]">
                <span>532</span>
                <span>⇅</span>
              </div>
            </div>
            <div id="col-high" class="space-y-2.5">
              <!-- Rendered via JS in medium dark graphite -->
            </div>
          </div>

          <!-- COLUMN 4: CRITICAL (>50m) - DARKEST TONE (GRAYISH-BLACK) -->
          <div class="space-y-3">
            <div class="flex items-center justify-between text-xs font-semibold text-[#18181b] px-1 pb-1 border-b border-[#eeece6]">
              <span class="flex items-center space-x-1.5">
                <span class="w-2 h-2 rounded-full bg-[#dc2626]"></span>
                <span>Critical (>50m)</span>
              </span>
              <div class="flex items-center space-x-1 text-[#71717a] font-mono text-[11px]">
                <span>758</span>
                <span>⇅</span>
              </div>
            </div>
            <div id="col-critical" class="space-y-2.5">
              <!-- Rendered via JS in grayish-black (Darkest) -->
            </div>
          </div>

        </div>
      </div>

    </div>


    <!-- ======================================================== -->
    <!-- VIEW 2: PREDICTIONS HUB (WITH BIG HIGHLIGHTED DROPDOWN)   -->
    <!-- ======================================================== -->
    <div id="view-predictions" class="view-panel space-y-7">
      
      <!-- SUBPAGE HEADER WITH BIG PROMINENT DROPDOWN HIGHLIGHT -->
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-5 border-b border-[#eeece6] pb-5">
        <div>
          <div class="flex items-center space-x-2 text-[10px] font-mono uppercase text-blue-600 font-bold">
            <span>AQUORA FORECASTING ENGINE · 1–3 MONTHS</span>
          </div>
          <h2 class="text-2xl font-bold font-display text-[#18181b] mt-1">Station Forecasting & Multi-Step Prediction Hub</h2>
          <p class="text-xs text-[#71717a] mt-0.5">High-visibility water table forecasts with directional drop indicators and 95% error margins</p>
        </div>

        <!-- BIG HIGHLIGHTED DROPDOWN SELECTOR (MATCHING USER REQUEST) -->
        <div class="p-2.5 rounded-2xl bg-gradient-to-r from-blue-50/90 via-indigo-50/80 to-blue-50/90 border-2 border-blue-400 shadow-sm flex flex-col sm:flex-row sm:items-center gap-2.5">
          <div class="flex items-center space-x-2 px-2">
            <div class="w-6 h-6 rounded-lg bg-blue-600 text-white flex items-center justify-center text-xs font-bold shadow-xs">
              💧
            </div>
            <span class="text-xs font-bold uppercase tracking-wider text-blue-950 font-display">Select Well:</span>
          </div>
          
          <select id="predWellSelect" class="bg-white border-2 border-blue-300 text-blue-950 text-sm font-bold rounded-xl px-4 py-2.5 focus:outline-none focus:ring-4 focus:ring-blue-100 focus:border-blue-600 shadow-xs min-w-[300px] sm:min-w-[380px] transition">
            <!-- Injected dynamically with station name, block, depth, and tier -->
          </select>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- LARGE FORECAST CARDS (5 COLS) -->
        <div class="lg:col-span-5 saas-card p-6 flex flex-col justify-between space-y-5">
          <div class="space-y-4">
            <div class="border-b border-[#eeece6] pb-3">
              <span class="text-[10px] font-mono uppercase tracking-wider text-[#a1a1aa]">Monitoring Station</span>
              <h3 id="predStationTitle" class="text-2xl font-bold font-display text-[#18181b] mt-0.5">--</h3>
              <p id="predLocationSub" class="text-xs text-[#71717a] mt-0.5">Village • Block • Tehsil</p>
            </div>

            <!-- OBSERVED CALLOUT -->
            <div class="p-4 rounded-xl bg-[#fbfaf7] border border-[#eeece6] flex items-center justify-between">
              <div>
                <span class="text-[10px] font-mono uppercase text-[#71717a]">Current Water Depth</span>
                <p id="predCurrentDepth" class="text-3xl font-extrabold font-display text-[#18181b] mono mt-0.5">-- m</p>
                <span class="text-[10px] text-[#a1a1aa]">CGWB Field Reading</span>
              </div>
              <div id="predRiskBadge" class="px-3 py-1.5 rounded-lg text-xs font-mono font-medium">--</div>
            </div>

            <!-- MULTI-STEP FORWARD CARDS -->
            <div class="space-y-2 pt-1">
              <span class="text-[10px] font-mono uppercase text-[#a1a1aa] block tracking-wider">Multi-Step Forward AI Predictions</span>
              
              <div class="p-3.5 rounded-xl bg-white border border-[#eeece6] flex items-center justify-between shadow-xs">
                <div>
                  <span class="text-xs font-semibold text-[#18181b]">+1 Month (30 Days Forward)</span>
                  <p class="text-[10px] text-[#71717a]">Short-term trajectory</p>
                </div>
                <div class="text-right">
                  <span id="predF1Val" class="text-base font-bold text-[#18181b] mono">-- m</span>
                  <p id="predDelta1" class="text-[11px] mono mt-0.5">--</p>
                </div>
              </div>

              <div class="p-3.5 rounded-xl bg-white border border-[#eeece6] flex items-center justify-between shadow-xs">
                <div>
                  <span class="text-xs font-semibold text-[#18181b]">+2 Months (60 Days Forward)</span>
                  <p class="text-[10px] text-[#71717a]">Mid-term seasonal shift</p>
                </div>
                <div class="text-right">
                  <span id="predF2Val" class="text-base font-bold text-[#18181b] mono">-- m</span>
                  <p id="predDelta2" class="text-[11px] mono mt-0.5">--</p>
                </div>
              </div>

              <div class="p-3.5 rounded-xl bg-[#27272a] text-white flex items-center justify-between shadow-sm">
                <div>
                  <span class="text-xs font-semibold text-white">+3 Months (90 Days Forward)</span>
                  <p class="text-[10px] text-[#a1a1aa]">Quarterly planning horizon</p>
                </div>
                <div class="text-right">
                  <span id="predF3Val" class="text-base font-bold text-white mono">-- m</span>
                  <p id="predDelta3" class="text-[11px] mono mt-0.5 text-blue-300">--</p>
                </div>
              </div>
            </div>

            <!-- RISK OUTLOOK -->
            <div class="p-3.5 rounded-xl bg-[#fbfaf7] border border-[#eeece6] text-xs text-[#52525b]">
              <span class="font-semibold block text-[11px] mono text-[#18181b] uppercase">Quarterly Trajectory & Advisory:</span>
              <p id="predOutlookText" class="mt-1 leading-relaxed">--</p>
            </div>
          </div>

          <div class="text-[11px] mono text-[#71717a] pt-3 border-t border-[#eeece6] flex justify-between">
            <span id="predAnomalyFlag">Anomaly: Normal</span>
            <span>95% Confidence Band: ±0.52m</span>
          </div>
        </div>

        <!-- TRAJECTORY GRAPH (7 COLS) -->
        <div class="lg:col-span-7 saas-card p-6 flex flex-col justify-between space-y-5">
          <div class="flex items-center justify-between border-b border-[#eeece6] pb-3">
            <div>
              <h3 class="text-base font-bold font-display text-[#18181b]">Historical Readings → 90-Day Predictive Trajectory</h3>
              <p class="text-[11px] text-[#71717a]">Actual monitoring observations transitioning into 3-step forecast with shaded 95% error margin band</p>
            </div>
            <div class="flex items-center space-x-3 text-[11px] mono text-[#71717a]">
              <span class="flex items-center space-x-1.5"><span class="w-3 h-0.5 bg-[#18181b] inline-block"></span><span>Actual</span></span>
              <span class="flex items-center space-x-1.5"><span class="w-3 h-0.5 bg-blue-600 inline-block"></span><span>Forecast</span></span>
            </div>
          </div>

          <div class="h-72 w-full">
            <canvas id="predTrajectoryCanvas"></canvas>
          </div>

          <!-- TOP DEPLETIONS ROW -->
          <div class="border-t border-[#eeece6] pt-3">
            <div class="flex items-center justify-between mb-2">
              <span class="text-[11px] font-mono uppercase tracking-wider text-[#18181b] font-semibold">Top Depletion Warnings (Next 90 Days)</span>
              <span class="text-[10px] mono text-blue-600 font-medium">Click well to inspect</span>
            </div>
            <div id="predTopDepletionRow" class="grid grid-cols-2 sm:grid-cols-5 gap-2">
              <!-- Injected dynamically -->
            </div>
          </div>
        </div>

      </div>
    </div>


    <!-- ======================================================== -->
    <!-- VIEW 3: RESULT VALIDATION (RENAMED FROM CROSS-VERIFY)    -->
    <!-- ======================================================== -->
    <div id="view-verify" class="view-panel space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#eeece6] pb-4">
        <div>
          <div class="flex items-center space-x-2 text-[10px] font-mono uppercase text-emerald-600 font-bold">
            <span>GROUND-TRUTH ACCURACY VALIDATION</span>
          </div>
          <h2 class="text-2xl font-bold font-display text-[#18181b] mt-1">Result Validation Explorer</h2>
          <p class="text-xs text-[#71717a] mt-0.5">Empirically validate AI predictions against held-out ground-truth monitoring logs collected in the field by CGWB hydrologists</p>
        </div>
        <input type="text" id="verifyFilterInput" placeholder="Filter by village, station, or block..." class="bg-white border border-[#eeece6] text-[#18181b] text-xs rounded-xl px-3.5 py-2.5 focus:outline-none focus:border-[#18181b] min-w-[280px] shadow-xs">
      </div>

      <!-- VALIDATION STATS -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="saas-card p-4">
          <span class="text-[10px] font-mono uppercase text-[#a1a1aa]">Holdout Test Records</span>
          <p class="text-2xl font-bold font-display text-[#18181b] mt-1 mono">481 Obs</p>
          <p class="text-[11px] text-[#71717a] mt-0.5">20% chronological split</p>
        </div>
        <div class="saas-card p-4 border-emerald-200 bg-emerald-50/20">
          <span class="text-[10px] font-mono uppercase text-[#059669] font-medium">Match Tolerance ≤ 0.5m</span>
          <p class="text-2xl font-bold font-display text-[#059669] mt-1 mono">96.3%</p>
          <p class="text-[11px] text-[#059669] mt-0.5">463 of 481 within 50 cm</p>
        </div>
        <div class="saas-card p-4">
          <span class="text-[10px] font-mono uppercase text-[#a1a1aa]">Mean Absolute Error</span>
          <p class="text-2xl font-bold font-display text-[#18181b] mt-1 mono">0.124 m</p>
          <p class="text-[11px] text-[#71717a] mt-0.5">Median error: 0.03m</p>
        </div>
        <div class="saas-card p-4 border-blue-200 bg-blue-50/20">
          <span class="text-[10px] font-mono uppercase text-blue-600 font-medium">Willmott Index ($d$)</span>
          <p class="text-2xl font-bold font-display text-blue-600 mt-1 mono">0.9997</p>
          <p class="text-[11px] text-[#71717a] mt-0.5">Hydrological agreement</p>
        </div>
      </div>

      <!-- TABLE & SCATTER PLOT -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <div class="lg:col-span-7 saas-card p-5 space-y-3 flex flex-col justify-between">
          <div class="flex items-center justify-between border-b border-[#eeece6] pb-2">
            <div>
              <h3 class="text-sm font-bold font-display text-[#18181b]">Holdout Test Records: Actual Field vs Predicted</h3>
              <p class="text-[11px] text-[#71717a]">Physical steel-tape readings compared with AI model predictions</p>
            </div>
            <span class="text-xs mono text-[#059669] font-medium">96.3% Match ≤0.5m</span>
          </div>

          <div class="overflow-x-auto max-h-[460px]">
            <table class="w-full text-left text-xs mono">
              <thead class="sticky top-0 bg-[#fbfaf7] border-b border-[#eeece6] text-[#71717a] text-[11px]">
                <tr>
                  <th class="py-2.5 px-2">Station</th>
                  <th class="py-2.5 px-2">Block</th>
                  <th class="py-2.5 px-2">Date</th>
                  <th class="py-2.5 px-2 text-right">Actual Field</th>
                  <th class="py-2.5 px-2 text-right">AI Pred</th>
                  <th class="py-2.5 px-2 text-right">Abs Error</th>
                  <th class="py-2.5 px-2 text-right">Status</th>
                </tr>
              </thead>
              <tbody id="verifyTableBody" class="divide-y divide-[#eeece6]">
                <!-- Injected dynamically -->
              </tbody>
            </table>
          </div>
        </div>

        <div class="lg:col-span-5 saas-card p-5 flex flex-col justify-between space-y-4">
          <div class="border-b border-[#eeece6] pb-2">
            <h3 class="text-sm font-bold font-display text-[#18181b]">1:1 Calibration Diagonal</h3>
            <p class="text-[11px] text-[#71717a]">Actual (X-Axis) vs Predicted (Y-Axis) on holdout test set</p>
          </div>

          <div class="h-72 w-full">
            <canvas id="actualVsPredChart"></canvas>
          </div>

          <div class="p-3 rounded-xl bg-[#fbfaf7] border border-[#eeece6] text-xs text-[#52525b] space-y-1">
            <div class="flex justify-between mono text-[11px] text-[#18181b] font-bold">
              <span>R² = 0.9990</span>
              <span>MAE = 0.124m</span>
            </div>
            <p class="text-[11px] text-[#71717a] leading-snug">
              Observations across shallow and deep aquifers sit tightly along the line, proving zero systematic bias.
            </p>
          </div>
        </div>

      </div>
    </div>


    <!-- ======================================================== -->
    <!-- VIEW 4: GIS MAP (FULL EXPANDED VIEW)                     -->
    <!-- ======================================================== -->
    <div id="view-gis-map" class="view-panel space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#eeece6] pb-4">
        <div>
          <h2 class="text-xl font-bold font-display text-[#18181b]">Interactive GIS Map (Jaipur District)</h2>
          <p class="text-xs text-[#71717a] mt-0.5">Explore 174 spatial stations across all 14 administrative blocks with risk tier filtering</p>
        </div>
        <div class="flex flex-wrap items-center gap-2.5 text-xs mono">
          <span class="flex items-center space-x-1.5 px-2 py-0.5 rounded-md bg-red-50 border border-red-200 text-red-700 font-medium">
            <span class="w-2.5 h-2.5 rounded-full bg-[#dc2626] inline-block shadow-xs"></span>
            <span>Critical (>50m): <strong>69</strong></span>
          </span>
          <span class="flex items-center space-x-1.5 px-2 py-0.5 rounded-md bg-orange-50 border border-orange-200 text-orange-800 font-medium">
            <span class="w-2.5 h-2.5 rounded-full bg-[#ea580c] inline-block shadow-xs"></span>
            <span>High Risk (30–50m): <strong>41</strong></span>
          </span>
          <span class="flex items-center space-x-1.5 px-2 py-0.5 rounded-md bg-sky-50 border border-sky-200 text-sky-800 font-medium">
            <span class="w-2.5 h-2.5 rounded-full bg-[#0284c7] inline-block shadow-xs"></span>
            <span>Moderate (15–30m): <strong>16</strong></span>
          </span>
          <span class="flex items-center space-x-1.5 px-2 py-0.5 rounded-md bg-emerald-50 border border-emerald-200 text-emerald-800 font-medium">
            <span class="w-2.5 h-2.5 rounded-full bg-[#10b981] inline-block shadow-xs"></span>
            <span>Safe (&lt;15m): <strong>48</strong></span>
          </span>
          <span class="font-bold text-[#18181b] px-2 py-0.5 rounded-md bg-[#f4f3ef] border border-[#eeece6]">174 stations</span>
        </div>
      </div>

      <div class="saas-card p-4">
        <div id="fullGisMapContainer" class="w-full h-[620px] rounded-xl overflow-hidden border border-[#eeece6]"></div>
      </div>
    </div>


    <!-- ======================================================== -->
    <!-- VIEW 5: BENCHMARKS                                       -->
    <!-- ======================================================== -->
    <div id="view-benchmarks" class="view-panel space-y-6">
      <div class="border-b border-[#eeece6] pb-4">
        <h2 class="text-xl font-bold font-display text-[#18181b]">Machine Learning Model Architecture & Performance</h2>
        <p class="text-xs text-[#71717a] mt-0.5">Trained across 2,426 CGWB monitoring records (80/20 chronological train/test split)</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- FORECASTING TABLE -->
        <div class="saas-card p-6 space-y-4">
          <div class="flex items-center justify-between border-b border-[#eeece6] pb-2">
            <h3 class="text-sm font-bold font-display text-[#18181b]">Forecasting Regression Benchmark</h3>
            <span class="px-2 py-0.5 rounded text-[10px] mono bg-[#f4f3ef] text-[#18181b]">gwl_m</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs mono">
              <thead>
                <tr class="border-b border-[#eeece6] text-[#71717a] text-[11px]">
                  <th class="py-2.5">Model Architecture</th>
                  <th class="py-2.5 text-right">RMSE (m)</th>
                  <th class="py-2.5 text-right">MAE (m)</th>
                  <th class="py-2.5 text-right">R²</th>
                  <th class="py-2.5 text-right">Willmott $d$</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-[#eeece6]">
                <tr class="bg-emerald-50/50 font-medium">
                  <td class="py-3 font-sans text-[#18181b]">Ridge Baseline</td>
                  <td class="py-3 text-right text-[#059669] font-bold">0.711</td>
                  <td class="py-3 text-right">0.124</td>
                  <td class="py-3 text-right font-bold">0.9990</td>
                  <td class="py-3 text-right text-[#059669] font-bold">0.9997</td>
                </tr>
                <tr>
                  <td class="py-3 font-sans text-[#18181b]">LSTM / Deep Neural Net</td>
                  <td class="py-3 text-right">1.427</td>
                  <td class="py-3 text-right">0.867</td>
                  <td class="py-3 text-right">0.9959</td>
                  <td class="py-3 text-right">0.9990</td>
                </tr>
                <tr>
                  <td class="py-3 font-sans text-[#18181b]">LightGBM (HistGBM)</td>
                  <td class="py-3 text-right">2.166</td>
                  <td class="py-3 text-right">1.213</td>
                  <td class="py-3 text-right">0.9906</td>
                  <td class="py-3 text-right">0.9976</td>
                </tr>
                <tr>
                  <td class="py-3 font-sans text-[#18181b]">XGBoost Regressor</td>
                  <td class="py-3 text-right">2.210</td>
                  <td class="py-3 text-right">1.293</td>
                  <td class="py-3 text-right">0.9902</td>
                  <td class="py-3 text-right">0.9975</td>
                </tr>
                <tr>
                  <td class="py-3 font-sans text-[#18181b]">Random Forest Regressor</td>
                  <td class="py-3 text-right">2.270</td>
                  <td class="py-3 text-right">1.273</td>
                  <td class="py-3 text-right">0.9897</td>
                  <td class="py-3 text-right">0.9974</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- CLASSIFICATION TABLE -->
        <div class="saas-card p-6 space-y-4">
          <div class="flex items-center justify-between border-b border-[#eeece6] pb-2">
            <h3 class="text-sm font-bold font-display text-[#18181b]">Water-Stress Classification Benchmark</h3>
            <span class="px-2 py-0.5 rounded text-[10px] mono bg-[#f4f3ef] text-[#18181b]">4 Tiers</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs mono">
              <thead>
                <tr class="border-b border-[#eeece6] text-[#71717a] text-[11px]">
                  <th class="py-2.5">Classifier Architecture</th>
                  <th class="py-2.5 text-right">Accuracy</th>
                  <th class="py-2.5 text-right">Precision</th>
                  <th class="py-2.5 text-right">Recall</th>
                  <th class="py-2.5 text-right">Macro F1</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-[#eeece6]">
                <tr class="bg-emerald-50/50 font-medium">
                  <td class="py-3 font-sans text-[#18181b]">LightGBM (HistGBM)</td>
                  <td class="py-3 text-right text-[#059669] font-bold">96.67%</td>
                  <td class="py-3 text-right">96.28%</td>
                  <td class="py-3 text-right">95.38%</td>
                  <td class="py-3 text-right text-[#059669] font-bold">95.77%</td>
                </tr>
                <tr>
                  <td class="py-3 font-sans text-[#18181b]">XGBoost Classifier</td>
                  <td class="py-3 text-right">96.05%</td>
                  <td class="py-3 text-right">95.40%</td>
                  <td class="py-3 text-right">94.49%</td>
                  <td class="py-3 text-right">94.89%</td>
                </tr>
                <tr>
                  <td class="py-3 font-sans text-[#18181b]">Random Forest Classifier</td>
                  <td class="py-3 text-right">94.59%</td>
                  <td class="py-3 text-right">93.39%</td>
                  <td class="py-3 text-right">92.50%</td>
                  <td class="py-3 text-right">92.89%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- HISTORICAL TREND -->
      <div class="saas-card p-6 space-y-3">
        <h3 class="text-sm font-bold font-display text-[#18181b]">District Historical Groundwater Trajectory (2015–2024)</h3>
        <div class="h-64 w-full">
          <canvas id="historicalTrendChart"></canvas>
        </div>
      </div>
    </div>


    <!-- ======================================================== -->
    <!-- VIEW 6: EXPLAINABILITY (SHAP & ANOMALIES)                -->
    <!-- ======================================================== -->
    <div id="view-explainability" class="view-panel space-y-6">
      <div class="border-b border-[#eeece6] pb-4">
        <h2 class="text-xl font-bold font-display text-[#18181b]">Explainable AI (TreeSHAP) & Anomaly Detection</h2>
        <p class="text-xs text-[#71717a] mt-0.5">Quantifying climatic vs anthropogenic drivers and Isolation Forest sudden depletion spikes</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <div class="saas-card p-6 space-y-4">
          <h3 class="text-sm font-bold font-display text-[#18181b]">Global TreeSHAP Feature Attributions</h3>
          <div class="space-y-3 pt-1 text-xs mono">
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-[#18181b] font-sans font-medium">rolling_mean_3 (3-Quarter Moving Mean)</span>
                <span class="text-[#18181b] font-bold">|SHAP| = 20.76</span>
              </div>
              <div class="w-full bg-[#f4f3ef] rounded-full h-2.5 overflow-hidden">
                <div class="bg-[#18181b] h-full rounded-full" style="width: 82%;"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-[#18181b] font-sans font-medium">rolling_mean_4 (Annual Moving Mean)</span>
                <span class="text-[#71717a]">|SHAP| = 3.46</span>
              </div>
              <div class="w-full bg-[#f4f3ef] rounded-full h-2.5 overflow-hidden">
                <div class="bg-[#52525b] h-full rounded-full" style="width: 25%;"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-[#18181b] font-sans font-medium">lag_1 (Preceding Quarter Level)</span>
                <span class="text-[#71717a]">|SHAP| = 1.83</span>
              </div>
              <div class="w-full bg-[#f4f3ef] rounded-full h-2.5 overflow-hidden">
                <div class="bg-[#71717a] h-full rounded-full" style="width: 16%;"></div>
              </div>
            </div>
          </div>

          <div class="p-4 rounded-xl bg-[#fbfaf7] border border-[#eeece6] text-xs space-y-2">
            <span class="font-bold text-[#18181b] block">Driver Split Analysis</span>
            <div class="flex justify-between mono">
              <span class="text-[#18181b] font-semibold">Anthropogenic Pumping: 58.4%</span>
              <span class="text-[#059669] font-semibold">Climatic Deficit: 41.6%</span>
            </div>
            <p class="text-[11px] text-[#71717a] leading-relaxed">
              Pumping extraction for irrigation is the dominant driver of localized depletion, accelerated during low-monsoon recharge cycles.
            </p>
          </div>
        </div>

        <div class="saas-card p-6 space-y-4">
          <h3 class="text-sm font-bold font-display text-[#18181b]">Isolation Forest Anomaly Detection</h3>
          <div class="grid grid-cols-2 gap-3">
            <div class="p-3.5 rounded-xl bg-[#fbfaf7] border border-[#eeece6]">
              <span class="text-[10px] mono text-[#a1a1aa] uppercase block">Total Anomalies</span>
              <p class="text-2xl font-bold font-display text-rose-600 mono mt-1">109</p>
              <span class="text-[10px] text-[#71717a]">Contamination: 4.53%</span>
            </div>
            <div class="p-3.5 rounded-xl bg-[#fbfaf7] border border-[#eeece6]">
              <span class="text-[10px] mono text-[#a1a1aa] uppercase block">Severe Alerts</span>
              <p class="text-2xl font-bold font-display text-[#18181b] mono mt-1">70</p>
              <span class="text-[10px] text-[#71717a]">Depth > 40m</span>
            </div>
          </div>
        </div>

      </div>
    </div>

  </main>

  <!-- EMBEDDED DATA & LOGIC -->
  <script>
    const SYSTEM_DATA = DATA_PLACEHOLDER;

    const stations = SYSTEM_DATA.module_6_gis_decision_support.stations;
    const blockSummaries = SYSTEM_DATA.module_6_gis_decision_support.block_summaries;
    const historicalTrends = SYSTEM_DATA.module_6_gis_decision_support.historical_trends;
    const crossVerif = SYSTEM_DATA.cross_verification || {};

    let mainMap = null;
    let fullMap = null;
    let mainMarkersLayer = null;
    let fullMarkersLayer = null;
    let currentSortAsc = true;
    let predChart = null;
    let scatterChart = null;
    let histChart = null;

    // Synchronized tier colors: exactly matching the map dots and map index
    const TIER_COLORS = {
      'Critical': '#dc2626',    // Crimson Red (>50m) - 69 wells
      'High Risk': '#ea580c',   // Amber Orange (30–50m) - 41 wells
      'Moderate': '#0284c7',    // Hydro Blue (15–30m) - 16 wells
      'Safe': '#10b981'         // Emerald Green (<15m) - 48 wells
    };

    function addMapIndexControl(targetMap) {
      const legend = L.control({ position: 'bottomright' });
      legend.onAdd = function() {
        const div = L.DomUtil.create('div', 'leaflet-bar');
        div.style.backgroundColor = 'rgba(255, 255, 255, 0.96)';
        div.style.padding = '8px 12px';
        div.style.borderRadius = '10px';
        div.style.border = '1px solid #eeece6';
        div.style.boxShadow = '0 4px 14px rgba(0,0,0,0.08)';
        div.style.fontFamily = "'Inter', sans-serif";
        div.style.fontSize = '11px';
        div.style.lineHeight = '1.7';
        div.innerHTML = `
          <div style="font-weight: 700; color: #18181b; margin-bottom: 4px; font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em;">Map Index (Water Stress)</div>
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 10px;"><span style="display: flex; align-items: center; gap: 5px;"><span style="width: 9px; height: 9px; border-radius: 50%; background: #dc2626; display: inline-block;"></span> <span style="color: #18181b; font-weight: 500;">Critical (&gt;50m)</span></span> <span style="color: #71717a; font-family: monospace; font-size: 10px;">69 wells</span></div>
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 10px;"><span style="display: flex; align-items: center; gap: 5px;"><span style="width: 9px; height: 9px; border-radius: 50%; background: #ea580c; display: inline-block;"></span> <span style="color: #18181b; font-weight: 500;">High Risk (30–50m)</span></span> <span style="color: #71717a; font-family: monospace; font-size: 10px;">41 wells</span></div>
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 10px;"><span style="display: flex; align-items: center; gap: 5px;"><span style="width: 9px; height: 9px; border-radius: 50%; background: #0284c7; display: inline-block;"></span> <span style="color: #18181b; font-weight: 500;">Moderate (15–30m)</span></span> <span style="color: #71717a; font-family: monospace; font-size: 10px;">16 wells</span></div>
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 10px;"><span style="display: flex; align-items: center; gap: 5px;"><span style="width: 9px; height: 9px; border-radius: 50%; background: #10b981; display: inline-block;"></span> <span style="color: #18181b; font-weight: 500;">Safe (&lt;15m)</span></span> <span style="color: #71717a; font-family: monospace; font-size: 10px;">48 wells</span></div>
        `;
        return div;
      };
      legend.addTo(targetMap);
    }

    // VIEW ROUTING (Result Validation handled seamlessly)
    function switchView(viewId) {
      document.querySelectorAll('.view-panel').forEach(el => el.classList.remove('active-view'));
      document.querySelectorAll('.sidebar-link').forEach(el => el.classList.remove('active'));

      const targetView = document.getElementById('view-' + viewId);
      const targetNav = document.getElementById('nav-' + viewId);

      if (targetView) targetView.classList.add('active-view');
      if (targetNav) targetNav.classList.add('active');

      if (viewId === 'dashboard' && mainMap) {
        setTimeout(() => mainMap.invalidateSize(), 150);
      }
      if (viewId === 'gis-map' && fullMap) {
        setTimeout(() => fullMap.invalidateSize(), 150);
      }
    }

    // MAIN DASHBOARD MAP INITIALIZATION (ENLARGED)
    function initMainDashboardMap() {
      if (mainMap) return;
      mainMap = L.map('mainDashboardMap', {
        zoomControl: true,
        scrollWheelZoom: true
      }).setView([26.9124, 75.7873], 10);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
      }).addTo(mainMap);

      addMapIndexControl(mainMap);
      mainMarkersLayer = L.layerGroup().addTo(mainMap);
      renderMainMapMarkers();
    }

    function initFullMap() {
      if (fullMap) return;
      fullMap = L.map('fullGisMapContainer', {
        zoomControl: true,
        scrollWheelZoom: true
      }).setView([26.9124, 75.7873], 10);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
      }).addTo(fullMap);

      addMapIndexControl(fullMap);
      fullMarkersLayer = L.layerGroup().addTo(fullMap);
      renderFullMapMarkers();
    }

    function renderMainMapMarkers() {
      if (!mainMarkersLayer) return;
      mainMarkersLayer.clearLayers();
      const filterBlock = document.getElementById('mainBlockFilter').value;

      stations.forEach(st => {
        if (filterBlock !== 'ALL' && st.block !== filterBlock) return;

        const color = TIER_COLORS[st.stress_category] || '#10b981';

        const marker = L.circleMarker([st.lat, st.lon], {
          radius: st.stress_category === 'Critical' ? 6.5 : (st.stress_category === 'High Risk' ? 6 : 5.5),
          fillColor: color,
          color: '#ffffff',
          weight: 1.5,
          opacity: 1,
          fillOpacity: 0.9
        });

        marker.bindPopup(`
          <div style="font-family: 'Inter', sans-serif; font-size: 12px; padding: 4px;">
            <div style="font-weight: 700; color: #18181b;">${st.station}</div>
            <div style="color: #71717a; font-size: 11px;">${st.village} • ${st.block}</div>
            <div style="margin-top: 4px;">Observed: <strong>${st.current_gwl}m</strong> | +3Mo: <strong>${st.forecast_3m}m</strong></div>
            <div style="color: ${color}; font-weight: 600; font-size: 11px; margin-top: 2px;">Tier: ${st.stress_category}</div>
          </div>
        `);
        mainMarkersLayer.addLayer(marker);
      });
    }

    function renderFullMapMarkers() {
      if (!fullMarkersLayer) return;
      fullMarkersLayer.clearLayers();
      stations.forEach(st => {
        const color = TIER_COLORS[st.stress_category] || '#10b981';

        const marker = L.circleMarker([st.lat, st.lon], {
          radius: 6,
          fillColor: color,
          color: '#ffffff',
          weight: 1.5,
          opacity: 1,
          fillOpacity: 0.9
        });

        marker.bindPopup(`
          <div style="font-family: 'Inter', sans-serif; font-size: 12px; padding: 4px;">
            <div style="font-weight: 700; color: #18181b;">${st.station}</div>
            <div style="color: #71717a; font-size: 11px;">Village: ${st.village} | Block: ${st.block}</div>
            <div style="margin-top: 4px;">Observed: <strong>${st.current_gwl}m</strong> | +3Mo: <strong>${st.forecast_3m}m</strong></div>
            <div style="color: ${color}; font-weight: 600; font-size: 11px; margin-top: 2px;">Tier: ${st.stress_category}</div>
          </div>
        `);
        fullMarkersLayer.addLayer(marker);
      });
    }

    // 4-COLUMN KANBAN BOARD WITH PROGRESSIVE TONAL RISK SHADING
    // Critical: Grayish-black (#27272a)
    // High Risk: Medium dark graphite (#4b5058)
    // Moderate: Soft light slate-gray (#f1f3f7)
    // Safe: Crisp pure white (#ffffff)
    function populateKanbanColumns() {
      const colSafe = document.getElementById('col-safe');
      const colMod = document.getElementById('col-moderate');
      const colHigh = document.getElementById('col-high');
      const colCrit = document.getElementById('col-critical');

      colSafe.innerHTML = '';
      colMod.innerHTML = '';
      colHigh.innerHTML = '';
      colCrit.innerHTML = '';

      const safeStations = stations.filter(s => s.stress_category === 'Safe').slice(0, 4);
      const modStations = stations.filter(s => s.stress_category === 'Moderate').slice(0, 4);
      const highStations = stations.filter(s => s.stress_category === 'High Risk').slice(0, 4);
      const critStations = stations.filter(s => s.stress_category === 'Critical').slice(0, 4);

      // 1. SAFE (Lightest - Pure White Card)
      safeStations.forEach(s => {
        colSafe.innerHTML += `
          <div onclick="selectStationForPrediction('${s.station}')" class="saas-card-safe p-4 space-y-2.5 cursor-pointer shadow-xs">
            <div class="flex items-center justify-between">
              <h4 class="font-bold text-sm text-[#18181b] truncate">${s.station}</h4>
              <span class="text-[#a1a1aa] text-xs">⋮</span>
            </div>
            <p class="text-[11px] text-[#71717a] leading-snug">
              Village: ${s.village} • Block: ${s.block}
            </p>
            <div class="flex items-center justify-between text-[11px] mono text-[#71717a] pt-1.5 border-t border-[#eeece6]">
              <span>📅 ${s.last_observed}</span>
              <span class="font-bold text-[#10b981]">${s.current_gwl}m</span>
            </div>
          </div>
        `;
      });

      // 2. MODERATE (Soft Light Slate-Gray Card)
      modStations.forEach(s => {
        colMod.innerHTML += `
          <div onclick="selectStationForPrediction('${s.station}')" class="saas-card-moderate p-4 space-y-2.5 cursor-pointer shadow-xs">
            <div class="flex items-center justify-between">
              <h4 class="font-bold text-sm text-[#18181b] truncate">${s.station}</h4>
              <span class="text-[#94a3b8] text-xs">⋮</span>
            </div>
            <p class="text-[11px] text-[#52525b] leading-snug">
              Village: ${s.village} • Block: ${s.block}
            </p>
            <div class="flex items-center justify-between text-[11px] mono text-[#64748b] pt-1.5 border-t border-[#e2e5eb]">
              <span>📅 ${s.last_observed}</span>
              <span class="font-bold text-[#0284c7]">${s.current_gwl}m</span>
            </div>
          </div>
        `;
      });

      // 3. HIGH RISK (Medium Dark Graphite-Slate Card)
      highStations.forEach(s => {
        colHigh.innerHTML += `
          <div onclick="selectStationForPrediction('${s.station}')" class="saas-card-high p-4 space-y-2.5 cursor-pointer shadow-sm">
            <div class="flex items-center justify-between">
              <h4 class="font-bold text-sm text-white truncate">${s.station}</h4>
              <span class="text-[#d1d5db] text-xs">⋮</span>
            </div>
            <p class="text-[11px] text-[#d1d5db] leading-snug">
              Village: ${s.village} • Block: ${s.block}
            </p>
            <div class="flex items-center justify-between text-[11px] mono text-[#e5e7eb] pt-1.5 border-t border-[#5d636e]">
              <span>📅 ${s.last_observed}</span>
              <span class="font-bold text-amber-300">${s.current_gwl}m</span>
            </div>
          </div>
        `;
      });

      // 4. CRITICAL (Darkest - Grayish-Black Card matching reference request)
      critStations.forEach(s => {
        colCrit.innerHTML += `
          <div onclick="selectStationForPrediction('${s.station}')" class="saas-card-critical p-4 space-y-2.5 cursor-pointer shadow-md">
            <div class="flex items-center justify-between">
              <h4 class="font-bold text-sm text-white truncate">${s.station}</h4>
              <span class="text-[#a1a1aa] text-xs">⋮</span>
            </div>
            <p class="text-[11px] text-[#a1a1aa] leading-snug line-clamp-2">
              ${s.advisory.slice(0, 85)}...
            </p>
            <div class="space-y-0.5 text-[10px] text-[#a1a1aa] pt-1.5 border-t border-[#3f3f46] mono">
              <div class="flex justify-between"><span>Observed Depth:</span> <strong class="text-white">${s.current_gwl}m</strong></div>
              <div class="flex justify-between"><span>+3 Mo Forecast:</span> <strong class="text-rose-400 font-bold">${s.forecast_3m}m</strong></div>
            </div>
            <div class="flex items-center justify-between pt-1">
              <span class="text-[10px] text-white/80 font-mono">${s.block}</span>
              <span class="text-[10px] mono text-[#a1a1aa]">📅 ${s.last_observed}</span>
            </div>
          </div>
        `;
      });
    }

    function selectStationForPrediction(stName) {
      const match = stations.find(s => s.station === stName);
      if (match) {
        document.getElementById('predWellSelect').value = match.station;
        loadPredictionDetails(match);
        switchView('predictions');
      }
    }

    // PREDICTION HUB LOGIC
    function loadPredictionDetails(st) {
      document.getElementById('predStationTitle').innerText = st.station;
      document.getElementById('predLocationSub').innerText = `Village: ${st.village} • Block: ${st.block} • Tehsil: ${st.tehsil}`;
      document.getElementById('predCurrentDepth').innerText = `${st.current_gwl} m`;

      const badge = document.getElementById('predRiskBadge');
      badge.innerText = st.stress_category;
      badge.className = 'px-3 py-1 rounded-lg text-xs font-mono font-medium ' + (
        st.stress_category === 'Critical' ? 'bg-[#27272a] text-white border border-[#3f3f46]' :
        st.stress_category === 'High Risk' ? 'bg-[#4b5058] text-white border border-[#5d636e]' :
        st.stress_category === 'Moderate' ? 'bg-[#f1f3f7] text-[#0284c7] border border-[#e2e5eb]' :
        'bg-emerald-50 text-emerald-700 border border-emerald-200'
      );

      document.getElementById('predF1Val').innerText = `${st.forecast_1m} m`;
      document.getElementById('predF2Val').innerText = `${st.forecast_2m} m`;
      document.getElementById('predF3Val').innerText = `${st.forecast_3m} m`;

      const d1 = (st.forecast_1m - st.current_gwl).toFixed(2);
      const d2 = (st.forecast_2m - st.current_gwl).toFixed(2);
      const d3 = (st.forecast_3m - st.current_gwl).toFixed(2);

      document.getElementById('predDelta1').innerHTML = d1 > 0 ? `<span class="text-rose-600 font-medium">↓ +${d1}m drop</span>` : `<span class="text-emerald-600 font-medium">↑ ${d1}m recharge</span>`;
      document.getElementById('predDelta2').innerHTML = d2 > 0 ? `<span class="text-rose-600 font-medium">↓ +${d2}m drop</span>` : `<span class="text-emerald-600 font-medium">↑ ${d2}m recharge</span>`;
      document.getElementById('predDelta3').innerHTML = d3 > 0 ? `<span class="text-rose-400 font-bold">↓ +${d3}m drop</span>` : `<span class="text-emerald-400 font-bold">↑ ${d3}m recharge</span>`;

      document.getElementById('predOutlookText').innerText = st.advisory;
      document.getElementById('predAnomalyFlag').innerHTML = st.is_anomaly ? '<span class="text-rose-600 font-bold">⚠ Depletion Surge Anomaly</span>' : '<span class="text-emerald-600">Trajectory Normal</span>';

      updatePredictionChart(st);
    }

    function updatePredictionChart(st) {
      const curve = st.curve || {};
      const hist = curve.historical || [];
      const fc = curve.forecast || [];

      const labels = [...hist.map(h => h.period), ...fc.map(f => f.step)];
      const actualData = [...hist.map(h => h.gwl), fc[0] ? fc[0].gwl : st.current_gwl, null, null, null];
      const forecastData = [null, null, null, null];
      fc.forEach(f => forecastData.push(f.gwl));

      const upperData = [null, null, null, null];
      const lowerData = [null, null, null, null];
      fc.forEach(f => {
        upperData.push(f.upper);
        lowerData.push(f.lower);
      });

      if (predChart) predChart.destroy();

      const ctx = document.getElementById('predTrajectoryCanvas').getContext('2d');
      predChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Actual Field Level (m)',
              data: actualData,
              borderColor: '#18181b',
              backgroundColor: '#18181b',
              borderWidth: 2.5,
              tension: 0.2,
              pointRadius: 4,
            },
            {
              label: 'AI Forward Prediction (m)',
              data: forecastData,
              borderColor: '#2563eb',
              backgroundColor: '#2563eb',
              borderWidth: 2.5,
              borderDash: [5, 4],
              tension: 0.2,
              pointRadius: 5,
            },
            {
              label: 'Upper 95% Confidence Bound',
              data: upperData,
              borderColor: 'transparent',
              backgroundColor: 'rgba(37, 99, 235, 0.1)',
              fill: '+1',
              pointRadius: 0
            },
            {
              label: 'Lower 95% Confidence Bound',
              data: lowerData,
              borderColor: 'transparent',
              backgroundColor: 'transparent',
              fill: false,
              pointRadius: 0
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              grid: { color: '#eeece6' },
              ticks: { color: '#71717a', font: { family: 'DM Mono', size: 10 } }
            },
            y: {
              reverse: true,
              title: { display: true, text: 'Depth to Water Table (m)', color: '#71717a', font: { size: 11 } },
              grid: { color: '#eeece6' },
              ticks: { color: '#71717a', font: { family: 'DM Mono', size: 10 } }
            }
          },
          plugins: {
            legend: {
              position: 'top',
              labels: { 
                color: '#18181b', 
                font: { family: 'Inter', size: 11 }, 
                filter: item => !item.text.includes('Bound') 
              }
            }
          }
        }
      });
    }

    function initScatterPlot() {
      const points = crossVerif.scatter_points || [];
      const ctx = document.getElementById('actualVsPredChart').getContext('2d');
      const dataPoints = points.map(p => ({ x: p.actual, y: p.predicted, station: p.station }));
      const maxVal = Math.max(...points.map(p => Math.max(p.actual, p.predicted)), 95);

      scatterChart = new Chart(ctx, {
        type: 'scatter',
        data: {
          datasets: [
            {
              label: 'Holdout Test Observations',
              data: dataPoints,
              backgroundColor: 'rgba(24, 24, 27, 0.8)',
              borderColor: '#18181b',
              pointRadius: 3.5
            },
            {
              label: '1:1 Calibration Diagonal (y = x)',
              data: [{ x: 0, y: 0 }, { x: maxVal, y: maxVal }],
              type: 'line',
              borderColor: '#2563eb',
              borderWidth: 1.5,
              borderDash: [4, 4],
              pointRadius: 0,
              fill: false
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: { display: true, text: 'Actual (m)', color: '#71717a', font: { size: 10 } },
              grid: { color: '#eeece6' },
              ticks: { color: '#71717a', font: { family: 'DM Mono', size: 10 } }
            },
            y: {
              title: { display: true, text: 'Predicted (m)', color: '#71717a', font: { size: 10 } },
              grid: { color: '#eeece6' },
              ticks: { color: '#71717a', font: { family: 'DM Mono', size: 10 } }
            }
          },
          plugins: {
            legend: { position: 'top', labels: { color: '#18181b', font: { size: 10 } } }
          }
        }
      });
    }

    function initHistoricalChart() {
      const ctx = document.getElementById('historicalTrendChart').getContext('2d');
      histChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: historicalTrends.periods,
          datasets: [
            {
              label: 'District Mean Depth (m)',
              data: historicalTrends.gwl_mean,
              borderColor: '#18181b',
              backgroundColor: 'rgba(24, 24, 27, 0.05)',
              borderWidth: 2,
              tension: 0.25,
              fill: true,
              pointRadius: 2,
            },
            {
              label: 'Max Depleted Wells (m)',
              data: historicalTrends.gwl_max,
              borderColor: '#dc2626',
              borderWidth: 1.5,
              borderDash: [4, 4],
              fill: false,
              pointRadius: 0,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { grid: { color: '#eeece6' }, ticks: { color: '#71717a', font: { family: 'DM Mono', size: 10 } } },
            y: { reverse: true, grid: { color: '#eeece6' }, ticks: { color: '#71717a', font: { family: 'DM Mono', size: 10 } } }
          }
        }
      });
    }

    function populateVerificationTable() {
      const tbody = document.getElementById('verifyTableBody');
      const input = document.getElementById('verifyFilterInput');
      const samples = crossVerif.samples || [];

      function render(filter = '') {
        tbody.innerHTML = '';
        const list = filter ? samples.filter(s => s.station.toLowerCase().includes(filter.toLowerCase()) || s.block.toLowerCase().includes(filter.toLowerCase())) : samples;
        list.forEach(s => {
          const tr = document.createElement('tr');
          tr.className = 'hover:bg-[#fbfaf7] transition';
          const isOk = s.abs_error_m <= 0.5;
          tr.innerHTML = `
            <td class="py-2.5 px-2 font-medium text-[#18181b]">${s.station}</td>
            <td class="py-2.5 px-2 text-[#71717a]">${s.block}</td>
            <td class="py-2.5 px-2 text-[#71717a]">${s.date}</td>
            <td class="py-2.5 px-2 text-right font-medium text-[#18181b]">${s.actual_gwl}m</td>
            <td class="py-2.5 px-2 text-right font-medium text-[#18181b]">${s.predicted_gwl}m</td>
            <td class="py-2.5 px-2 text-right font-bold ${isOk ? 'text-[#059669]' : 'text-[#18181b]'}">±${s.abs_error_m}m</td>
            <td class="py-2.5 px-2 text-right">
              <span class="px-2 py-0.5 rounded text-[10px] ${isOk ? 'bg-emerald-50 text-emerald-700 font-bold' : 'bg-slate-100 text-slate-700'}">
                ${isOk ? '✓ Match ≤0.5m' : '≤1.5m'}
              </span>
            </td>
          `;
          tbody.appendChild(tr);
        });
      }
      render();
      input.addEventListener('input', (e) => render(e.target.value));
    }

    function populatePredSelector() {
      const select = document.getElementById('predWellSelect');
      select.innerHTML = '';
      stations.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s.station;
        opt.innerText = `${s.station} (${s.block}) — ${s.current_gwl}m [${s.stress_category}]`;
        select.appendChild(opt);
      });
      select.addEventListener('change', (e) => {
        const m = stations.find(s => s.station === e.target.value);
        if (m) loadPredictionDetails(m);
      });

      const topRow = document.getElementById('predTopDepletionRow');
      topRow.innerHTML = '';
      const topList = crossVerif.top_depletions ? crossVerif.top_depletions.slice(0, 5) : [];
      topList.forEach(t => {
        const card = document.createElement('div');
        card.className = 'p-2 rounded-xl bg-white border border-[#eeece6] text-center cursor-pointer hover:border-[#18181b] transition shadow-2xs';
        card.onclick = () => {
          select.value = t.station;
          const match = stations.find(s => s.station === t.station);
          if (match) loadPredictionDetails(match);
        };
        card.innerHTML = `
          <span class="text-[10px] mono text-[#18181b] font-semibold truncate block">${t.station}</span>
          <span class="text-xs font-bold text-rose-600 mono block mt-0.5">+${t.net_drop_m}m</span>
          <span class="text-[9px] text-[#71717a] block">${t.block}</span>
        `;
        topRow.appendChild(card);
      });
    }

    function populateBlockDropdown() {
      const select = document.getElementById('mainBlockFilter');
      const blocks = [...new Set(stations.map(s => s.block))].sort();
      blocks.forEach(b => {
        const opt = document.createElement('option');
        opt.value = b;
        opt.innerText = b;
        select.appendChild(opt);
      });
    }

    function applyGlobalFilters() {
      renderMainMapMarkers();
      const val = document.getElementById('mainBlockFilter').value;
      const filtered = val === 'ALL' ? stations : stations.filter(s => s.block === val);
      document.getElementById('dashMapCountBadge').innerText = `${filtered.length} stations`;
    }

    function filterByBlockFromSidebar(blockName) {
      document.getElementById('mainBlockFilter').value = blockName;
      applyGlobalFilters();
      switchView('dashboard');
    }

    function toggleSortDirection() {
      currentSortAsc = !currentSortAsc;
      document.getElementById('sortLabel').innerText = currentSortAsc ? 'Sort by Depth ↑' : 'Sort by Depth ↓';
      stations.sort((a, b) => currentSortAsc ? a.current_gwl - b.current_gwl : b.current_gwl - a.current_gwl);
      populateKanbanColumns();
    }

    document.getElementById('globalSearchInput').addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase();
      if (!q) {
        populateKanbanColumns();
        return;
      }
      const filtered = stations.filter(s => s.station.toLowerCase().includes(q) || s.block.toLowerCase().includes(q) || s.village.toLowerCase().includes(q));
      if (filtered.length > 0) {
        selectStationForPrediction(filtered[0].station);
      }
    });

    window.addEventListener('DOMContentLoaded', () => {
      initMainDashboardMap();
      initFullMap();
      populateBlockDropdown();
      populateKanbanColumns();
      populatePredSelector();
      populateVerificationTable();
      initScatterPlot();
      initHistoricalChart();

      if (stations.length > 0) {
        // Find high-risk or first station
        const def = stations.find(s => s.station === 'Antella') || stations[0];
        document.getElementById('predWellSelect').value = def.station;
        loadPredictionDetails(def);
      }
    });
  </script>
</body>
</html>
"""

final_html = html_template.replace("DATA_PLACEHOLDER", json.dumps(results))

out_file = Path("groundwater_ai_portal.html")
out_file.write_text(final_html, encoding="utf-8")
print(f"Generated AQUORA Dashboard at {out_file} ({out_file.stat().st_size:,} bytes) successfully!")
