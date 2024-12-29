
### priority=bigger, strategy=roundrobin ###

set terminal svg size 1200 900

# plot 1. x-axis: ships, y-axis: queuing duration of ship

set out 'plot_ships_roundrobin_bigger.svg'
set title "Queueing duration (strategy=roundrobin, priority=bigger)"
set xlabel "Ship #"
set ylabel "Seconds"
#unset xlabel
#unset xtics
set key title "Max Wait"
set key bottom center out
set key horizontal



# set yrange [0:90000]
set xrange [0:500]
set style fill solid

plot 'output_roundrobin_bigger.csv' \
    using 1:2 title '0.0' w boxes ls 1, \
 '' using 1:3 title '120.0' w boxes ls 2, \
 '' using 1:4 title '240.0' w boxes ls 3, \
 '' using 1:5 title '360.0' w boxes ls 4, \
 '' using 1:6 title '480.0' w boxes ls 5


### priority=bigger, strategy=fillerup ###

set terminal svg size 1200 900

# plot 1. x-axis: ships, y-axis: queuing duration of ship

set out 'plot_ships_fillerup_bigger.svg'
set title "Queueing duration (strategy=fillerup, priority=bigger)"
set xlabel "Ship #"
set ylabel "Seconds"
#unset xlabel
#unset xtics
set key title "Max Wait"
set key bottom center out
set key horizontal



# set yrange [0:90000]
set xrange [0:500]
set style fill solid

plot 'output_fillerup_bigger.csv' \
    using 1:2 title '0.0' w boxes ls 1, \
 '' using 1:3 title '120.0' w boxes ls 2, \
 '' using 1:4 title '240.0' w boxes ls 3, \
 '' using 1:5 title '360.0' w boxes ls 4, \
 '' using 1:6 title '480.0' w boxes ls 5


### priority=smaller, strategy=roundrobin ###

set terminal svg size 1200 900

# plot 1. x-axis: ships, y-axis: queuing duration of ship

set out 'plot_ships_roundrobin_smaller.svg'
set title "Queueing duration (strategy=roundrobin, priority=smaller)"
set xlabel "Ship #"
set ylabel "Seconds"
#unset xlabel
#unset xtics
set key title "Max Wait"
set key bottom center out
set key horizontal



# set yrange [0:90000]
set xrange [0:500]
set style fill solid

plot 'output_roundrobin_smaller.csv' \
    using 1:2 title '0.0' w boxes ls 1, \
 '' using 1:3 title '120.0' w boxes ls 2, \
 '' using 1:4 title '240.0' w boxes ls 3, \
 '' using 1:5 title '360.0' w boxes ls 4, \
 '' using 1:6 title '480.0' w boxes ls 5


### priority=smaller, strategy=fillerup ###

set terminal svg size 1200 900

# plot 1. x-axis: ships, y-axis: queuing duration of ship

set out 'plot_ships_fillerup_smaller.svg'
set title "Queueing duration (strategy=fillerup, priority=smaller)"
set xlabel "Ship #"
set ylabel "Seconds"
#unset xlabel
#unset xtics
set key title "Max Wait"
set key bottom center out
set key horizontal



# set yrange [0:90000]
set xrange [0:500]
set style fill solid

plot 'output_fillerup_smaller.csv' \
    using 1:2 title '0.0' w boxes ls 1, \
 '' using 1:3 title '120.0' w boxes ls 2, \
 '' using 1:4 title '240.0' w boxes ls 3, \
 '' using 1:5 title '360.0' w boxes ls 4, \
 '' using 1:6 title '480.0' w boxes ls 5

# plot 2. x-axis: max-wait parameter, y-axis: queueing durations of ships

set out 'plot_box_roundrobin_bigger.svg'
set title "Queueing duration (strategy=roundrobin, priority=bigger)"
set style fill solid 0.25 border -1
set style boxplot outliers pointtype 7
set style data boxplot
set key off

set xlabel "Max Wait"
unset xrange
unset yrange

set xtics ('0.0' 0, '120.0' 1, '240.0' 2, '360.0' 3, '480.0' 4)

plot 'output_roundrobin_bigger.csv' \
    using (0):2 title '0.0', \
  '' using (1):3 title '120.0', \
  '' using (2):4 title '240.0', \
  '' using (3):5 title '360.0', \
  '' using (4):6 title '480.0'



# plot 2. x-axis: max-wait parameter, y-axis: queueing durations of ships

set out 'plot_box_fillerup_bigger.svg'
set title "Queueing duration (strategy=fillerup, priority=bigger)"
set style fill solid 0.25 border -1
set style boxplot outliers pointtype 7
set style data boxplot
set key off

set xlabel "Max Wait"
unset xrange
unset yrange

set xtics ('0.0' 0, '120.0' 1, '240.0' 2, '360.0' 3, '480.0' 4)

plot 'output_fillerup_bigger.csv' \
    using (0):2 title '0.0', \
  '' using (1):3 title '120.0', \
  '' using (2):4 title '240.0', \
  '' using (3):5 title '360.0', \
  '' using (4):6 title '480.0'



# plot 2. x-axis: max-wait parameter, y-axis: queueing durations of ships

set out 'plot_box_roundrobin_smaller.svg'
set title "Queueing duration (strategy=roundrobin, priority=smaller)"
set style fill solid 0.25 border -1
set style boxplot outliers pointtype 7
set style data boxplot
set key off

set xlabel "Max Wait"
unset xrange
unset yrange

set xtics ('0.0' 0, '120.0' 1, '240.0' 2, '360.0' 3, '480.0' 4)

plot 'output_roundrobin_smaller.csv' \
    using (0):2 title '0.0', \
  '' using (1):3 title '120.0', \
  '' using (2):4 title '240.0', \
  '' using (3):5 title '360.0', \
  '' using (4):6 title '480.0'



# plot 2. x-axis: max-wait parameter, y-axis: queueing durations of ships

set out 'plot_box_fillerup_smaller.svg'
set title "Queueing duration (strategy=fillerup, priority=smaller)"
set style fill solid 0.25 border -1
set style boxplot outliers pointtype 7
set style data boxplot
set key off

set xlabel "Max Wait"
unset xrange
unset yrange

set xtics ('0.0' 0, '120.0' 1, '240.0' 2, '360.0' 3, '480.0' 4)

plot 'output_fillerup_smaller.csv' \
    using (0):2 title '0.0', \
  '' using (1):3 title '120.0', \
  '' using (2):4 title '240.0', \
  '' using (3):5 title '360.0', \
  '' using (4):6 title '480.0'

# plot 3. x-axis: queueing duration interval, y-axis: number of ships

bin_width = 5*60;

set out 'plot_freq_roundrobin_bigger.svg'
set title "Frequency of queueing durations (strategy=roundrobin, priority=bigger)"
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

plot 'output_roundrobin_bigger.csv' \
    using (rounded($2)):(1) title '0.0' smooth frequency with boxes, \
 '' using (rounded($3)):(1) title '120.0' smooth frequency with boxes, \
 '' using (rounded($4)):(1) title '240.0' smooth frequency with boxes, \
 '' using (rounded($5)):(1) title '360.0' smooth frequency with boxes, \
 '' using (rounded($6)):(1) title '480.0' smooth frequency with boxes



# plot 3. x-axis: queueing duration interval, y-axis: number of ships

bin_width = 5*60;

set out 'plot_freq_fillerup_bigger.svg'
set title "Frequency of queueing durations (strategy=fillerup, priority=bigger)"
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

plot 'output_fillerup_bigger.csv' \
    using (rounded($2)):(1) title '0.0' smooth frequency with boxes, \
 '' using (rounded($3)):(1) title '120.0' smooth frequency with boxes, \
 '' using (rounded($4)):(1) title '240.0' smooth frequency with boxes, \
 '' using (rounded($5)):(1) title '360.0' smooth frequency with boxes, \
 '' using (rounded($6)):(1) title '480.0' smooth frequency with boxes



# plot 3. x-axis: queueing duration interval, y-axis: number of ships

bin_width = 5*60;

set out 'plot_freq_roundrobin_smaller.svg'
set title "Frequency of queueing durations (strategy=roundrobin, priority=smaller)"
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

plot 'output_roundrobin_smaller.csv' \
    using (rounded($2)):(1) title '0.0' smooth frequency with boxes, \
 '' using (rounded($3)):(1) title '120.0' smooth frequency with boxes, \
 '' using (rounded($4)):(1) title '240.0' smooth frequency with boxes, \
 '' using (rounded($5)):(1) title '360.0' smooth frequency with boxes, \
 '' using (rounded($6)):(1) title '480.0' smooth frequency with boxes



# plot 3. x-axis: queueing duration interval, y-axis: number of ships

bin_width = 5*60;

set out 'plot_freq_fillerup_smaller.svg'
set title "Frequency of queueing durations (strategy=fillerup, priority=smaller)"
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

plot 'output_fillerup_smaller.csv' \
    using (rounded($2)):(1) title '0.0' smooth frequency with boxes, \
 '' using (rounded($3)):(1) title '120.0' smooth frequency with boxes, \
 '' using (rounded($4)):(1) title '240.0' smooth frequency with boxes, \
 '' using (rounded($5)):(1) title '360.0' smooth frequency with boxes, \
 '' using (rounded($6)):(1) title '480.0' smooth frequency with boxes