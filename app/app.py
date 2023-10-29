"""
Author: Jianyin Roachell
MPI: Department of Geoanthropology
update: Oct. 29, 2023
"""



import pandas as pd
from shiny import App, Inputs, Outputs, Session, render, ui
from shiny.types import FileInfo
from matplotlib import pyplot as plt
from helpers import *
import io

series_may, ts_may = ews_exe()

app_ui = ui.page_fluid(
    # TTILE PANEL
    ui.panel_title("Sentinel v0.0.1"),
    ui.markdown("""Computing predictions of a DL classifier:
The method `apply_classifier()` applies a deep learning classifier (a TensorFlow Model) to a segment of the time series data, specified using tmin and tmax. The prediction (a vector of probabilites for each class) is then saved into the attribute dl_preds, which is a pandas DataFrame.

Let's see this in action. We will import one of the classifiers that was trained in Bury et al. (PNAS, 2021). These are saved in the ewstools Github repository under /saved_classifiers for convenience. These classifiers were trained to predict the following classes:
> 0	fold bifurcation

> 1	Hopf bifurcation

> 2	transcritical bifurcation

> 3	null
"""),


    # INPUTS
    # Add a file input component to upload data

    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_file("file1", "Choose CSV File", accept=[".csv"], multiple=False),
            ui.input_checkbox("header", "Header", True),
            width=5,
        ),
        ui.panel_main(
            ui.output_ui("contents"),
        ),
    ),

    # OUTPUTS
    ui.output_text_verbatim("txt"),
    ui.output_plot("plot"),
    ui.output_plot("plot2"),
    ui.output_table("ml_preds")
)

def server(input, output, session):
    # Define a callback to read and process the uploaded file
    @output
    @render.ui
    def contents():
        if input.file1() is None:
            return "Please upload a csv file"
        f: list[FileInfo] = input.file1()
        df = pd.read_csv(f[0]["datapath"], header=0 if input.header() else None)
        return ui.HTML(df.to_html(classes="table table-striped"))

    @output
    @render.text()
    def txt():
        return f"n*2 is {input.n()}"

    @output
    @render.plot
    def plot():
        return series_may.plot()

    @output
    @render.plot
    def plot2():
        return ts_may.state[['state', 'smoothing']].plot()

    @output
    @render.table
    def ml_preds():
        return ts_may.dl_preds



# Create the Shiny app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
