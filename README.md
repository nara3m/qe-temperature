# Temperature Dashboard Generator

This Python script reads multiple `.tsv` files containing temperature data and generates interactive Bokeh dashboards. The dashboards allow users to explore temperature trends over time for two Pumps: TURBO1 and TURBO2.

## Features

- Reads all `.tsv` files in the current directory.
- Cleans and filters data, removing the 10 lowest values for each dataset.
- Creates a time series scatter plot for each file.
- Adds interactive date range sliders for zooming into specific time periods.
- Groups plots into TURBO1 and TURBO2 based on the filename or column name.
- Saves five combined dashboards (each showing one plot from TURBO1 and one from TURBO2) as HTML files.

## File Requirements

- Each `.tsv` file must:
  - Be tab-delimited.
  - Contain exactly two columns: one with dates and one with numeric values.
  - Include "TURBO1" or "TURBO2" in the filename or column name to be properly grouped.

## Output

- Generates up to 5 HTML dashboards: `temperature_dashboard_row_1.html`, ..., `temperature_dashboard_row_5.html`.
- Each dashboard contains a pair of plots (one TURBO1 and one TURBO2) with an interactive date range slider.

## How to Use

1. Place your `.tsv` files in the script's directory.
2. Run the script:
   ```bash
   python bokeh.py
   ```
3. Open the generated HTML files in a browser to view the dashboards.

## Dependencies

- `pandas`
- `bokeh`

Install required packages with:
```bash
pip install pandas bokeh
```

## Notes

- Files with missing or non-numeric data will be skipped.
- The script expects at least 10 data points after removing outliers.
