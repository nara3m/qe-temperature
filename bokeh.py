import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, DateRangeSlider, CustomJS
from bokeh.plotting import figure, output_file, save
from glob import glob
import os

# === SETTINGS ===
tsv_files = glob("*.tsv")
dashboard_output = "temperature_dashboard_sorted.html"

turbo1_plots = []
turbo2_plots = []

# Sort the files based on the filename to ensure related plots are grouped
tsv_files.sort()

for tsv_file in tsv_files:
    df = pd.read_csv(tsv_file, sep='\t')

    if df.shape[1] != 2:
        print(f"⚠️ Skipping {tsv_file}: Expected exactly 2 columns.")
        continue

    date_col = df.columns[0]
    value_col = df.columns[1]

    # === CLEAN DATA ===
    df = df[[date_col, value_col]].copy()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
    df.dropna(subset=[date_col, value_col], inplace=True)

    # === REMOVE BOTTOM 10 Y-VALUES ===
    if len(df) > 10:
        df = df.sort_values(by=value_col, ascending=True).iloc[10:]
    else:
        print(f"⚠️ Skipping {tsv_file}: Not enough data after outlier removal.")
        continue

    # === PLOT TITLE FROM FILE NAME ===
    plot_title = df.columns[1]
    print(plot_title)

    # === BOKEH DATA SOURCE ===
    source = ColumnDataSource(data={
        'x': df[date_col],
        'y': df[value_col],
    })

    # === MAIN PLOT ===
    p = figure(
        width=600,
        height=250,
        x_axis_type="datetime",
        tools="xpan,xwheel_zoom,reset,save",
        toolbar_location="above",
        title=plot_title
    )

    p.scatter('x', 'y', source=source, size=2, color="navy", alpha=0.5)
    p.xaxis.axis_label = date_col
    # p.yaxis.axis_label = value_col

    # === DATE RANGE SELECTOR ===
    min_date = df[date_col].min()
    max_date = df[date_col].max()

    date_range_slider = DateRangeSlider(
        start=min_date,
        end=max_date,
        value=(min_date, max_date),
        step=1,
        title="Select Date Range"
    )

    # Custom callback to filter the data based on date range selection
    callback = CustomJS(args=dict(source=source, date_range_slider=date_range_slider), code="""
        var data = source.data;
        var start_date = date_range_slider.value[0];
        var end_date = date_range_slider.value[1];
        var x = data['x'];
        var y = data['y'];

        var new_x = [];
        var new_y = [];

        for (var i = 0; i < x.length; i++) {
            if (x[i] >= start_date && x[i] <= end_date) {
                new_x.push(x[i]);
                new_y.push(y[i]);
            }
        }

        // Update the source with filtered data
        data['x'] = new_x;
        data['y'] = new_y;
        source.change.emit();
    """)

    date_range_slider.js_on_change('value', callback)

    # === GROUPING BY TURBO1 / TURBO2 ===
    if "TURBO1" in plot_title.upper():
        turbo1_plots.append(column(p, date_range_slider))
    elif "TURBO2" in plot_title.upper():
        turbo2_plots.append(column(p, date_range_slider))
    else:
        print(f"⚠️ Skipping {tsv_file}: Filename must include 'TURBO1' or 'TURBO2' for grouping.")
        continue

# === SAVE TO 5 SEPARATE HTML DASHBOARDS ===
for i in range(5):
    # Take the i-th plot from turbo1_plots and turbo2_plots
    dashboard_layout = row(turbo1_plots[i], turbo2_plots[i])

    # Define the output file name for each dashboard
    dashboard_output = f"temperature_dashboard_row_{i+1}.html"

    # Output the file
    output_file(dashboard_output)
    save(dashboard_layout)

    print(f"✅ Dashboard for row {i+1} created: {dashboard_output}")

