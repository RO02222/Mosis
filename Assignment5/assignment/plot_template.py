def make_plot_ships_script(priority:str, strategy:str, max_waits:list[float], gen_num:int):
    return (f"""
### priority={priority}, strategy={strategy} ###

set terminal svg size 1200 900

# plot 1. x-axis: ships, y-axis: queuing duration of ship

set out 'plot_ships_{strategy}_{priority}.svg'
set title "Queueing duration (strategy={strategy}, priority={priority})"
set xlabel "Ship #"
set ylabel "Seconds"
#unset xlabel
#unset xtics
set key title "Max Wait"
set key bottom center out
set key horizontal

"""
#  + '\n'.join([
#     f"set style line {i+1} lw 4"
#         for i in range(len(max_waits))
# ])
 + f"""

# set yrange [0:90000]
set xrange [0:{gen_num}]
set style fill solid

plot 'output_{strategy}_{priority}.csv' \\\n    """ + ", \\\n '' ".join([
    f"using 1:{i+2} title '{max_wait}' w boxes ls {i+1}"
        for i, max_wait in enumerate(max_waits)
]))

def make_plot_box_script(priority:str, strategy:str, max_waits:list[float], gen_num:int):
    return (f"""

# plot 2. x-axis: max-wait parameter, y-axis: queueing durations of ships

set out 'plot_box_{strategy}_{priority}.svg'
set title "Queueing duration (strategy={strategy}, priority={priority})"
set style fill solid 0.25 border -1
set style boxplot outliers pointtype 7
set style data boxplot
set key off

set xlabel "Max Wait"
unset xrange
unset yrange

set xtics (""" + ', '.join([ f"'{max_wait}' {i}"
    for i, max_wait in enumerate(max_waits)]) + f""")

plot 'output_{strategy}_{priority}.csv' \\\n    """ + ", \\\n  '' ".join([
    f"using ({i}):{i+2} title '{max_wait}'"
        for i, max_wait in enumerate(max_waits)
]))

def make_plot_frequency_script(priority:str, strategy:str, max_waits:list[float], gen_num:int):
    return (f"""

# plot 3. x-axis: queueing duration interval, y-axis: number of ships

bin_width = 5*60;

set out 'plot_freq_{strategy}_{priority}.svg'
set title "Frequency of queueing durations (strategy={strategy}, priority={priority})"
set boxwidth (bin_width) absolute
set style fill solid 1.0 noborder

set key title "Max Wait"
set key bottom center out
# set key horizontal

set xtics auto
set xrange [0:]
set xlabel "Queueing duration (interval)"
set ylabel "Number of ships"

bin_number(x) = floor(x/bin_width)
rounded(x) = bin_width * ( bin_number(x) + 0.5 )

plot 'output_{strategy}_{priority}.csv' \\\n    """ + ", \\\n '' ".join([
    f"using (rounded(${i+2})):(1) title '{max_wait}' smooth frequency with boxes"
        for i, max_wait in list(enumerate(max_waits))
]))
