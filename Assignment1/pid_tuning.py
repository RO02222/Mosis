from simulate import singleSimulation
import pandas as pd
import os
from animation import animate_gantry_system


def generate_cost_function_params(student_id1, student_id2=0):
    """
    This function is used to generate group-specific cost-function parameters for the Modelica assignment.
    Use it as follows in a Python interpreter:
    > import cost_param
    > cost_param.generate_cost_function_params("<student_id1>","<student_id2>")
    
    :param student_id1: string: Last four digits of the student ID of the first/only student in the group.
    :param student_id2: string: Last four digits of the student ID of the second student in the group.
    :return: Prints the parameters a and b to stdout
    """
    
    combo = (int(student_id2) + int(student_id1)) % 10000
    a = int(str(combo)[:2])
    b = combo % 100
    if a == 0 and b == 0:
        return 1, 1
    elif a == 0:
        return b, b
    elif b == 0:
        return a, a
    else:
        def compute_hcf(x, y):
            while y:
                x, y = y, x % y
            return x

        hcf = compute_hcf(a, b)
        return a/hcf, b/hcf

def calculate_cost(a, b, th_vals, time_vals, x_vals):
    th_max = max(th_vals)
    x_i = 0
    # Find time when gantry displacement passes 9.9m
    for i in range(len(x_vals)):
        if x_vals[i] >= 9.9:
            x_i = i
            break
    t_gantry = time_vals[x_i]
    th_bound = 0.1745
    t_oscillation = t_gantry
    # Find time when theta passes the 10 degree bound for the last time
    for i in range(x_i, len(time_vals)):
        if abs(th_vals[i]) > th_bound:
            t_oscillation = time_vals[i]
    t_task = max(t_gantry, t_oscillation)
    cost = a*th_max + b*t_task
    return cost

def simulate_pid_loop():
    # Iterate through all values of kp & kd and save simulation result in csv files
    os.mkdir("pid_results")
    for kp in range(1, 41):
        for kd in range(10, 501, 10):
            vars = singleSimulation("pendulum/Assignment1.pid_control_loop", "pid_control_loop", {"pid1.kp": kp, "pid1.kd": kd})
            df = pd.DataFrame({"time": vars["time"],
                               "displacement gantry": vars["plant1.x"],
                               "angular displacement": vars["plant1.th"]})
            df.to_csv("pid_results/kp_" + str(kp) + "_kd_" + str(kd) + ".csv")

def tune_pid(a: int, b: int):
    # If simulation results already present, skip to calculating cost
    if not os.path.exists("pid_results"):
        simulate_pid_loop()
    kp_best = 0
    kd_best = 0
    min_cost = float("+inf")
    for kp in range(1, 41):
        for kd in range(10, 501, 10):
            df = pd.read_csv("pid_results/kp_" + str(kp) + "_kd_" + str(kd) + ".csv")
            th_vals = df["angular displacement"].to_list()
            time_vals = df["time"].to_list()
            x_vals = df["displacement gantry"].to_list()
            cost = calculate_cost(a, b, th_vals, time_vals, x_vals)
            # If cost of simulation smaller than all previous ones, consider it the best one
            if cost < min_cost:
                min_cost = cost
                kp_best = kp
                kd_best = kd
    return kp_best, kd_best


if __name__ == "__main__":
    a, b = generate_cost_function_params("1127", "0395")
    print(a, b)
    kp, kd = tune_pid(a, b)
    print(kp, kd)
    df = pd.read_csv("pid_results/kp_" + str(kp) + "_kd_" + str(kd) + ".csv")
    x_vals = df["displacement gantry"]
    th_vals = df["angular displacement"]
    animate_gantry_system(x_vals[:100], th_vals[:100], 1, 100)
