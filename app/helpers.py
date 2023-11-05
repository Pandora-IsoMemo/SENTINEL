"""
Author: Jianyin Roachell
MPI: Department of Geoanthropology
update: Oct. 29, 2023
"""
# operations of TS analysis
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR) # comment out to see TensorFlow warnings
from tensorflow.keras.models import load_model
import ewstools
from ewstools.models import simulate_may, simulate_rosen_mac
from typing import List

model_names = {
"saved_classifiers/bury_pnas_21/len500/best_model_1_1_len500.pkl": "Model Lens500",
"saved_classifiers/bury_pnas_21/len1500/best_model_1_1_len1500.pkl":"Model Lens1500"
}


def get_example_df():
    series_may = simulate_may(tmax=500, dt=0.01, h=[0.15,0.28]).iloc[::100]
    ts_may = ewstools.TimeSeries(series_may['x'], transition=420)
    ts_may.detrend(method='Lowess', span=0.2)
    ts_may.state[['state','smoothing']].plot()
    return series_may, ts_may

def get_model(model_path, ts_may):
    classifier = load_model(model_path)
    ts_may.apply_classifier(classifier, tmin=0, tmax=400)
    return ts_may.dl_preds




# UI helper
from shiny.types import NavSetArg


def nav_controls(prefix: str) -> List[NavSetArg]:
    return [
        ui.nav("a", prefix + ": tab a content"),
        ui.nav("b", prefix + ": tab b content"),
        ui.nav("c", prefix + ": tab c content"),
        ui.nav_spacer(),
        ui.nav_menu(
            "Links",
            ui.nav_control(
                ui.a(
                    "Shiny",
                    href="https://shiny.posit.co/py/",
                    target="_blank",
                )
            ),
            "----",
            "Plain text",
            "----",
            ui.nav_control(
                ui.a(
                    "Posit",
                    href="https://posit.co",
                    target="_blank",
                )
            ),
            align="right",
        ),
    ]

