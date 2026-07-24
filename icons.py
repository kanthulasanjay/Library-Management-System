"""
Reusable inline SVG icons + heading helper.

Emoji (📚, 👥, etc.) render inconsistently across OS/browsers — on some
Windows + Chrome/Edge combos without a color-emoji font installed, they
fall back to a broken monochrome glyph. These SVGs render identically
everywhere since they're plain vector markup, not font glyphs.
"""

BOOK_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;">
<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
</svg>"""

USERS_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;">
<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
<circle cx="9" cy="7" r="4"></circle>
<path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
<path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
</svg>"""

OPEN_BOOK_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;">
<path d="M2 4h5a4 4 0 0 1 4 4v12a3 3 0 0 0-3-3H2z"></path>
<path d="M22 4h-5a4 4 0 0 0-4 4v12a3 3 0 0 1 3-3h6z"></path>
</svg>"""

CHECK_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;">
<circle cx="12" cy="12" r="10"></circle>
<path d="m9 12 2 2 4-4"></path>
</svg>"""

CHART_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;">
<line x1="18" y1="20" x2="18" y2="10"></line>
<line x1="12" y1="20" x2="12" y2="4"></line>
<line x1="6" y1="20" x2="6" y2="14"></line>
</svg>"""

LOCK_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;">
<rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
<path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
</svg>"""


LOGOUT_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;">
<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
<polyline points="16 17 21 12 16 7"></polyline>
<line x1="21" y1="12" x2="9" y2="12"></line>
</svg>"""


MONEY_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;">
<line x1="12" y1="1" x2="12" y2="23"></line>
<path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
</svg>"""


def icon_html(icon, size=24, color="#2563EB"):
    """Return a sized, colored SVG string ready to drop into markdown."""
    return icon.format(size=size, color=color)


def icon_heading(text, icon=BOOK_ICON, size=28, color="#2563EB", tag="h1", gradient=True):
    """
    Render an icon + heading side by side, in place of e.g. st.title('📚 My Title').
    Use with: st.markdown(icon_heading("My Title"), unsafe_allow_html=True)
    """
    svg = icon_html(icon, size=size, color=color)

    if gradient:
        text_style = (
            "background:linear-gradient(90deg,#2563EB,#7C3AED);"
            "-webkit-background-clip:text;background-clip:text;"
            "-webkit-text-fill-color:transparent;"
        )
    else:
        text_style = f"color:{color};"

    return f"""
    <div style="display:flex; align-items:center; gap:10px; margin:0 0 4px 0;">
        {svg}
        <{tag} style="margin:0; {text_style}">{text}</{tag}>
    </div>
    """

def kpi_card(col, icon, label, value, accent="blue", color="#2563EB"):
    """
    Render a styled KPI card inside a given st.columns() slot.
    accent: "blue" | "purple" | "amber" | "green" (matches CSS classes)
    Use with: kpi_card(col1, BOOK_ICON, "Total Books", 200, accent="blue")
    """
    with col:
        col.markdown(
            f"""
            <div class="kpi-card kpi-accent-{accent}">
                <div class="kpi-icon">{icon_html(icon, size=26, color=color)}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )