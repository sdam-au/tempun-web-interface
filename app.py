import gradio as gr
import pandas as pd
import tempun
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io
from datetime import datetime

def get_columns(file):
    """Extract column names from uploaded file"""
    if file is None:
        return gr.Dropdown(choices=[]), gr.Dropdown(choices=[])
    
    try:
        if file.name.endswith('.csv'):
            data = pd.read_csv(file.name)
        elif file.name.endswith(('.xlsx', '.xls')):
            data = pd.read_excel(file.name)
        else:
            return gr.Dropdown(choices=[]), gr.Dropdown(choices=[])
        
        columns = list(data.columns)
        return (
            gr.Dropdown(choices=columns, value=columns[0] if columns else None),
            gr.Dropdown(choices=columns, value=columns[1] if len(columns) > 1 else None)
        )
    except Exception as e:
        return gr.Dropdown(choices=[]), gr.Dropdown(choices=[])

def process_data(file, start_col, end_col, start_year, end_year, bin_size, size_simulations, 
                 plot_title, x_label, y_label, legend_label):
    """Process uploaded data and generate Monte Carlo simulation"""
    
    # 1) Read in data
    if file is None:
        return None, None, None, "Error: Please upload a file"
    
    try:
        if file.name.endswith('.csv'):
            data = pd.read_csv(file.name)
        elif file.name.endswith(('.xlsx', '.xls')):
            data = pd.read_excel(file.name)
        else:
            return None, None, None, "Error: Please upload CSV or Excel file"
    except Exception as e:
        return None, None, None, f"Error reading file: {str(e)}"
    
    # Check if columns exist
    if start_col not in data.columns or end_col not in data.columns:
        return None, None, None, f"Error: Columns '{start_col}' or '{end_col}' not found in data"
    
    # 2) Choose data with non-null dates
    data_dated = data[(data[start_col].notnull()) | (data[end_col].notnull())].copy()
    
    if len(data_dated) == 0:
        return None, None, None, f"Error: No records with {start_col} or {end_col} dates found"
    
    # 3) Generate random dates
    data_dated["random_dates"] = data_dated.apply(
        lambda row: tempun.model_date(
            row[start_col], row[end_col], size=int(size_simulations)
        ), 
        axis=1
    )
    
    # 4) Bin them
    data_dated_complete_simulations = tempun.timeblocks_from_randoms(
        data_dated["random_dates"], [int(start_year), int(end_year), int(bin_size)]
    )
    
    # 5) Visualise
    plt.style.use("seaborn-v0_8-white")
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['font.size'] = 10
    plt.rcParams['font.family'] = 'Calibri'
    
    fig, ax = plt.subplots(figsize=(14, 6), tight_layout=True)
    
    # Use custom legend label with record count
    final_legend_label = f"{legend_label} (n={len(data_dated)})"
    
    tempun.plot_timeblocks_data(
        data_dated_complete_simulations, 
        ax=ax, 
        color="blue", 
        label=final_legend_label
    )
    
    ax.set_xlabel(x_label, weight="bold")
    ax.set_ylabel(y_label, weight="bold")
    ax.set_title(plot_title)
    ax.legend(title="Data source", title_fontsize="large", 
             bbox_to_anchor=(1, 1), loc='upper right')
    
    # Save plot to file
    plot_path = "simulation_plot.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6) Prepare data download
    data_output_path = "processed_data.csv"
    data_dated.to_csv(data_output_path, index=False)
    
    # 7) Generate script with comprehensive metadata
    script_content = f"""# Monte Carlo Simulation Script
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# PROVENANCE INFORMATION
# =====================
# Generated with: tempun package
# Package URL: https://pypi.org/project/tempun/
# Package DOI: https://zenodo.org/records/8179346
# Package author: Vojtěch Kaše
#
# Dashboard: Tempun Web Interface
# Dashboard URL: https://huggingface.co/spaces/petrifiedvoices/tempun
# Dashboard author: Petra Heřmánková (ORCID: 0000-0002-6349-0540)
#
# SIMULATION PARAMETERS
# ====================
# Input file: {file.name if file else 'N/A'}
# Start date column: {start_col}
# End date column: {end_col}
# Temporal range: {int(start_year)} - {int(end_year)} CE
# Bin size: {int(bin_size)} years
# Simulation size: {int(size_simulations)} iterations per record
# Records processed: {len(data_dated)}
#
# VISUALISATION PARAMETERS
# ========================
# Title: {plot_title}
# X-axis label: {x_label}
# Y-axis label: {y_label}
# Legend label: {legend_label}
#
# CITATION
# ========
# If you use this script in your research, please cite:
# - Kaše, V. (2022). tempun (Version v0.2.2) [Software]. Zenodo. 
#   https://zenodo.org/records/8179346
# - Heřmánková, P. (2025). Tempun Web Interface [Software]. DOI TBA.
#   https://huggingface.co/spaces/petrifiedvoices/tempun

import pandas as pd
import tempun
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Read data
data = pd.read_csv('your_data.csv')

# Filter dated records
data_dated = data[(data["{start_col}"].notnull()) | (data["{end_col}"].notnull())].copy()

print(f"Processing {{len(data_dated)}} records with temporal information")

# Generate random dates (Monte Carlo simulation)
data_dated["random_dates"] = data_dated.apply(
    lambda row: tempun.model_date(
        row["{start_col}"], row["{end_col}"], size={int(size_simulations)}
    ), 
    axis=1
)

# Create time blocks
data_dated_complete_simulations = tempun.timeblocks_from_randoms(
    data_dated["random_dates"], [{int(start_year)}, {int(end_year)}, {int(bin_size)}]
)

# Visualisation
plt.style.use("seaborn-v0_8-white")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'Calibri'

fig, ax = plt.subplots(figsize=(14, 6), tight_layout=True)

tempun.plot_timeblocks_data(
    data_dated_complete_simulations, 
    ax=ax, 
    color="blue", 
    label="{legend_label} (n={{len(data_dated)}})"
)

ax.set_xlabel("{x_label}", weight="bold")
ax.set_ylabel("{y_label}", weight="bold")
ax.set_title("{plot_title}")
ax.legend(title="Data source", title_fontsize="large", 
         bbox_to_anchor=(1, 1), loc='upper right')

plt.savefig('simulation_output.png', dpi=300, bbox_inches='tight')
plt.show()

print("Simulation complete!")
"""
    
    script_path = "simulation_script.py"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    return plot_path, data_output_path, script_path, f"Success! Processed {len(data_dated)} records."

# Create Gradio interface
with gr.Blocks(title="Tempun Monte Carlo Simulation") as demo:
    gr.Markdown("# Monte Carlo Simulation for Historical Datasets with a High Level of Uncertainty")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            ## Instructions
            1. Upload a CSV or Excel file containing temporal data.
            2. Select which columns contain start dates (*i.e., not_before*) and end dates (*i.e., not_after*).
            3. Set temporal parameters for your visualisation (start year, end year, bin size), *for example, 300, 800, 25 for data from 300 to 800 CE, binned by 25 years*.
            4. Set simulation size (number of random dates per record), *for example, 100 or 1000, depending on your needs*.
            5. Customise visualisation labels (optional).
            6. Click "Run Simulation".
            7. Download the visualisation, processed data with random dates, and a Python script with attached metadata for reproducible and responsible practice!
            8. Repeat the steps above if you would like to adjust your visualisation.
            9. Don't forget to cite us in your research (see below).
            """)
        
        with gr.Column():
            gr.Markdown("""
            ## Required Data Format
            Your file should contain at least two columns with temporal information (start and end dates). Dates have to be formatted as years (YYYY), with BCE years as negative values and CE years as positive values.
            
            This page is not intended for the processing of large datasets. If you need to process a large dataset (more than 5,000 records), download our demo and run it locally on your computer. See https://github.com/sdam-au/tempun_demo or read Kaše, Vojtěch, Adéla Sobotkova, and Petra Heřmánková. 2023. 'Modeling Temporal Uncertainty in Historical Datasets'. *Proceedings of the Computational Humanities Research Conference 2023*, 413–25. https://ceur-ws.org/Vol-3558/paper5123.pdf
            """)
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="Upload your CSV or Excel file", file_types=[".csv", ".xlsx", ".xls"])
            
            gr.Markdown("### Data Configuration")
            with gr.Row():
                start_col = gr.Dropdown(label="Start Date Column (not_before)", choices=[], allow_custom_value=True)
                end_col = gr.Dropdown(label="End Date Column (not_after)", choices=[], allow_custom_value=True)
            
            gr.Markdown("### Simulation Parameters")
            with gr.Row():
                start_year = gr.Number(label="Start Year", value=300)
                end_year = gr.Number(label="End Year", value=800)
            
            with gr.Row():
                bin_size = gr.Number(label="Bin Size (years)", value=25)
                size_simulations = gr.Number(label="Simulation Size", value=1000)
            
            gr.Markdown("### Visualisation Labels")
            plot_title = gr.Textbox(
                label="Plot Title", 
                value="Monte Carlo Simulation of Temporal Distribution"
            )
            x_label = gr.Textbox(label="X-axis Label", value="Year")
            y_label = gr.Textbox(label="Y-axis Label", value="Count")
            legend_label = gr.Textbox(label="Legend Label", value="Data")
            
            submit_btn = gr.Button("Run Simulation", variant="primary")
        
        with gr.Column(scale=1):
            status_output = gr.Textbox(label="Status")
            plot_output = gr.Image(label="Visualisation")
            
            with gr.Row():
                data_download = gr.File(label="Download Processed Data")
                script_download = gr.File(label="Download Script")
    
    # Update dropdowns when file is uploaded
    file_input.change(
        fn=get_columns,
        inputs=[file_input],
        outputs=[start_col, end_col]
    )
    
    submit_btn.click(
        fn=process_data,
        inputs=[file_input, start_col, end_col, start_year, end_year, bin_size, size_simulations,
                plot_title, x_label, y_label, legend_label],
        outputs=[plot_output, data_download, script_download, status_output]
    )
    
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            ## Tool Information
            - Built with [tempun](https://pypi.org/project/tempun/) package by Vojtěch Kaše ([DOI: 10.5281/zenodo.8179346](https://zenodo.org/records/8179346))
            - Dashboard by Petra Heřmánková ([ORCID: 0000-0002-6349-0540](https://orcid.org/0000-0002-6349-0540))
            """)
        
        with gr.Column():
            gr.Markdown("""
            ## Citation
            If you use this tool in your research, please cite:
            - Kaše, V. (2022). *tempun* (Version v0.2.2) [Software]. Zenodo. https://zenodo.org/records/8179346
            - Heřmánková, P. (2025). *Tempun Web Interface* [Software]. DOI TBA.
            """)

demo.launch()