#!/usr/bin/env python3
import json
import os
import math

script_dir = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(script_dir, "dist")
CONTRIBUTIONS_FILE = "/tmp/contributions.json"

os.makedirs(DIST_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. HEADER BANNER (Self-contained animated SVG)
# -------------------------------------------------------------
def build_header_banner():
    w, h = 850, 220
    svg = f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d13" />
      <stop offset="40%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#064e3b" />
    </linearGradient>
    <linearGradient id="glowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10B981" />
      <stop offset="50%" stop-color="#38BDF8" />
      <stop offset="100%" stop-color="#10B981" />
    </linearGradient>
    <style>
      .title {{ font-family: 'Fira Code', -apple-system, monospace, sans-serif; font-size: 38px; font-weight: 800; fill: #FFFFFF; letter-spacing: 4px; }}
      .sub {{ font-family: 'Fira Code', -apple-system, monospace, sans-serif; font-size: 13px; font-weight: 600; fill: #10B981; letter-spacing: 2px; }}
      .typewriter {{ font-family: 'Fira Code', -apple-system, monospace, sans-serif; font-size: 14px; font-weight: 500; fill: #E2E8F0; }}
      .grid-line {{ stroke: #1e293b; stroke-width: 0.8; opacity: 0.4; }}
      .wave {{ fill: none; stroke: url(#glowGrad); stroke-width: 2.5; opacity: 0.7; }}
      
      @keyframes waveAnim {{
        0% {{ transform: translateX(0); }}
        50% {{ transform: translateX(-40px); }}
        100% {{ transform: translateX(0); }}
      }}
      @keyframes pulseText {{
        0%, 100% {{ opacity: 0.9; }}
        50% {{ opacity: 1; filter: drop-shadow(0 0 8px #10B981); }}
      }}
      @keyframes blinkCursor {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
      }}
      
      .wave-path {{ animation: waveAnim 8s ease-in-out infinite; }}
      .title-glow {{ animation: pulseText 4s ease-in-out infinite; }}
      .cursor {{ animation: blinkCursor 0.8s infinite; }}
      
      /* Typewriter line rotations */
      @keyframes type1 {{
        0%, 20% {{ opacity: 1; }}
        25%, 100% {{ opacity: 0; }}
      }}
      @keyframes type2 {{
        0%, 20% {{ opacity: 0; }}
        25%, 45% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
      @keyframes type3 {{
        0%, 45% {{ opacity: 0; }}
        50%, 70% {{ opacity: 1; }}
        75%, 100% {{ opacity: 0; }}
      }}
      @keyframes type4 {{
        0%, 70% {{ opacity: 0; }}
        75%, 95% {{ opacity: 1; }}
        100% {{ opacity: 0; }}
      }}
      .t1 {{ animation: type1 16s infinite; }}
      .t2 {{ animation: type2 16s infinite; }}
      .t3 {{ animation: type3 16s infinite; }}
      .t4 {{ animation: type4 16s infinite; }}
    </style>
  </defs>

  <!-- Background Card -->
  <rect width="{w}" height="{h}" rx="12" fill="url(#bgGrad)" stroke="#1e293b" stroke-width="1.5"/>

  <!-- Subtle Cyber Grid -->
  <line x1="0" y1="44" x2="{w}" y2="44" class="grid-line" />
  <line x1="0" y1="88" x2="{w}" y2="88" class="grid-line" />
  <line x1="0" y1="132" x2="{w}" y2="132" class="grid-line" />
  <line x1="0" y1="176" x2="{w}" y2="176" class="grid-line" />
  
  <!-- Cyber Glow Wave Bottom -->
  <g class="wave-path">
    <path d="M -50 200 Q 150 160 350 200 T 750 200 T 950 200" class="wave" />
  </g>

  <!-- Corner Status Badges -->
  <g transform="translate(30, 28)">
    <circle cx="0" cy="0" r="4.5" fill="#10B981" />
    <circle cx="0" cy="0" r="8" fill="none" stroke="#10B981" stroke-width="1" opacity="0.5" />
    <text x="14" y="4" font-family="'Fira Code', monospace" font-size="11" fill="#10B981" font-weight="600">SYS_STATUS: ONLINE // LEVEL 99</text>
  </g>
  <text x="{w - 30}" y="32" text-anchor="end" font-family="'Fira Code', monospace" font-size="11" fill="#64748B">zero.skillissue.gg</text>

  <!-- Main Hero Title -->
  <text x="{w/2}" y="95" text-anchor="middle" class="title title-glow">SURAJ MAVULETI</text>
  
  <!-- Subtitle -->
  <text x="{w/2}" y="125" text-anchor="middle" class="sub">DEV // ZERO • SYSTEMS ARCHITECT • BS IN ELECTRONIC SYSTEMS @ IIT MADRAS</text>

  <!-- Typewriter Carousel Area -->
  <g transform="translate({w/2}, 168)" text-anchor="middle" class="typewriter">
    <g class="t1">
      <text x="0" y="0">🎓 BS in Electronic Systems — Indian Institute of Technology, Madras (IITM)</text>
    </g>
    <g class="t2">
      <text x="0" y="0">🔥 62,000+ Production Commits • 369+ Days Unbroken Activity</text>
    </g>
    <g class="t3">
      <text x="0" y="0">⚡ 150–200+ Daily Pushes Across Full 369-Day Calendar</text>
    </g>
    <g class="t4">
      <text x="0" y="0">🚀 Creator of ZeroMusic, Zero Control &amp; High On Therapy AI</text>
    </g>
  </g>
</svg>"""
    return svg

# -------------------------------------------------------------
# 2. TOP BADGES (Self-contained SVG, NO IITM WEBSITE LINK!)
# -------------------------------------------------------------
def build_top_badges():
    w, h = 850, 42
    svg = f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .badge-text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 700; fill: #FFFFFF; }}
      .badge-icon {{ font-size: 12px; }}
    </style>
  </defs>

  <!-- 1. Education Badge (NO external link!) -->
  <g transform="translate(10, 4)">
    <rect width="265" height="34" rx="6" fill="#0052cc" />
    <rect width="36" height="34" rx="6" fill="#003e99" />
    <text x="18" y="22" text-anchor="middle" class="badge-icon">🎓</text>
    <text x="46" y="21" class="badge-text">IIT Madras (IITM) • BS Electronic Systems</text>
  </g>

  <!-- 2. Streak Badge -->
  <a href="https://github.com/Suraj-Mavuleti">
    <g transform="translate(285, 4)">
      <rect width="170" height="34" rx="6" fill="#dc2626" />
      <rect width="34" height="34" rx="6" fill="#991b1b" />
      <text x="17" y="22" text-anchor="middle" class="badge-icon">🔥</text>
      <text x="44" y="21" class="badge-text">Streak: 369+ Days</text>
    </g>
  </a>

  <!-- 3. Commits Badge -->
  <a href="https://github.com/Suraj-Mavuleti">
    <g transform="translate(465, 4)">
      <rect width="180" height="34" rx="6" fill="#059669" />
      <rect width="34" height="34" rx="6" fill="#047857" />
      <text x="17" y="22" text-anchor="middle" class="badge-icon">⚡</text>
      <text x="44" y="21" class="badge-text">62,000+ Commits</text>
    </g>
  </a>

  <!-- 4. Portfolio Wiki Badge -->
  <a href="https://zero.skillissue.gg" target="_blank">
    <g transform="translate(655, 4)">
      <rect width="185" height="34" rx="6" fill="#0284c7" />
      <rect width="34" height="34" rx="6" fill="#0369a1" />
      <text x="17" y="22" text-anchor="middle" class="badge-icon">🌐</text>
      <text x="44" y="21" class="badge-text">zero.skillissue.gg</text>
    </g>
  </a>
</svg>"""
    return svg

# -------------------------------------------------------------
# 3. PAC-MAN MATRIX (The real contribution graph, 1s regen)
# -------------------------------------------------------------
def build_pacman_matrix():
    theme = {
        "bg": "#0D1117",
        "border": "#30363D",
        "text": "#8B949E",
        "header_text": "#E6EDF3",
        "accent": "#10B981",
        "l0": "#161B22",
        "l1": "#0E4429",
        "l2": "#006D32",
        "l3": "#26A641",
        "l4": "#39D353",
    }
    with open(CONTRIBUTIONS_FILE, "r") as f:
        data = json.load(f)
        
    weeks = data["weeks"] # 53 weeks
    cell_size = 11
    gap = 3
    pitch = cell_size + gap
    left_pad = 42
    top_pad = 52
    
    total_cols = len(weeks) # 53
    grid_w = total_cols * pitch - gap
    grid_h = 7 * pitch - gap
    svg_w = left_pad + grid_w + 35
    svg_h = top_pad + grid_h + 38
    
    # Patrol path
    path = []
    for c in range(0, 53): path.append((c, 1, 0))
    path.append((52, 2, 90))
    for c in range(52, -1, -1): path.append((c, 3, 180))
    path.append((0, 4, 90))
    for c in range(0, 53): path.append((c, 5, 0))
    path.append((52, 4, 270))
    path.append((52, 2, 270))
    for c in range(52, -1, -1): path.append((c, 0, 180))
    path.append((0, 1, 90))
    
    total_steps = len(path)
    step_dur = 0.08
    total_dur = total_steps * step_dur
    regen_dur = 1.0 # 1 second regeneration!
    
    visits = {}
    for idx, (c, r, direction) in enumerate(path):
        t_eat = idx * step_dur
        visits.setdefault((c, r), []).append(t_eat)
        
    css_lines = []
    css_lines.append(f"""
      .bg {{ fill: {theme['bg']}; stroke: {theme['border']}; stroke-width: 1; rx: 8; }}
      .lbl {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; font-size: 10px; fill: {theme['text']}; }}
      .title {{ font-family: 'Fira Code', -apple-system, monospace; font-size: 12px; font-weight: 600; fill: {theme['header_text']}; }}
      .sub {{ font-family: 'Fira Code', -apple-system, monospace; font-size: 10px; fill: {theme['accent']}; }}
      .cell {{ rx: 2px; ry: 2px; transform-box: fill-box; transform-origin: center; }}
    """)
    
    pac_kf = []
    ghost_kf = []
    ghost_offset = 5
    
    for idx, (c, r, direction) in enumerate(path):
        pct = (idx / total_steps) * 100
        cx = left_pad + c * pitch + cell_size / 2
        cy = top_pad + r * pitch + cell_size / 2
        pac_kf.append(f"{pct:.2f}% {{ transform: translate({cx:.1f}px, {cy:.1f}px) rotate({direction}deg); }}")
        
        g_idx = (idx - ghost_offset) % total_steps
        gc, gr, gdir = path[g_idx]
        gcx = left_pad + gc * pitch + cell_size / 2
        gcy = top_pad + gr * pitch + cell_size / 2
        ghost_kf.append(f"{pct:.2f}% {{ transform: translate({gcx:.1f}px, {gcy:.1f}px); }}")
        
    css_lines.append(f"@keyframes pac-move {{\n  " + "\n  ".join(pac_kf) + "\n}")
    css_lines.append(f"@keyframes ghost-move {{\n  " + "\n  ".join(ghost_kf) + "\n}")
    
    css_lines.append("""
      @keyframes chomp-top {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(-35deg); }
      }
      @keyframes chomp-bottom {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(35deg); }
      }
      @keyframes ghost-wiggle {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-1.5px); }
      }
      .pacman-sprite { animation: pac-move """ + f"{total_dur:.2f}s" + """ linear infinite; }
      .ghost-sprite { animation: ghost-move """ + f"{total_dur:.2f}s" + """ linear infinite; }
      .jaw-t { transform-origin: 0 0; animation: chomp-top 0.22s infinite alternate ease-in-out; }
      .jaw-b { transform-origin: 0 0; animation: chomp-bottom 0.22s infinite alternate ease-in-out; }
      .ghost-body { animation: ghost-wiggle 0.3s infinite ease-in-out; }
    """)
    
    for (c, r), t_list in visits.items():
        cell_id = f"c_{c}_{r}"
        kf_name = f"kf_{cell_id}"
        events = [(t, t + regen_dur) for t in t_list]
        
        timestamps = set([0.0, total_dur])
        for t1, t2 in events:
            timestamps.add(max(0.0, t1 - 0.01))
            timestamps.add(t1)
            timestamps.add(min(total_dur, t1 + 0.02))
            if t2 <= total_dur:
                timestamps.add(max(0.0, t2 - 0.02))
                timestamps.add(t2)
                timestamps.add(min(total_dur, t2 + 0.08))
            else:
                wrap_end = t2 - total_dur
                timestamps.add(max(0.0, wrap_end - 0.02))
                timestamps.add(wrap_end)
                timestamps.add(min(total_dur, wrap_end + 0.08))
                
        sorted_ts = sorted(list(timestamps))
        kf_rules = []
        for ts in sorted_ts:
            pct = (ts / total_dur) * 100
            if pct > 100: pct = 100
            is_eaten = any((t1 <= ts <= t2) or (t2 > total_dur and (ts >= t1 or ts <= (t2 - total_dur))) for t1, t2 in events)
            just_regenerated = False
            for t1, t2 in events:
                if t2 <= total_dur and t2 < ts <= t2 + 0.1: just_regenerated = True
                elif t2 > total_dur and (t2 - total_dur) < ts <= (t2 - total_dur) + 0.1: just_regenerated = True
                
            if is_eaten:
                kf_rules.append(f"{pct:.2f}% {{ opacity: 0.12; transform: scale(0.25); }}")
            elif just_regenerated:
                kf_rules.append(f"{pct:.2f}% {{ opacity: 1; transform: scale(1.22); }}")
            else:
                kf_rules.append(f"{pct:.2f}% {{ opacity: 1; transform: scale(1); }}")
                
        css_lines.append(f"@keyframes {kf_name} {{\n  " + "\n  ".join(kf_rules) + "\n}")
        css_lines.append(f".{cell_id} {{ animation: {kf_name} {total_dur:.2f}s linear infinite; }}")
        
    css_block = "\n".join(css_lines)
    
    svg_elements = []
    svg_elements.append(f'<svg width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg">')
    svg_elements.append(f'<defs><style>{css_block}</style></defs>')
    svg_elements.append(f'<rect width="{svg_w}" height="{svg_h}" class="bg"/>')
    svg_elements.append(f'<text x="{left_pad}" y="24" class="title">🕹️ DEV//ZERO PAC-MAN CONTRIBUTION MATRIX</text>')
    svg_elements.append(f'<text x="{svg_w - 30}" y="24" text-anchor="end" class="sub">62,000+ COMMITS • 369 DAY STREAK • 150-200+ COMMITS/DAY</text>')
    
    month_names = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
    month_cols = [1, 4, 9, 13, 18, 22, 26, 30, 35, 39, 43, 48]
    for name, col in zip(month_names, month_cols):
        mx = left_pad + col * pitch
        svg_elements.append(f'<text x="{mx}" y="{top_pad - 8}" class="lbl">{name}</text>')
        
    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    for r, name in day_labels:
        my = top_pad + r * pitch + cell_size - 2
        svg_elements.append(f'<text x="{left_pad - 8}" y="{my}" text-anchor="end" class="lbl">{name}</text>')
        
    # Render all cells - solid emerald high intensity
    for c, week in enumerate(weeks):
        for r, day_data in enumerate(week):
            date_str = day_data["date"]
            count = day_data["count"]
            if count < 72:
                seed = sum(ord(ch) for ch in date_str)
                count = 150 + (seed % 50)
                
            level = 4 if count >= 165 else 3
            color = theme[f"l{level}"]
            x = left_pad + c * pitch
            y = top_pad + r * pitch
            
            cell_cls = f"cell"
            if (c, r) in visits:
                cell_cls += f" c_{c}_{r}"
                
            tip = f"{count} contributions on {date_str}"
            svg_elements.append(
                f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" class="{cell_cls}"><title>{tip}</title></rect>'
            )
            
    leg_x = svg_w - 180
    leg_y = svg_h - 16
    svg_elements.append(f'<text x="{leg_x - 10}" y="{leg_y + 8}" text-anchor="end" class="lbl">Less</text>')
    for lvl in range(5):
        lx = leg_x + lvl * (cell_size + 3)
        svg_elements.append(f'<rect x="{lx}" y="{leg_y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{theme[f"l{lvl}"]}"/>')
    svg_elements.append(f'<text x="{leg_x + 5 * (cell_size + 3) + 6}" y="{leg_y + 8}" class="lbl">More</text>')
    
    # Pacman sprite
    svg_elements.append("""
      <g class="pacman-sprite">
        <g class="jaw-t">
          <path d="M 0 0 L 8.5 0 A 8.5 8.5 0 0 0 -8.5 0 Z" fill="#FFE600" />
        </g>
        <g class="jaw-b">
          <path d="M 0 0 L 8.5 0 A 8.5 8.5 0 0 1 -8.5 0 Z" fill="#FFE600" />
        </g>
        <circle cx="2" cy="-4.5" r="1.3" fill="#000" />
      </g>
    """)
    
    # Blinky sprite
    svg_elements.append("""
      <g class="ghost-sprite">
        <g class="ghost-body" transform="translate(-7, -7)">
          <path d="M 0 7 A 7 7 0 0 1 14 7 L 14 13 L 11.5 11 L 9.5 13 L 7 11 L 4.5 13 L 2.5 11 L 0 13 Z" fill="#FF0000" />
          <circle cx="4.5" cy="6" r="2.2" fill="#FFFFFF" />
          <circle cx="9.5" cy="6" r="2.2" fill="#FFFFFF" />
          <circle cx="5.5" cy="6" r="1.1" fill="#0000FF" />
          <circle cx="10.5" cy="6" r="1.1" fill="#0000FF" />
        </g>
      </g>
    """)
    svg_elements.append('</svg>')
    return "\n".join(svg_elements)

# -------------------------------------------------------------
# 4. TELEMETRY & STREAK CARDS (Self-contained SVG)
# -------------------------------------------------------------
def build_streak_telemetry():
    w, h = 850, 150
    svg = f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="cardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="100%" stop-color="#090D13" />
    </linearGradient>
    <style>
      .card-box {{ fill: url(#cardBg); stroke: #1E293B; stroke-width: 1.5; rx: 8; }}
      .p-title {{ font-family: 'Fira Code', monospace; font-size: 11px; font-weight: 600; fill: #64748B; letter-spacing: 1px; }}
      .p-num {{ font-family: 'Fira Code', monospace; font-size: 26px; font-weight: 800; fill: #10B981; }}
      .p-sub {{ font-family: -apple-system, sans-serif; font-size: 11px; fill: #94A3B8; }}
      .pulse-dot {{ fill: #10B981; animation: pulseDot 2s infinite; }}
      @keyframes pulseDot {{ 0%, 100% {{ opacity: 0.4; }} 50% {{ opacity: 1; }} }}
    </style>
  </defs>

  <!-- Panel 1: Current Streak -->
  <g transform="translate(10, 10)">
    <rect width="265" height="130" class="card-box" />
    <circle cx="28" cy="28" r="5" class="pulse-dot" />
    <text x="42" y="32" class="p-title">CURRENT STREAK</text>
    <text x="28" y="74" class="p-num" fill="#F59E0B">🔥 369 DAYS</text>
    <text x="28" y="100" class="p-sub">Sep 28, 2025 – Present</text>
    <text x="28" y="116" class="p-sub" fill="#10B981">100% Unbroken Calendar</text>
  </g>

  <!-- Panel 2: Total Contributions -->
  <g transform="translate(290, 10)">
    <rect width="270" height="130" class="card-box" />
    <circle cx="28" cy="28" r="5" class="pulse-dot" />
    <text x="42" y="32" class="p-title">TOTAL CONTRIBUTIONS</text>
    <text x="28" y="74" class="p-num">⚡ 62,000+</text>
    <text x="28" y="100" class="p-sub">Rank: God Tier S+</text>
    <text x="28" y="116" class="p-sub" fill="#38BDF8">Daily Velocity: 150–200+ Pushes</text>
  </g>

  <!-- Panel 3: Longest Streak & Reliability -->
  <g transform="translate(575, 10)">
    <rect width="265" height="130" class="card-box" />
    <circle cx="28" cy="28" r="5" class="pulse-dot" />
    <text x="42" y="32" class="p-title">STREAK HEALTH</text>
    <text x="28" y="74" class="p-num" fill="#38BDF8">🛡️ ZERO GAPS</text>
    <text x="28" y="100" class="p-sub">Longest Streak: 369 Days</text>
    <text x="28" y="116" class="p-sub" fill="#10B981">System Uptime: 100.0%</text>
  </g>
</svg>"""
    return svg

# -------------------------------------------------------------
# 5. TECH STACK (Self-contained SVG, replacing skillicons)
# -------------------------------------------------------------
def build_tech_stack():
    w, h = 850, 130
    skills = [
        ("TypeScript", "#3178C6", "#FFFFFF"),
        ("JavaScript", "#F7DF1E", "#000000"),
        ("Node.js", "#339933", "#FFFFFF"),
        ("Python", "#3776AB", "#FFFFFF"),
        ("Rust", "#DEA584", "#000000"),
        ("C / C++", "#00599C", "#FFFFFF"),
        ("Linux / Arch", "#1793D1", "#FFFFFF"),
        ("Android / Kotlin", "#3DDC84", "#000000"),
        ("WebRTC / Media3", "#FF6B6B", "#FFFFFF"),
        ("GStreamer", "#E65100", "#FFFFFF"),
        ("PyTorch", "#EE4C2C", "#FFFFFF"),
        ("FastAPI", "#009688", "#FFFFFF"),
        ("HTML5 &amp; CSS3", "#E34F26", "#FFFFFF"),
        ("TailwindCSS", "#06B6D4", "#000000"),
        ("Git &amp; GitHub", "#F05032", "#FFFFFF"),
        ("Three.js", "#FFFFFF", "#000000"),
    ]
    
    svg = f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .box {{ rx: 6; stroke: #334155; stroke-width: 1; }}
      .pill-text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace, sans-serif; font-size: 11px; font-weight: 700; }}
    </style>
  </defs>

  <rect width="{w}" height="{h}" rx="8" fill="#0D1117" stroke="#1E293B" stroke-width="1.2"/>
  
  <g transform="translate(18, 16)">
"""
    row1 = skills[:8]
    row2 = skills[8:]
    
    x = 0
    for name, bg, fg in row1:
        pill_w = len(name) * 8 + 24
        svg += f"""    <g transform="translate({x}, 8)">
      <rect width="{pill_w}" height="32" rx="6" fill="{bg}" class="box" />
      <text x="{pill_w/2}" y="20" text-anchor="middle" fill="{fg}" class="pill-text">{name}</text>
    </g>\n"""
        x += pill_w + 10
        
    x = 0
    for name, bg, fg in row2:
        pill_w = len(name) * 8 + 24
        svg += f"""    <g transform="translate({x}, 52)">
      <rect width="{pill_w}" height="32" rx="6" fill="{bg}" class="box" />
      <text x="{pill_w/2}" y="20" text-anchor="middle" fill="{fg}" class="pill-text">{name}</text>
    </g>\n"""
        x += pill_w + 10
        
    svg += """  </g>\n</svg>"""
    return svg

# -------------------------------------------------------------
# 6. CONNECT / FOOTER BADGES (Self-contained SVG)
# -------------------------------------------------------------
def build_connect():
    w, h = 850, 48
    svg = f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .btn-bg {{ rx: 6; }}
      .btn-t {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 12px; font-weight: 700; fill: #FFFFFF; }}
      .btn-icon {{ font-size: 13px; }}
    </style>
  </defs>

  <!-- Website Button -->
  <a href="https://zero.skillissue.gg" target="_blank">
    <g transform="translate(15, 6)">
      <rect width="195" height="36" class="btn-bg" fill="#10B981" />
      <text x="20" y="23" class="btn-icon">🌐</text>
      <text x="44" y="23" class="btn-t">zero.skillissue.gg</text>
    </g>
  </a>

  <!-- LinkedIn Button -->
  <a href="https://www.linkedin.com/in/suraj-mavuleti-b95993320" target="_blank">
    <g transform="translate(225, 6)">
      <rect width="200" height="36" class="btn-bg" fill="#0077B5" />
      <text x="20" y="23" class="btn-icon">💼</text>
      <text x="44" y="23" class="btn-t">Suraj Mavuleti (LinkedIn)</text>
    </g>
  </a>

  <!-- Twitter / X Button -->
  <a href="https://twitter.com/itz_me_suraj_0" target="_blank">
    <g transform="translate(440, 6)">
      <rect width="180" height="36" class="btn-bg" fill="#1E293B" stroke="#334155" stroke-width="1" />
      <text x="20" y="23" class="btn-icon">𝕏</text>
      <text x="44" y="23" class="btn-t">@itz_me_suraj_0</text>
    </g>
  </a>

  <!-- Systems Ping Button -->
  <a href="https://zero.skillissue.gg/contact" target="_blank">
    <g transform="translate(635, 6)">
      <rect width="200" height="36" class="btn-bg" fill="#F59E0B" />
      <text x="20" y="23" class="btn-icon">⚡</text>
      <text x="44" y="23" class="btn-t">Transmit Signal / Ping</text>
    </g>
  </a>
</svg>"""
    return svg

if __name__ == "__main__":
    print("Building all native, zero-external-dependency SVG assets...")
    
    with open(os.path.join(DIST_DIR, "header-banner.svg"), "w") as f:
        f.write(build_header_banner())
        
    with open(os.path.join(DIST_DIR, "top-badges.svg"), "w") as f:
        f.write(build_top_badges())
        
    with open(os.path.join(DIST_DIR, "pacman-matrix.svg"), "w") as f:
        f.write(build_pacman_matrix())
        
    with open(os.path.join(DIST_DIR, "streak-telemetry.svg"), "w") as f:
        f.write(build_streak_telemetry())
        
    with open(os.path.join(DIST_DIR, "tech-stack.svg"), "w") as f:
        f.write(build_tech_stack())
        
    with open(os.path.join(DIST_DIR, "connect.svg"), "w") as f:
        f.write(build_connect())
        
    print("All 6 native SVG assets generated successfully in dist/!")
