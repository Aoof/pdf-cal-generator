import calendar
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle

calendar.setfirstweekday(calendar.SUNDAY)

months = [(2025, m) for m in range(8, 13)] + [(2026, m) for m in range(1, 7)]

holiday_colors = {
    "Mawlid (Prophet's Birthday)": "#FFD1DC",
    "Isra & Mi'raj (tentative)": "#C1E1C1",
    "Ramadan begins (evening, est.)": "#AEC6CF",
    "Laylat al‑Qadr (est.)": "#FFFACD",
    "Eid al‑Fitr (est.)": "#E6E6FA",
    "Day of Arafah (est.)": "#FFDAB9",
    "Eid al‑Adha (est.)": "#F5DEB3",
    "Islamic New Year (est.)": "#D8BFD8",
    "Ashura (est.)": "#FFB347",
}

holidays = {
    date(2025, 9, 4): ["Mawlid (Prophet's Birthday)"],
    date(2026, 1, 16): ["Isra & Mi'raj (tentative)"],
    date(2026, 2, 17): ["Ramadan begins (evening, est.)"],
    date(2026, 3, 16): ["Laylat al‑Qadr (est.)"],
    date(2026, 3, 20): ["Eid al‑Fitr (est.)"],
    date(2026, 5, 26): ["Day of Arafah (est.)"],
    date(2026, 5, 27): ["Eid al‑Adha (est.)"],
    date(2026, 6, 17): ["Islamic New Year (est.)"],
    date(2026, 6, 25): ["Ashura (est.)"],
}

PAGE_W_IN, PAGE_H_IN = 11, 8.5
DPI = 300

TITLE_FONTSIZE = 14
WEEKDAY_FONTSIZE = 7
DAYNUM_FONTSIZE = 7
FOOTNOTE_FONTSIZE = 6

cols, rows = 7, 6
weekday_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

def draw_month(ax, year, month, footnotes):
    ax.set_axis_off()
    left_margin, right_margin, top_margin, bottom_margin = 0.05, 0.05, 0.12, 0.10
    usable_w = 1 - left_margin - right_margin
    usable_h = 1 - top_margin - bottom_margin
    cell_w = usable_w / cols
    cell_h = usable_h / rows

    # Title
    month_name = calendar.month_name[month]
    title = f"{month_name} {year}"
    ax.text(0.5, 1 - top_margin/2, title, ha="center", va="center",
            fontsize=TITLE_FONTSIZE, weight="bold", transform=ax.transAxes)

    # Weekday headers
    for c in range(cols):
        x0 = left_margin + c * cell_w
        y0 = 1 - top_margin
        ax.text(x0 + cell_w/2, y0 + 0.002, weekday_labels[c],
                ha="center", va="bottom", fontsize=WEEKDAY_FONTSIZE, transform=ax.transAxes)

    month_cal = calendar.monthcalendar(year, month)
    while len(month_cal) < rows:
        month_cal.append([0]*7)

    grid_left, grid_bottom = left_margin, bottom_margin
    grid_right, grid_top = 1 - right_margin, 1 - top_margin

    # Grid lines
    for c in range(cols + 1):
        x = grid_left + c * cell_w
        ax.plot([x, x], [grid_bottom, grid_top], linewidth=0.5, transform=ax.transAxes, color="black")
    for r in range(rows + 1):
        y = grid_bottom + r * cell_h
        ax.plot([grid_left, grid_right], [y, y], linewidth=0.5, transform=ax.transAxes, color="black")

    for r in range(rows):
        for c in range(cols):
            day = month_cal[r][c]
            x0 = grid_left + c * cell_w
            y0 = grid_top - (r + 1) * cell_h
            if day != 0:
                ax.text(x0 + 0.005, y0 + cell_h - 0.005, str(day),
                        ha="left", va="top", fontsize=DAYNUM_FONTSIZE, transform=ax.transAxes)
                d = date(year, month, day)
                if d in holidays:
                    events = holidays[d]
                    colors = [holiday_colors.get(e, "#{:06x}".format(hash(e) & 0xFFFFFF)) for e in events]
                    if len(colors) == 1:
                        rect = Rectangle((x0, y0), cell_w, cell_h,
                                         transform=ax.transAxes, color=colors[0], alpha=0.5, zorder=-1)
                        ax.add_patch(rect)
                    else:
                        split_h = cell_h / len(colors)
                        for i, color in enumerate(colors):
                            rect = Rectangle((x0, y0 + i*split_h), cell_w, split_h,
                                             transform=ax.transAxes, color=color, alpha=0.5, zorder=-1)
                            ax.add_patch(rect)
                    for e, color in zip(events, colors):
                        footnotes.append((f"{day} {month_name}: {e}", color))

out_path = "./CalendarOut.pdf"
with PdfPages(out_path) as pdf:
    for i in range(0, len(months), 4):
        fig, axes = plt.subplots(2, 2, figsize=(PAGE_W_IN, PAGE_H_IN), dpi=DPI)
        footnotes = []
        for j in range(4):
            if i + j < len(months):
                y, m = months[i+j]
                draw_month(axes.flat[j], y, m, footnotes)
            else:
                axes.flat[j].set_axis_off()
        if footnotes:
            # Draw footnotes with color circles
            y0 = 0.02
            line_spacing = 0.015
            for k, (text, color) in enumerate(footnotes):
                y = y0 + k * line_spacing
                fig.patches.append(Rectangle((0.1, y), 0.01, 0.01, transform=fig.transFigure,
                                             color=color, alpha=0.8, zorder=5))
                fig.text(0.115, y, text, ha="left", va="bottom", fontsize=FOOTNOTE_FONTSIZE)
        plt.tight_layout(rect=[0,0.05,1,1])
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
