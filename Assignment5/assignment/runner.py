import os
from pypdevs.simulator import Simulator
from plot_template import make_plot_ships_script, make_plot_box_script, make_plot_frequency_script
# from system_solution import * # Teacher's solution
from system import *
## Parameters ##
gen_num = 500 # how many ships to generate
# How often to generate a ship (on average)
gen_rate = 1/60/4 # once every 4 minutes
# Ship size will be sampled uniformly from the following list.
gen_types = [1,1,2] # ship size '1' twice as likely to be generated as ship size '2'
# Load balancer...
priorities = {
    # you can outcomment one of these lines to reduce the number of experiments (useful for debugging):
    PRIORITIZE_BIGGER_SHIPS: "bigger",
    # PRIORITIZE_SMALLER_SHIPS: "smaller",
}
strategies = {
    # you can outcomment one of these lines to reduce the number of experiments (useful for debugging):
    STRATEGY_ROUND_ROBIN: "roundrobin",
    # STRATEGY_FILL_ER_UP: "fillerup",
}
# The number of locks and their capacities
lock_capacities=[3,2] # two locks, of capacity 3 and 2
# The different parameters to try for max_wait_duration
max_wait_durations = [ 0.0+i*120.0 for i in range(1) ] # all these values will be attempted
# max_wait_durations = [ 15.0 ] # <-- uncomment if you only want to run an experiment with this value (useful for debugging)
# How long does it take for a ship to pass through a lock
passthrough_duration = 60.0*15 # 15 minutes
outdir = "assignment_output"
plots_ships = []
plots_box = []
plots_freq = []
os.makedirs(outdir, exist_ok=True)
# try all combinations of priorities and strategies (4 total)
for priority in priorities:
    for strategy in strategies:
        values = []
        # and in each experiment, try a bunch of different values for the 'max_wait_duration' parameter:
        for max_wait_duration in max_wait_durations:
            print("Run simulation:", priorities[priority], strategies[strategy], "max_wait =",max_wait_duration)
            sys = LockQueueingSystem(
                # See system.py for explanation of these values:
                seed=0,
                gen_num=gen_num,
                gen_rate=gen_rate,
                gen_types=gen_types,
                load_balancer_strategy=strategy,
                lock_capacities=lock_capacities,
                priority=priority,
                max_wait_duration=max_wait_duration,
                passthrough_duration=passthrough_duration,
            )
            sim = Simulator(sys)
            sim.setClassicDEVS()
            # sim.setVerbose() # <-- uncomment to see what's going on
            sim.simulate()
            # all the ships that made it through
            ships = sys.sink.state.ships
            values.append([ship.queueing_duration for ship in ships])
        # Write out all the ship queueuing durations for every 'max_wait_duration' parameter
        #  for every ship, we write a line:
        #    <ship_num>, time_max_wait0, time_max_wait1, time_max_wait2, ... time_max_wait10
        filename = f'{outdir}/output_{strategies[strategy]}_{priorities[priority]}.csv'
        with open(filename, 'w') as f:
            try:
                for i in range(gen_num):
                    f.write("%s" % i)
                    for j in range(len(values)):
                        f.write(", %5f" % (values[j][i]))
                    f.write("\n")
            except IndexError as e:
                raise Exception("There was an IndexError, meaning that fewer ships have made it to the sink than expected.\nYour model is not (yet) correct.") from e
        # Generate gnuplot code:
        for f, col in [(make_plot_ships_script, plots_ships), (make_plot_box_script, plots_box), (make_plot_frequency_script, plots_freq)]:
            col.append(f(
                priority=priorities[priority],
                strategy=strategies[strategy],
                max_waits=max_wait_durations,
                gen_num=gen_num,
            ))

# Finally, write out a single gnuplot script that plots everything
with open(f'{outdir}/plot.gnuplot', 'w') as f:
    # first plot the ships
    f.write('\n\n'.join(plots_ships))
    # then do the box plots
    f.write('\n\n'.join(plots_box))
    f.write('\n\n'.join(plots_freq))