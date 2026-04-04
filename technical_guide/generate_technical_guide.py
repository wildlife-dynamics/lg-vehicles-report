"""
Generate the LG Vehicles Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: lg_vehicles_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from datetime import date

OUTPUT_FILE = "lg_vehicles_report_technical_guide.pdf"

# ── Colour palette (same as STE Mapbook) ─────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=24, leading=30, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=12, leading=16, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=14, leading=18, textColor=GREEN_DARK,
                  spaceBefore=16, spaceAfter=5, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=11, leading=15, textColor=GREEN_MID,
                  spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=9.5, leading=13, textColor=SLATE,
                  spaceBefore=7, spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=5, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=13, textColor=SLATE,
                  spaceAfter=2, leftIndent=14, firstLineIndent=-10)
CELL     = _style("Cell", fontSize=8.5, leading=12, textColor=SLATE,
                  spaceAfter=0, spaceBefore=0)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():
    return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)

def p(text, style=BODY):       return Paragraph(text, style)
def h1(text):                  return Paragraph(text, H1)
def h2(text):                  return Paragraph(text, H2)
def h3(text):                  return Paragraph(text, H3)
def sp(n=6):                   return Spacer(1, n)
def bullet(text):              return Paragraph(f"• {text}", BULLET)
def note(text):                return Paragraph(f"<b>Note:</b> {text}", NOTE)
def c(text):                   return Paragraph(text, CELL)


def make_table(data, col_widths):
    """Build a table where every cell value is already a Paragraph (use c())."""
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  GREEN_DARK),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",           (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",    (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 6),
        ("TOPPADDING",     (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


# ── Page template ─────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 7, "LG Vehicles Report — Technical Guide")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build story ───────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="LG Vehicles Report — Technical Guide",
        author="Ecoscope",
    )

    story = []

    # ── Cover ─────────────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("Lion Guardians Vehicles Report", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8),
        hr(),
        p("Vehicle Movement Analysis — Methodology &amp; Calculation Reference", META),
        p(f"Version 1.0  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        hr(),
        PageBreak(),
    ]

    # ── 1. Overview ───────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"), hr(),
        p(
            "The <b>LG Vehicles Report</b> workflow analyses GPS-tracked vehicle movement "
            "in the Amboseli ecosystem for the <b>Lion Guardians</b> programme. "
            "It ingests telemetry from <b>EarthRanger</b> for the <i>Vehicles</i> subject "
            "group, computes speed maps, vehicle tracks, and a speed-over-time line chart "
            "per subject, generates speed and distance statistics, and delivers an "
            "interactive dashboard plus a print-ready Word report."
        ),
        p(
            "The workflow produces two map visualisations (Speed Map and Vehicle Tracks), "
            "a speed line chart, four scalar metric widgets, and a per-subject summary "
            "CSV for each tracked vehicle."
        ),
        note(
            "The grouper is fixed to <code>subject_name</code> — one set of outputs "
            "is produced per individual vehicle."
        ),
    ]

    # ── 2. Dependencies ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Dependencies &amp; Prerequisites"), hr(),

        h2("2.1 EarthRanger Connection"),
        p(
            "All telemetry is fetched from an <b>EarthRanger</b> instance via "
            "<code>set_er_connection</code>. The workflow calls "
            "<code>get_subjectgroup_observations</code> for the subject group "
            "<b>Vehicles</b> with <code>filter: clean</code>, discarding junk-flagged "
            "observations before they reach the pipeline. Subject details and "
            "subject-source details are not included in the raw fetch "
            "(<code>include_details: false</code>)."
        ),

        sp(4), h2("2.2 Grouper"),
        p(
            "The grouper is pre-configured to <code>subject_name</code> and is not "
            "user-selectable. All downstream map, metric, and report tasks iterate "
            "over individual vehicles."
        ),

        sp(6), h2("2.3 Static Geodata Files"),
        p("Three boundary datasets are downloaded from Dropbox and cached locally:"),
        make_table(
            [
                [c("Dataset"),               c("File"),                          c("Purpose")],
                [c("Group Ranch Boundaries"), c("lg_group_ranch_boundaries.gpkg"), c("Community ranch polygons in Amboseli")],
                [c("Conflict Hotspot Areas"), c("lg_conflict_hotspots.gpkg"),      c("Known human–lion conflict hotspot features")],
                [c("Protected Areas"),        c("lg_protected_areas.gpkg"),        c("National parks and reserves")],
            ],
            [4*cm, 5*cm, 7.5*cm],
        ),
        sp(4),
        p(
            "All three files use <code>overwrite_existing: false</code> (3 retries). "
            "After loading, each is reprojected to <b>EPSG:4326</b> and annotated with "
            "its geometry type before layer creation."
        ),

        sp(4), h2("2.4 Word Document Templates"),
        make_table(
            [
                [c("Template file"),             c("Purpose")],
                [c("vehicles_cover_page.docx"),  c("Report cover page — subject count, time range, preparer")],
                [c("custom_vehicle_template.docx"), c("Per-subject section — speed map, tracks map, line chart, summary table")],
            ],
            [6.5*cm, 10*cm],
        ),
        sp(4),
        p("Both templates are downloaded from Dropbox with 2 retries."),

        sp(6), h2("2.5 Base Map Tile Layers"),
        make_table(
            [
                [c("Layer"),                  c("Opacity"), c("Max zoom")],
                [c("ArcGIS World Hillshade"),  c("100 %"),   c("20")],
                [c("ArcGIS World Street Map"), c("15 %"),    c("20")],
            ],
            [10*cm, 2.5*cm, 4*cm],
        ),
        sp(4),
        p(
            "The hillshade provides full-opacity terrain context. "
            "The street map is overlaid at 15 % to show roads and settlement names "
            "without obscuring the vehicle data layers."
        ),
    ]

    # ── 3. Data Ingestion ─────────────────────────────────────────────────────
    story += [
        sp(4), h1("3. Data Ingestion Pipeline"), hr(),

        h2("3.1 Observations → Relocations"),
        p(
            "<code>process_relocations</code> converts raw EarthRanger observations to a "
            "standardised GeoDataFrame. Retained columns:"
        ),
        make_table(
            [
                [c("Column"),                          c("Source field"),            c("Description")],
                [c("groupby_col"),                     c("internal"),                c("Subject identifier for grouping")],
                [c("fixtime"),                         c("observation timestamp"),   c("UTC datetime of the GPS fix")],
                [c("junk_status"),                     c("EarthRanger flag"),        c("True if fix is marked junk")],
                [c("geometry"),                        c("lat/lon"),                 c("Point geometry (WGS 84)")],
                [c("extra__subject__name"),            c("subject.name"),            c("Vehicle display name")],
                [c("extra__subject__subject_subtype"), c("subject.subject_subtype"), c("Subject subtype")],
                [c("extra__subject__sex"),             c("subject.sex"),             c("Subject sex field")],
            ],
            [4.5*cm, 3.8*cm, 8.2*cm],
        ),
        sp(4),
        p("Three bad coordinate pairs are removed unconditionally:"),
        bullet("(180.0, 90.0) — boundary sentinel"),
        bullet("(0.0, 0.0) — null-island artefact"),
        bullet("(1.0, 1.0) — common default / test value"),
        p(
            "Cleaned relocations are persisted as "
            "<code>vehicle_relocations.geoparquet</code>."
        ),

        sp(4), h2("3.2 Relocations → Trajectories"),
        p(
            "<code>relocations_to_trajectory</code> connects consecutive fixes per vehicle "
            "into LineString segments, adding <code>dist_meters</code>, "
            "<code>speed_kmhr</code>, <code>segment_start</code>, and "
            "<code>segment_end</code>. Trajectories are persisted as "
            "<code>vehicle_trajectories.geoparquet</code>."
        ),

        sp(4), h2("3.3 Temporal Index, Speed Classification &amp; Column Renaming"),
        p(
            "<code>add_temporal_index</code> keys the trajectory GeoDataFrame to "
            "<code>segment_start</code>, grouped by <code>subject_name</code>. "
            "<code>apply_classification</code> then bins <code>speed_kmhr</code> into "
            "<b>6 equal-interval classes</b> (output column: <code>speed_bins</code>, "
            "labels to 1 decimal place). Three columns are renamed via "
            "<code>map_columns</code>:"
        ),
        make_table(
            [
                [c("Original column"),        c("Renamed to")],
                [c("extra__name"),            c("subject_name")],
                [c("extra__sex"),             c("subject_sex")],
                [c("extra__subject_subtype"), c("subject_subtype")],
            ],
            [7.5*cm, 9*cm],
        ),
        sp(4),
        p(
            "The renamed GeoDataFrame is split into per-vehicle partitions by "
            "<code>split_groups</code>. All downstream map and metric tasks iterate "
            "over these partitions via <code>mapvalues</code>."
        ),
    ]

    # ── 4. Static Map Layers ──────────────────────────────────────────────────
    story += [
        sp(4), h1("4. Static Map Layers"), hr(),
        p(
            "Four static layers are built once and composited onto every vehicle-level "
            "map to provide spatial context."
        ),

        h2("4.1 Layer Styles"),
        make_table(
            [
                [c("Layer"),               c("Colour (RGB)"),             c("Opacity"), c("Filled"), c("Notes")],
                [c("Group Ranch Boundaries"), c("(169, 169, 169) grey"),   c("55 %"),    c("No"),
                 c("Outline only, line width 4.5")],
                [c("Conflict Hotspots"),   c("(220, 20, 60) crimson"),    c("75 %"),    c("Yes"),
                 c("Point radius 2.55, line width 1.95")],
                [c("Protected Areas"),     c("(77, 102, 0) dark green"),  c("35 %"),    c("Yes"),
                 c("Line width 1.95")],
                [c("Hotspot Text Labels"), c("(20, 20, 20) near-black"),  c("—"),       c("—"),
                 c("Arial, 1 000 m base, 40–75 px clamp, centroid-anchored")],
            ],
            [3.8*cm, 3.8*cm, 2*cm, 1.8*cm, 5.1*cm],
        ),
    ]

    # ── 5. Map Outputs ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("5. Map Outputs — Methodology"), hr(),

        h2("5.1 Speed Map"),
        p(
            "The speed map renders each trajectory segment coloured by its speed bin. "
            "Processing steps before layer creation:"
        ),
        bullet("Sort segments ascending by <code>speed_bins</code> so faster segments render on top."),
        bullet("Apply a custom 6-colour diverging palette to <code>speed_bins</code>:"),
        make_table(
            [
                [c("Bin (slowest → fastest)"), c("Hex colour"), c("Visual tone")],
                [c("1 — slowest"),  c("#1a9850"), c("Dark green")],
                [c("2"),           c("#91cf60"), c("Light green")],
                [c("3"),           c("#d9ef8b"), c("Yellow-green")],
                [c("4"),           c("#fee08b"), c("Yellow")],
                [c("5"),           c("#fc8d59"), c("Orange")],
                [c("6 — fastest"), c("#d73027"), c("Red")],
            ],
            [5*cm, 3*cm, 8.5*cm],
        ),
        sp(4),
        bullet("Format bin labels and speed values to 1 decimal place with km/h unit."),
        bullet(
            "Retain only: <code>dist_meters</code>, <code>speed_bins_colormap</code>, "
            "<code>geometry</code>, <code>speed_kmhr</code>, <code>speed_bins_formatted</code>."
        ),
        p(
            "<code>create_path_layer</code> renders the filtered GeoDataFrame with "
            "width 1.55 px (min 2 px, max 8 px, screen-space), rounded caps and joins, "
            "55 % opacity. Legend title: <i>Speed (km/h)</i>. The layer is combined with "
            "the four static boundary layers. The map is auto-zoomed to the trajectory "
            "extent and persisted as HTML (suffix: <code>speedmap</code>), then "
            "converted to PNG at 2× scale with a 40 s tile-load wait."
        ),

        sp(4), h2("5.2 Vehicle Tracks Map"),
        p(
            "<code>create_path_layer</code> renders all trajectory segments per vehicle "
            "as a uniform blue path:"
        ),
        make_table(
            [
                [c("Property"),     c("Value")],
                [c("Colour"),       c("RGB(0, 0, 255) — blue")],
                [c("Width"),        c("1.55 px, min 2 px, max 8 px (screen-space)")],
                [c("Cap / Join"),   c("Rounded")],
                [c("Opacity"),      c("55 %")],
                [c("Max zoom"),     c("15 (draw_map setting)")],
            ],
            [4.5*cm, 12*cm],
        ),
        sp(4),
        p(
            "The path layer is combined with the four static layers. The view state is "
            "shared with the Speed Map (same envelope and zoom). The map is persisted "
            "as HTML (suffix: <code>tracks</code>) and converted to PNG at 2× scale "
            "with a 40 s tile-load wait."
        ),

        sp(4), h2("5.3 Speed Line Chart"),
        p(
            "<code>draw_line_chart</code> plots vehicle speed over the analysis period "
            "for each subject individually (no category grouping):"
        ),
        make_table(
            [
                [c("Property"),     c("Value")],
                [c("X axis"),       c("segment_start — formatted as YYYY-MM-DD, ticks rotated −45°")],
                [c("Y axis"),       c("speed_kmhr — labelled Speed (km/h), 1 d.p. ticks")],
                [c("Line shape"),   c("Linear (no smoothing)")],
                [c("Background"),   c("#f5f5f5 plot area, #e0e0e0 gridlines")],
                [c("Hover mode"),   c("x unified")],
                [c("Legend"),       c("Hidden")],
            ],
            [3.5*cm, 13*cm],
        ),
        sp(4),
        p(
            "The chart is persisted as HTML (suffix: <code>speed_line_chart</code>) "
            "and converted to PNG via <code>html_to_png</code> (2× scale, 10 ms wait). "
            "Widget title: <i>Vehicle Speed Over Time</i>."
        ),
    ]

    # ── 6. Summary Metrics ────────────────────────────────────────────────────
    story += [
        sp(4), h1("6. Summary Metrics"), hr(),

        h2("6.1 Per-Vehicle Summary Table"),
        p(
            "<code>summarize_df</code> aggregates trajectory data grouped by "
            "<code>subject_name</code>:"
        ),
        make_table(
            [
                [c("Output column"),  c("Source"),      c("Aggregator"), c("Unit"),   c("D.p.")],
                [c("mean_speed"),     c("speed_kmhr"),  c("mean"),       c("km/h"),   c("2")],
                [c("min_speed"),      c("speed_kmhr"),  c("min"),        c("km/h"),   c("2")],
                [c("max_speed"),      c("speed_kmhr"),  c("max"),        c("km/h"),   c("2")],
                [c("total_distance"), c("dist_meters"), c("sum"),        c("m → km"), c("2")],
            ],
            [3.5*cm, 3*cm, 2.5*cm, 2.5*cm, 1.5*cm],
        ),
        sp(4),
        p(
            "<code>add_totals_row</code> appends a <i>Total</i> row across all vehicles. "
            "The table is persisted as CSV."
        ),

        sp(4), h2("6.2 Scalar Dashboard Widgets"),
        p(
            "Four scalar values are derived per group by summing the per-subject "
            "column from the summary table via <code>dataframe_column_sum</code>, "
            "then rounded to 2 d.p. by <code>round_off_values</code>:"
        ),
        make_table(
            [
                [c("Widget title"),    c("Source column"), c("Unit")],
                [c("Mean Speed"),      c("mean_speed"),    c("km/h")],
                [c("Min Speed"),       c("min_speed"),     c("km/h")],
                [c("Max Speed"),       c("max_speed"),     c("km/h")],
                [c("Distance covered"),c("total_distance"),c("km")],
            ],
            [4.5*cm, 4.5*cm, 7.5*cm],
        ),
    ]

    # ── 7. Word Report ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("7. Word Report (.docx)"), hr(),

        h2("7.1 Cover Page"),
        p(
            "<code>create_cl_ctx_cover</code> builds the cover context using the count "
            "of unique subjects (<code>dataframe_column_nunique</code> on "
            "<code>groupby_col</code>), the time range, and <i>Ecoscope</i> as preparer. "
            "<code>create_context_page_lg</code> renders it into "
            "<code>lg_cover_page.docx</code>."
        ),

        sp(4), h2("7.2 Per-Vehicle Sections"),
        p(
            "<code>create_vehicles_grouper_ctx</code> assembles a context dict per "
            "vehicle containing the trajectory DataFrame, summary table CSV, Speed Map "
            "PNG, Tracks Map PNG, and Speed Line Chart PNG. "
            "<code>create_grouper_page</code> renders each section from the "
            "<code>custom_vehicle_template.docx</code> template. "
            "Image boxes: <b>8.28 × 14.15 cm</b>. "
            "<code>validate_images: true</code> catches missing PNGs before rendering."
        ),

        sp(4), h2("7.3 Document Merge"),
        p(
            "<code>merge_cl_files</code> concatenates the cover page and all "
            "per-vehicle sections into a single Word file saved to the results directory."
        ),
    ]

    # ── 8. Interactive Dashboard ───────────────────────────────────────────────
    story += [
        sp(4), h1("8. Interactive Dashboard"), hr(),
        p(
            "<code>gather_dashboard</code> assembles the vehicles dashboard from "
            "seven widget groups:"
        ),
        make_table(
            [
                [c("Widget"),              c("Type"),          c("Source task")],
                [c("Mean Speed"),          c("Single value"),  c("round_mean_speed → total_mean_speed_sv_widget")],
                [c("Min Speed"),           c("Single value"),  c("round_min_speed → total_min_speed_sv_widget")],
                [c("Max Speed"),           c("Single value"),  c("round_max_speed → total_max_speed_sv_widget")],
                [c("Distance covered"),    c("Single value"),  c("round_total_distance → total_distance_sv_widget")],
                [c("Speed Map"),           c("Map"),           c("draw_speedmap → merge_speedmap_widgets")],
                [c("Vehicle Tracks"),      c("Map"),           c("draw_track_map → merge_tracks_widgets")],
                [c("Vehicle Speed Over Time"), c("Line chart"),c("draw_speed_line_chart → grouped_plot_widget_merge")],
            ],
            [4.5*cm, 2.8*cm, 9.2*cm],
        ),
        sp(4),
        note(
            "Single-value and chart widget tasks use <code>skipif: [never]</code> so "
            "the dashboard always assembles, even when some vehicles have no data."
        ),
    ]

    # ── 9. Output Files ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("9. Output Files"), hr(),
        p("All files are written to <code>$ECOSCOPE_WORKFLOWS_RESULTS</code>."),
        make_table(
            [
                [c("File / pattern"),              c("Format"),     c("Content")],
                [c("vehicle_relocations.geoparquet"), c("GeoParquet"), c("Cleaned GPS fix locations")],
                [c("vehicle_trajectories.geoparquet"), c("GeoParquet"), c("Segments with speed_kmhr, dist_meters, speed_bins")],
                [c("<subject>_speedmap.html"),     c("HTML"),       c("Interactive speed map per vehicle")],
                [c("<subject>_tracks.html"),       c("HTML"),       c("Interactive tracks map per vehicle")],
                [c("<subject>_speed_line_chart.html"), c("HTML"),   c("Interactive speed-over-time line chart")],
                [c("<subject>_speedmap.png"),      c("PNG"),        c("2× screenshot of speed map")],
                [c("<subject>_tracks.png"),        c("PNG"),        c("2× screenshot of tracks map")],
                [c("<subject>_speed_line_chart.png"), c("PNG"),     c("2× screenshot of speed line chart")],
                [c("<subject>_summary.csv"),       c("CSV"),        c("Speed and distance summary table with totals row")],
                [c("lg_cover_page.docx"),          c("Word"),       c("Rendered report cover page")],
                [c("<subject>.docx"),              c("Word"),       c("Per-vehicle report section")],
                [c("<merged_report>.docx"),        c("Word"),       c("Final combined Word report")],
            ],
            [5.5*cm, 2.5*cm, 8.5*cm],
        ),
    ]

    # ── 10. Workflow Execution Logic ──────────────────────────────────────────
    story += [
        sp(4), h1("10. Workflow Execution Logic"), hr(),

        h2("10.1 Skip Conditions"),
        p(
            "Two default skip conditions apply to every task "
            "(<code>task-instance-defaults</code>):"
        ),
        bullet(
            "<b>any_is_empty_df</b> — skips the task (and all dependants) when "
            "any input DataFrame is empty, handling vehicles with no fixes gracefully."
        ),
        bullet(
            "<b>any_dependency_skipped</b> — propagates skips downstream automatically."
        ),
        p(
            "Single-value widget and chart widget tasks override this with "
            "<code>skipif: [never]</code> to ensure the dashboard always assembles."
        ),

        sp(4), h2("10.2 Data Flow Summary"),
        make_table(
            [
                [c("Stage"),              c("Tasks")],
                [c("Setup"),              c("ER connection, time range, grouper (subject_name), base maps")],
                [c("Geodata download"),   c("3 boundary files + 2 Word templates from Dropbox")],
                [c("Static layers"),      c("Ranch, hotspot, protected area, hotspot text layers")],
                [c("Telemetry ingest"),   c("Observations → relocations → trajectories → temporal index → speed bins → rename → split")],
                [c("Speed Map branch"),   c("Sort → 6-colour palette → format labels → filter cols → path layer → compose → zoom → HTML → PNG → widget")],
                [c("Tracks branch"),      c("Blue path layer → compose → draw map (zoom 15) → HTML → PNG → widget")],
                [c("Line chart branch"),  c("draw_line_chart → HTML → PNG → plot widget")],
                [c("Metrics branch"),     c("summarize_df → totals row → CSV; 4 scalar widgets (mean/min/max speed, distance)")],
                [c("Report assembly"),    c("Unique subject count → cover page + per-vehicle sections → merge docx")],
                [c("Dashboard"),          c("gather_dashboard combines all 7 widgets")],
            ],
            [4.5*cm, 12*cm],
        ),
    ]

    # ── 11. Software Versions ─────────────────────────────────────────────────
    story += [
        sp(4), h1("11. Software Versions"), hr(),
        make_table(
            [
                [c("Package"),                               c("Version"),    c("Role")],
                [c("ecoscope-workflows-core"),               c("0.22.17.*"),  c("Core task library and workflow engine")],
                [c("ecoscope-workflows-ext-ecoscope"),       c("0.22.17.*"),  c("Spatial analysis tasks (relocations, trajectories, classification)")],
                [c("ecoscope-workflows-ext-custom"),         c("0.0.40.*"),   c("Utility tasks (column mapping, screenshots, line chart)")],
                [c("ecoscope-workflows-ext-ste"),            c("0.0.18.*"),   c("Summary table and totals-row tasks")],
                [c("ecoscope-workflows-ext-mnc"),            c("0.0.7.*"),    c("MNC domain tasks")],
                [c("ecoscope-workflows-ext-icf"),            c("0.0.0.*"),    c("ICF domain tasks")],
                [c("ecoscope-workflows-ext-big-life"),       c("0.0.8.*"),    c("Big Life Foundation domain tasks")],
                [c("ecoscope-workflows-ext-lion-guardians"), c("0.0.6.*"),    c("Lion Guardians Word report rendering tasks")],
            ],
            [6*cm, 2.5*cm, 8*cm],
        ),
        sp(4),
        p(
            "Packages are distributed via the <code>prefix.dev</code> conda channel "
            "and pinned to patch-compatible versions (<code>.*</code> suffix). "
            "The runtime environment is managed by <b>pixi</b>."
        ),
    ]

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
