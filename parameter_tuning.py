from simulate import singleSimulation
import pandas as pd
import numpy as np
from matplotlib import pyplot
import os

def compute_vals(param: str):
    # If results already generated return
    if os.path.exists(param + "_results"):
        return
    os.mkdir(param + "_results")
    data = pd.read_csv("calibration_data_" + param[0] + "_" + param[1] + ".csv", names=["measured"])
    data = data.drop(index=data.index[0], axis=0)
    # For each possible value simulate & store alongside measured values
    for val in np.arange(0, 5, 0.01).round(2):
        if val == 0:
            continue
        values = singleSimulation("pendulum/Assignment1.calibration_" + str(param), "calibration_" + str(param), {param: val})
        if param == "dp":
            th_vals = values["th"]
        else:
            th_vals = values["x"]
        simulation_df = pd.DataFrame(th_vals, columns=["simulation"])
        data["simulation"] = simulation_df["simulation"]
        data.to_csv(param + "_results/" + param + "_" + str(val))

def sum_of_squared_errors(param: str):
    # Loops through all values of param and calculates
    # sum of squared errors for each one
    # => smallest one is considered best
    os.chdir(param + "_results")
    min = float("+inf")
    best = 0.01
    for val in np.arange(0, 5, 0.01).round(2):
        if val == 0:
            continue
        df = pd.read_csv(param + "_" + str(val))
        measured = np.array(df["measured"].tolist())
        simulation = np.array(df["simulation"].tolist())
        sum = np.sum((measured-simulation)**2)
        if sum < min:
            best = val
            min = sum
    os.chdir("..")
    return best

def calibrate_dp():
    compute_vals("dp")
    return sum_of_squared_errors("dp")

def calibrate_dc():
    compute_vals("dc")
    return sum_of_squared_errors("dc")

if __name__ == "__main__":
    time_vals = np.arange(0, 20, 0.004).round(3)
    dc = calibrate_dc()
    dc_df = pd.read_csv("dc_results/dc_" + str(dc))
    dc_measured = dc_df["measured"].to_list()[:5000]
    dc_simulated = dc_df["simulation"].to_list()[:5000]
    pyplot.plot(time_vals, dc_measured, label="Measured", color="blue")
    pyplot.plot(time_vals, dc_simulated, label="Simulated", color="red")
    pyplot.xlabel("Time")
    pyplot.ylabel("Values")
    pyplot.legend()
    pyplot.show()
    dp = calibrate_dp()
    dp_df = pd.read_csv("dp_results/dp_" + str(dp))
    dp_measured = dp_df["measured"].to_list()[:5000]
    dp_simulated = dp_df["simulation"].to_list()[:5000]
    pyplot.plot(time_vals, dp_measured, label="Measured", color="blue")
    pyplot.plot(time_vals, dp_simulated, label="Simulated", color="red")
    pyplot.xlabel("Time")
    pyplot.ylabel("Values")
    pyplot.legend()
    pyplot.show()
    print(round(dp, 2))
    print(round(dc,2))