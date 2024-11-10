from fmpy import simulate_fmu
from fmpy.fmucontainer import create_fmu_container, Connection, Configuration, Component, Variable
from fmpy.validation import validate_fmu
from fmpy.util import compile_platform_binary
from fmpy.model_description import DefaultExperiment

if __name__ == "__main__":

	configuration = Configuration(
		fmiVersion='2.0',
		defaultExperiment=DefaultExperiment(
			startTime='0',
			stopTime='40',
			tolerance='1e-7',
			stepSize='0.001'
		),
		parallelDoStep=False,
		variables = [
			Variable(
				type='Real',
				initial='calculated',
				variability='continuous',
				causality='output',
				name='x',
				mapping=[('plant', 'x_output')]
			)
		],
		components=[
			Component(
				filename='Plant.fmu',
				name='plant'
			),
			Component(
				filename='Controller.fmu',
				name='pid'
			)
		],
		connections=[
			Connection('pid', 'Controller.OUT', 'plant', 'u_input'),
			Connection('plant', 'x_output', 'pid', 'Controller.IN')
		]
	)

	create_fmu_container(configuration, "Container.fmu")
	problems = validate_fmu("Container.fmu")
	if problems:
		print("PROBLEMS ENCOUNTERED WITH COMBINED FMU:")
		print(problems)
		exit()

	result = simulate_fmu("Container.fmu",
						  #debug_logging=True,
						  #fmi_call_logger=print,
						  stop_time=40,
						  output_interval=0.001)

	# import matplotlib.pyplot as plt
	#
	# plt.plot([r[0] for r in result], [r[2] for r in result], label="x_tgt")
	# plt.plot([r[0] for r in result], [r[3] for r in result], label="x_ego")
	# plt.legend()
	# plt.show()
	# plt.plot([r[0] for r in result], [r[1] for r in result], label="x_err")
	# plt.legend()
	# plt.show()