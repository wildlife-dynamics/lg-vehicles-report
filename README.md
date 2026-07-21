# LG Vehicles Report Workflow

Generates a vehicle movement analysis report for Lion Guardians in the Amboseli ecosystem, sourced from EarthRanger.

## What it produces

The workflow produces, for each tracked vehicle:

- A **Speed Map** &mdash; trajectory segments coloured by a 6-class speed palette (green &rarr; red)
- A **Vehicle Tracks Map** &mdash; uniform blue path overlay on the study area layers
- A **Speed Over Time line chart** &mdash; speed (km/h) plotted against date per vehicle
- **Scalar metric widgets** &mdash; Mean Speed, Min Speed, Max Speed, Distance covered
- A **per-vehicle summary CSV** &mdash; speed and distance statistics (one row per vehicle)
- A **Word document report** (`.docx`) &mdash; cover page plus one section per vehicle
- An **interactive widget dashboard**

## Requirements

- Access to an **EarthRanger** instance with a configured data source
- The **Vehicles** subject group present in your EarthRanger instance
- The **Conservancies** and **Group Ranch Boundaries** spatial features must exist in that EarthRanger instance &mdash; these are fetched live to build the study-area map layers

> Both Word report templates and the organisation logo are downloaded automatically from Dropbox &mdash; no local copies are required.

---

## 1. Load the Workflow

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste this repository's URL into the **Github Link** field, then click **Add Template**:

```
https://github.com/wildlife-dynamics/lg-vehicles-report.git
```

Once added, it appears in the **Workflow Templates** list as **lg-vehicles-report**. Click it to open the workflow configuration form.

> The card may show **Initializing…** briefly while the environment is set up.

---

## 2. Configure the Workflow

### Data Source Connection

Navigate to **Data Sources** and add a new EarthRanger connection. Fill in:

- **Data Source Name** &mdash; a label to identify this connection
- **EarthRanger URL** &mdash; your instance URL (e.g. `your-site.pamdas.org`)
- **EarthRanger Username** and **EarthRanger Password**

> Credentials are not validated at setup time. Any authentication errors will appear when the workflow runs.

### Workflow Details

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional notes about the run (e.g. date range or vehicle group) |

### Time Range

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time of the analysis period |
| Until | End date and time of the analysis period |

All vehicle tracks and metrics are computed within this window.

### Basemap Layers

Two stacked ArcGIS tile layers form the background of every map. Pre-filled with sensible defaults, but the URL, opacity, and max zoom of each layer are editable.

| Layer | Default Opacity | Max Zoom |
|-------|------------------|----------|
| ESRI World Hillshade | `1.0` | `15` |
| ESRI World Street Map | `0.15` | `15` |

### Connect to EarthRanger

Select the EarthRanger connection configured above from the **Connect to EarthRanger** dropdown. The workflow will fetch all observations for the **Vehicles** subject group from this instance.

### Trajectory Filter

Expand **Advanced Configurations** under **Transform relocations to trajectories** to adjust the segment filters. These parameters control how raw GPS fixes are converted into trajectory segments.

| Field | Default | Description |
|-------|---------|-------------|
| Minimum Segment Length (m) | `3` | Discard segments shorter than this distance |
| Maximum Segment Length (m) | `100000` | Discard segments longer than this distance |
| Minimum Segment Duration (s) | `1` | Discard segments shorter than this duration |
| Maximum Segment Duration (s) | `21600` | Discard segments longer than this duration (6 hours) |
| Minimum Segment Speed (km/h) | `3` | Discard segments below this average speed |
| Maximum Segment Speed (km/h) | `150` | Discard segments above this average speed |

### Zoom to Envelope

| Field | Default | Description |
|-------|---------|-------------|
| Expansion Factor | `1.05` | Factor to expand the bounding box when auto-zooming maps (e.g. `1.2` = 20% larger) |

---

## 3. Run the Workflow

Once all parameters are configured, click **Submit**. The runner will:

1. Pull vehicle GPS observations from EarthRanger for the specified time range.
2. Fetch the Conservancies and Group Ranch Boundaries spatial features from EarthRanger to build the study-area map layers.
3. Convert observations to relocations, then build trajectory segments with speed and distance metrics.
4. Classify speed into 6 equal-interval bins and generate the Speed Map.
5. Render the Vehicle Tracks map using a uniform blue path layer.
6. Draw the speed-over-time line chart per vehicle.
7. Compute per-vehicle summary statistics (mean, min, max speed; total distance).
8. Assemble the Word report (cover page + per-vehicle sections) and the dashboard.
9. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

### Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`:

| File | Description |
|------|-------------|
| `vehicle_relocations.geoparquet` | Cleaned GPS fix locations |
| `vehicle_trajectories.geoparquet` | Trajectory segments with speed and distance |
| `<vehicle>_speedmap.html` | Interactive speed map per vehicle |
| `<vehicle>_tracks.html` | Interactive tracks map per vehicle |
| `<vehicle>_speed_line_chart.html` | Interactive speed-over-time line chart |
| `<vehicle>_speedmap.png` | Screenshot of speed map (2&times; resolution) |
| `<vehicle>_tracks.png` | Screenshot of tracks map (2&times; resolution) |
| `<vehicle>_speed_line_chart.png` | Screenshot of speed line chart (2&times; resolution) |
| `<vehicle>_summary.csv` | Speed and distance summary table (one row per vehicle) |
| `cover_page.docx` | Rendered report cover page |
| `<vehicle>.docx` | Per-vehicle report section |
| `overall_report.docx` | Final combined Word report |

---

## More Help

- **Technical Guide:** [technical_guide/lg_vehicles_report_technical_guide.pdf](technical_guide/lg_vehicles_report_technical_guide.pdf) &mdash; pipeline internals and task-by-task reference
- **Issues:** [github.com/wildlife-dynamics/lg-vehicles-report/issues](https://github.com/wildlife-dynamics/lg-vehicles-report/issues)

## Development

This workflow's code (`ecoscope-workflows-vehicles-report-workflow/`) is generated from [`spec.yaml`](spec.yaml) and [`test-cases.yaml`](test-cases.yaml). After editing either file, recompile and commit the generated changes:

```
pixi run --manifest-path pixi.toml --locked bash -c "./dev/recompile.sh --update"
```

## License

[BSD 3-Clause](LICENSE)
