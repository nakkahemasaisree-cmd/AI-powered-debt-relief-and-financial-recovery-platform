def stat_card(label, value, subtext="", color="#f1f5f9"):
    return f"""
<div class="stat-card">
  <div class="label">{label}</div>
  <div class="value" style="color:{color};">{value}</div>
  {'<div class="subtext">' + subtext + '</div>' if subtext else ''}
</div>"""

def badge(text, level="blue"):
    return f'<span class="badge badge-{level}">{text}</span>'

def progress_bar(percent, label="", caption=""):
    clamped = max(0, min(100, percent))
    color = "#10b981" if clamped < 30 else ("#f59e0b" if clamped < 50 else "#ef4444")
    return f"""
<div>
  {'<div style="font-size:0.85rem;color:#94a3b8;margin-bottom:6px;">' + label + '</div>' if label else ''}
  <div class="progress-bar-wrap">
    <div class="progress-bar-fill" style="width:{clamped}%;background:linear-gradient(90deg,#2563eb,{color});"></div>
  </div>
  <div style="display:flex;justify-content:space-between;margin-top:4px;">
    <span style="font-size:0.75rem;color:#94a3b8;">{caption}</span>
    <span style="font-size:0.85rem;font-weight:700;color:{color};">{clamped:.1f}%</span>
  </div>
</div>"""

def stress_badge(level):
    mapping = {"Low": "green", "Medium": "amber", "High": "red"}
    return badge(level.upper(), mapping.get(level, "blue"))

def risk_badge(category):
    mapping = {"Low": "green", "Medium": "amber", "High": "red"}
    return badge(category.upper(), mapping.get(category, "blue"))

def tip_card(icon, text):
    return f"""
<div class="tip-card">
  <div style="font-size:1.5rem;margin-bottom:6px;">{icon}</div>
  <div style="font-size:0.85rem;color:#94a3b8;line-height:1.5;">{text}</div>
</div>"""

def rights_card(icon, title, description, color="#2563eb"):
    return f"""
<div class="rights-card" style="border-left-color:{color};">
  <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
    <span style="font-size:1.2rem;">{icon}</span>
    <span style="font-weight:700;font-size:0.95rem;color:#f1f5f9;">{title}</span>
  </div>
  <p style="font-size:0.82rem;color:#94a3b8;margin:0;line-height:1.5;">{description}</p>
</div>"""

def currency(amount):
    return f"₹{amount:,.0f}"
