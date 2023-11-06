"""
Author: Jianyin Roachell
MPI: Department of Geoanthropology
update: Oct. 29, 2023
"""

import pandas as pd
from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from shiny.types import FileInfo
from matplotlib import pyplot as plt
from helpers import *
import io
import webbrowser
import shinyswatch

series_may, ts_may = get_example_df()


app_ui = ui.page_fluid(

    ui.include_css("/Users/johann/Documents/PROJECTS/SENTINEL/app/stylesheet.css"),

    # Help buttons
    #ui.div(
    #    ui.input_action_button("help", "help_button_1", class_="btn btn-link"),
    # #ui.button("Help Button 2", id="help_button_2", class_="btn btn-link"),
    #    class_="btn-group",
    #    style={"margin-left": "10px", "margin-top": "10px"}),
    # TTILE PANEL
    ui.panel_title("SENTINEL v0.0.1"),
    ui.markdown("""Systematic Engagement with Time-series and Intelligent Early Learning"""),

    # INPUTS
    # Add a file input component to upload data
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_file("file1", "Choose CSV File", accept=[".csv"], multiple=False),
            #ui.input_action_button("example_button", "Ex. Data", class_="btn-success"),
            # ui.panel_conditional(
            #     "input.file1",
            ui.input_action_button("treat_dat", "Detrend", class_="btn-success"),
            #                     ),
            ui.input_checkbox("header", "Header", True),
            ui.input_select("model_name", "Select Model", choices = model_names),
            ui.input_action_button("model_button", "Model", class_ = "btn-success"),
            width=4.5,
        ),
        ui.panel_main(

            # OUTPUTS
            ui.markdown("""### Data"""),
            ui.output_text("value"),
            ui.output_table("contents"),
            ui.panel_conditional(
                "input.treat_dat",
                ui.output_table("treat_dat"),
            ),
            #ui.markdown("""### Classifier Results"""),
            ui.panel_conditional(
                "input.model_button",
                ui.markdown("""### Classifier Results"""), ui.output_table("ml_preds"),
            ),
            ui.output_text_verbatim("txt"),
            ui.output_plot("plot"),
            ui.output_plot("plot2"),

        ),
    ),



)

def server(input, output, session):
    # Define a callback to read and process the uploaded file
    # Define a callback to open the hyperlinks when help buttons are clicked
    df = reactive.Value(pd.DataFrame()) # initiate reactive df
    df_post = reactive.Value()
    @output
    @render.ui
    def contents():
        if input.file1() is None:
            #print("Please upload a csv file OR click example data")
            return ui.HTML(ts_may.state[['state', 'smoothing']].head().to_html(classes="table table-striped"))
        elif input.file1():
            f: list[FileInfo] = input.file1()
            df.set(pd.read_csv(f[0]["datapath"], header=0 if input.header() else None)) # suppose to instantiate the new file
            return ui.HTML(df.get().head().to_html(classes="table table-striped"))
        elif input.treat_dat():
            f: list[FileInfo] = input.file1()
            df.set(pd.read_csv(f[0]["datapath"], header=0 if input.header() else None)) # suppose to instantiate the new file
            df_post = transform_dat(df.get())
            return ui.HTML(df_post.get().head().to_html(classes="table table-striped"))

    @output
    @render.text
    def value():
        return "You choose: " + str(input.model_name())

    @output
    @render.plot
    def plot():
        if input.file1() is None:
            return series_may.plot()
        else:
            df.get()[['y','x']].plot()

    @output
    @render.plot
    def plot2():
        if input.file1() is None:
            return ts_may.state[['state', 'smoothing']].plot()
        else:
            return df_post.get().state[['state', 'smoothing']].plot()

    @output
    @render.ui
    @reactive.event(input.treat_dat, ignore_none=False)
    def treat_dat():
        df_post.set(transform_dat(df.get()))
        return ui.HTML(df_post.get().state[['state', 'smoothing']].head().to_html(classes="table table-striped"))

    @output
    @render.table
    @reactive.event(input.model_button, ignore_none=False)
    def ml_preds():
        if input.file1() is None:
            preds = get_model(str(input.model_name()), ts_may)
            return preds
        else:
            preds = get_model(str(input.model_name()), df_post.get())
            return preds



# Create the Shiny app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
