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


def ews_exe():
    series_may = simulate_may(tmax=500, dt=0.01, h=[0.15,0.28]).iloc[::100]
    ts_may = ewstools.TimeSeries(series_may['x'], transition=420)
    ts_may.detrend(method='Lowess', span=0.2)
    ts_may.state[['state','smoothing']].plot()
    classifier_path = '/Users/johann/Documents/PROJECTS/sentinelpy/saved_classifiers/bury_pnas_21/len500/best_model_1_1_len500.pkl'
    classifier = load_model(classifier_path)
    ts_may.apply_classifier(classifier, tmin=0, tmax=400)
    return series_may, ts_may
