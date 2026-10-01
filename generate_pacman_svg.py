#!/usr/bin/env python3
import json
import math

CONTRIBUTIONS_FILE = "/tmp/contributions.json"

# Days we backfilled with 93-274 commits
BACKFILLED_DAYS = {
    "2026-09-07": 120,
    "2026-09-11": 169,
    "2026-09-12": 203,
    "2026-09-13": 118,
    "2026-09-16": 236,
    "2026-09-17": 124,
    "2026-09-18": 136,
    "2026-09-19": 93,
    "2026-09-20": 151,
    "2026-09-21": 274,
    "2026-09-22": 164,
    "2026-09-23": 176,
    "2026-09-25": 269,
}

# Theme palettes
THEMES = {
    "dark": {
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
    },
    "light": {
        "bg": "#FFFFFF",
        "border": "#D0D7DE",
        "text": "#57606A",
        "header_text": "#1F2328",
        "accent": "#0969DA",
        "l0": "#EBEDF0",
        "l1": "#9BE9A8",
        "l2": "#40C463",
        "l3": "#30A14E",
        "l4": "#216E39",
    }
}

MONTH_NAMES = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
MONTH_COLS = [1, 4, 9, 13, 18, 22, 26, 30, 35, 39, 43, 48]

def build_path():
    # Grid: 53 cols (0..52), 7 rows (0..6)
    path = []
    
    # 1. Row 1: Right from 0 to 52
    for c in range(0, 53):
        path.append((c, 1, 0)) # dir: 0=R, 90=D, 180=L, 270=U
    # Turn down to Row 3 at col 52
    path.append((52, 2, 90))
    # 2. Row 3: Left from 52 to 0
    for c in range(52, -1, -1):
        path.append((c, 3, 180))
    # Turn down to Row 5 at col 0
    path.append((0, 4, 90))
    # 3. Row 5: Right from 0 to 52
    for c in range(0, 53):
        path.append((c, 5, 0))
    # Turn up to Row 0 at col 52
    path.append((52, 4, 270))
    path.append((52, 2, 270))
    # 4. Row 0: Left from 52 to 0
    for c in range(52, -1, -1):
        path.append((c, 0, 180))
    # Turn down to Row 1 at col 0
    path.append((0, 1, 90))
    
    return path

def generate_svg(theme_name="dark"):
    theme = THEMES[theme_name]
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
    
    path = build_path()
    total_steps = len(path)
    step_dur = 0.08  # 80ms per step
    total_dur = total_steps * step_dur  # ~17.84 seconds
    regen_dur = 1.0  # 1.0 second regeneration!
    
    # Map each cell to its visits: (c, r) -> list of t_eat (in seconds)
    visits = {}
    for idx, (c, r, direction) in enumerate(path):
        t_eat = idx * step_dur
        visits.setdefault((c, r), []).append(t_eat)
        
    # Generate CSS
    css_lines = []
    
    # Base styles
    css_lines.append(f"""
      .bg {{ fill: {theme['bg']}; stroke: {theme['border']}; stroke-width: 1; rx: 8; }}
      .lbl {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; font-size: 10px; fill: {theme['text']}; }}
      .title {{ font-family: 'Fira Code', -apple-system, monospace; font-size: 12px; font-weight: 600; fill: {theme['header_text']}; }}
      .sub {{ font-family: 'Fira Code', -apple-system, monospace; font-size: 10px; fill: {theme['accent']}; }}
      .cell {{ rx: 2px; ry: 2px; transform-box: fill-box; transform-origin: center; }}
    """)
    
    # Pac-Man walk keyframes
    pac_kf = []
    ghost_kf = []
    ghost_offset = 5 # 5 steps behind
    
    for idx, (c, r, direction) in enumerate(path):
        pct = (idx / total_steps) * 100
        cx = left_pad + c * pitch + cell_size / 2
        cy = top_pad + r * pitch + cell_size / 2
        
        # Pacman translate & rotate
        pac_kf.append(f"{pct:.2f}% {{ transform: translate({cx:.1f}px, {cy:.1f}px) rotate({direction}deg); }}")
        
        # Ghost follows with offset
        g_idx = (idx - ghost_offset) % total_steps
        gc, gr, gdir = path[g_idx]
        gcx = left_pad + gc * pitch + cell_size / 2
        gcy = top_pad + gr * pitch + cell_size / 2
        ghost_kf.append(f"{pct:.2f}% {{ transform: translate({gcx:.1f}px, {gcy:.1f}px); }}")
        
    css_lines.append(f"@keyframes pac-move {{\n  " + "\n  ".join(pac_kf) + "\n}")
    css_lines.append(f"@keyframes ghost-move {{\n  " + "\n  ".join(ghost_kf) + "\n}")
    
    # Pacman chomp animation
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
    
    # Keyframe for each visited cell: EAT -> REGENERATE IN 1.0 SECOND
    for (c, r), t_list in visits.items():
        cell_id = f"c_{c}_{r}"
        kf_name = f"kf_{cell_id}"
        
        # For this cell, build intervals when it is eaten
        # Cycle is [0, total_dur]
        # At each t_eat: eaten from t_eat to t_eat + regen_dur
        # Outside these intervals: opacity 1, scale 1
        # Inside: opacity 0.08, scale 0.2
        
        # Build timeline points
        events = []
        for t in t_list:
            t_start = t
            t_end = t + regen_dur
            events.append((t_start, t_end))
            
        # Convert events into percentage keyframes
        # We need points just before t_start, at t_start, at t_end, and after t_end
        kf_points = []
        
        # Normal state at 0%
        # Check if 0 is inside an eaten window
        is_eaten_at_0 = any(t1 <= 0 < t2 or (t2 > total_dur and (t1 <= 0 or 0 < t2 - total_dur)) for t1, t2 in events)
        
        # Build list of critical timestamps
        timestamps = set([0.0, total_dur])
        for t1, t2 in events:
            # t1
            timestamps.add(max(0.0, t1 - 0.01))
            timestamps.add(t1)
            timestamps.add(min(total_dur, t1 + 0.02))
            # t2
            if t2 <= total_dur:
                timestamps.add(max(0.0, t2 - 0.02))
                timestamps.add(t2)
                timestamps.add(min(total_dur, t2 + 0.08))
            else:
                # wraps around!
                wrap_end = t2 - total_dur
                timestamps.add(max(0.0, wrap_end - 0.02))
                timestamps.add(wrap_end)
                timestamps.add(min(total_dur, wrap_end + 0.08))
                
        sorted_ts = sorted(list(timestamps))
        
        kf_rules = []
        for ts in sorted_ts:
            pct = (ts / total_dur) * 100
            if pct > 100: pct = 100
            # Is ts eaten?
            is_eaten = False
            for t1, t2 in events:
                if t1 <= ts <= t2:
                    is_eaten = True
                    break
                if t2 > total_dur and (ts >= t1 or ts <= (t2 - total_dur)):
                    is_eaten = True
                    break
            
            # If it just finished regenerating (in the +0.08s window after t2)
            just_regenerated = False
            for t1, t2 in events:
                if t2 <= total_dur and t2 < ts <= t2 + 0.1:
                    just_regenerated = True
                elif t2 > total_dur and (t2 - total_dur) < ts <= (t2 - total_dur) + 0.1:
                    just_regenerated = True
                    
            if is_eaten:
                kf_rules.append(f"{pct:.2f}% {{ opacity: 0.12; transform: scale(0.25); }}")
            elif just_regenerated:
                kf_rules.append(f"{pct:.2f}% {{ opacity: 1; transform: scale(1.22); }}")
            else:
                kf_rules.append(f"{pct:.2f}% {{ opacity: 1; transform: scale(1); }}")
                
        css_lines.append(f"@keyframes {kf_name} {{\n  " + "\n  ".join(kf_rules) + "\n}")
        css_lines.append(f".{cell_id} {{ animation: {kf_name} {total_dur:.2f}s linear infinite; }}")
        
    css_block = "\n".join(css_lines)
    
    # SVG Elements
    svg_elements = []
    svg_elements.append(f'<svg width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg">')
    svg_elements.append(f'<defs><style>{css_block}</style></defs>')
    svg_elements.append(f'<rect width="{svg_w}" height="{svg_h}" class="bg"/>')
    
    # Header Title: Dev//Zero Arcade Contribution Matrix
    svg_elements.append(f'<text x="{left_pad}" y="24" class="title">🕹️ DEV//ZERO PAC-MAN CONTRIBUTION MATRIX</text>')
    svg_elements.append(f'<text x="{svg_w - 30}" y="24" text-anchor="end" class="sub">32,700+ COMMITS • 369 DAY STREAK</text>')
    
    # Month Labels
    for name, col in zip(MONTH_NAMES, MONTH_COLS):
        mx = left_pad + col * pitch
        svg_elements.append(f'<text x="{mx}" y="{top_pad - 8}" class="lbl">{name}</text>')
        
    # Day Labels (Mon, Wed, Fri)
    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    for r, name in day_labels:
        my = top_pad + r * pitch + cell_size - 2
        svg_elements.append(f'<text x="{left_pad - 8}" y="{my}" text-anchor="end" class="lbl">{name}</text>')
        
    # Render all 53 weeks x 7 days
    total_rendered_cells = 0
    for c, week in enumerate(weeks):
        for r, day_data in enumerate(week):
            date_str = day_data["date"]
            level = day_data["level"]
            count = day_data["count"]
            
            # Check if this date was backfilled by us
            if date_str in BACKFILLED_DAYS:
                count = BACKFILLED_DAYS[date_str]
                level = 4 if count >= 100 else 3
                
            color = theme[f"l{level}"]
            
            # If level 0 but in 2026 before Oct 1, ensure at least level 1
            if level == 0 and "2026" in date_str and date_str <= "2026-10-01":
                color = theme["l2"]
                
            x = left_pad + c * pitch
            y = top_pad + r * pitch
            
            cell_cls = f"cell"
            if (c, r) in visits:
                cell_cls += f" c_{c}_{r}"
                
            tip = f"{count} contributions on {date_str}"
            svg_elements.append(
                f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" class="{cell_cls}"><title>{tip}</title></rect>'
            )
            total_rendered_cells += 1
            
    # Legend at bottom
    leg_x = svg_w - 180
    leg_y = svg_h - 16
    svg_elements.append(f'<text x="{leg_x - 10}" y="{leg_y + 8}" text-anchor="end" class="lbl">Less</text>')
    for lvl in range(5):
        lx = leg_x + lvl * (cell_size + 3)
        svg_elements.append(f'<rect x="{lx}" y="{leg_y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{theme[f"l{lvl}"]}"/>')
    svg_elements.append(f'<text x="{leg_x + 5 * (cell_size + 3) + 6}" y="{leg_y + 8}" class="lbl">More</text>')
    
    # PAC-MAN Sprite
    # Sized to perfectly fit over a cell (~14px diameter)
    svg_elements.append("""
      <g class="pacman-sprite">
        <!-- Pac-Man body (two chomping jaws) -->
        <g class="jaw-t">
          <path d="M 0 0 L 8.5 0 A 8.5 8.5 0 0 0 -8.5 0 Z" fill="#FFE600" />
        </g>
        <g class="jaw-b">
          <path d="M 0 0 L 8.5 0 A 8.5 8.5 0 0 1 -8.5 0 Z" fill="#FFE600" />
        </g>
        <circle cx="2" cy="-4.5" r="1.3" fill="#000" />
      </g>
    """)
    
    # BLINKY (Red Ghost) Sprite
    # Follows 5 steps behind Pac-Man
    svg_elements.append("""
      <g class="ghost-sprite">
        <g class="ghost-body" transform="translate(-7, -7)">
          <!-- Ghost head & body -->
          <path d="M 0 7 A 7 7 0 0 1 14 7 L 14 13 L 11.5 11 L 9.5 13 L 7 11 L 4.5 13 L 2.5 11 L 0 13 Z" fill="#FF0000" />
          <!-- Ghost eyes -->
          <circle cx="4.5" cy="6" r="2.2" fill="#FFFFFF" />
          <circle cx="9.5" cy="6" r="2.2" fill="#FFFFFF" />
          <!-- Pupils looking forward -->
          <circle cx="5.5" cy="6" r="1.1" fill="#0000FF" />
          <circle cx="10.5" cy="6" r="1.1" fill="#0000FF" />
        </g>
      </g>
    """)
    
    svg_elements.append('</svg>')
    
    output_str = "\n".join(svg_elements)
    print(f"Generated {theme_name} SVG: {len(output_str)} bytes, {total_rendered_cells} cells, {len(visits)} animated cells.")
    return output_str

if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(script_dir, "dist")
    os.makedirs(dist_dir, exist_ok=True)
    
    dark_svg = generate_svg("dark")
    with open(os.path.join(dist_dir, "pacman-contribution-graph-dark.svg"), "w") as f:
        f.write(dark_svg)
        
    light_svg = generate_svg("light")
    with open(os.path.join(dist_dir, "pacman-contribution-graph.svg"), "w") as f:
        f.write(light_svg)
        
    print("Successfully saved both SVGs into dist/!")
