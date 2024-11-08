from pyCBD.Core import *
from pyCBD.lib.std import *
from pyCBD.simulator import Simulator
from matplotlib import pyplot as plt

class BackwardEulerIntegrator(CBD):
	def __init__(self, name="BackwardEulerIntegrator"):
		CBD.__init__(self, name, ["IN1", "IC"], ["OUT1"])
		self.addBlock(DeltaTBlock("deltaT"))
		self.addBlock(ConstantBlock("zero", 0))
		self.addBlock(DelayBlock("delay1"))
		self.addBlock(DelayBlock("delay2"))
		self.addBlock(ProductBlock("multDelta"))
		self.addBlock(AdderBlock("I"))

		self.addConnection("zero", "delay1", input_port_name="IC")
		self.addConnection("IN1", "delay1", input_port_name="IN1")
		self.addConnection("delay1", "multDelta")
		self.addConnection("deltaT", "multDelta")
		self.addConnection("multDelta", "I")

		self.addConnection("IC", "delay2", input_port_name="IC")
		self.addConnection("delay2", "I")

		self.addConnection("I", "delay2", input_port_name="IN1")

		self.addConnection("I", "OUT1")

class ForwardEulerIntegrator(CBD):
	def __init__(self, name="BackwardEulerIntegrator"):
		CBD.__init__(self, name, ["IN1", "IC"], ["OUT1"])
		self.addBlock(DeltaTBlock("deltaT"))
		self.addBlock(DelayBlock("delay"))
		self.addBlock(ProductBlock("multDelta"))
		self.addBlock(AdderBlock("I"))

		self.addConnection("IN1", "multDelta")
		self.addConnection("deltaT", "multDelta")
		self.addConnection("multDelta", "I")

		self.addConnection("IC", "delay", input_port_name="IC")
		self.addConnection("delay", "I")
		self.addConnection("I", "delay", input_port_name="IN1")

		self.addConnection("I", "OUT1")

class TrapezoidIntegrator(CBD):
	def __init__(self, name="TrapezoidIntegrator"):
		CBD.__init__(self, name, ["IN1", "IC"], ["OUT1"])
		self.addBlock(DelayBlock("delay1"))
		self.addBlock(DelayBlock("delay2"))
		self.addBlock(AdderBlock("sum"))
		self.addBlock(ConstantBlock("zero", value=0))
		self.addBlock(ConstantBlock("half", value=0.5))
		self.addBlock(DeltaTBlock("deltaT"))
		self.addBlock(ProductBlock("halfDelta"))
		self.addBlock(ProductBlock("multDelta"))
		self.addBlock(AdderBlock("I"))

		self.addConnection("IN1", "delay1", input_port_name="IN1")
		self.addConnection("zero", "delay1", input_port_name="IC")

		self.addConnection("IN1", "sum")
		self.addConnection("delay1", "sum")

		self.addConnection("half", "halfDelta")
		self.addConnection("deltaT","halfDelta")

		self.addConnection("sum", "multDelta")
		self.addConnection("halfDelta", "multDelta")

		self.addConnection("multDelta", "I")
		self.addConnection("delay2", "I")
		self.addConnection("I", "delay2", input_port_name="IN1")
		self.addConnection("IC", "delay2", input_port_name="IC")

		self.addConnection("I", "OUT1")

class FunctionGBlock(CBD):
	def __init__(self, name="FunctionG"):
		CBD.__init__(self, name, ["t"], ["g"])
		self.addBlock(ConstantBlock(block_name="Three", value=3))
		self.addBlock(ConstantBlock(block_name="Two", value=2))
		self.addBlock(AdderBlock(block_name="PlusTwo"))
		self.addBlock(AdderBlock(block_name="PlusThree"))
		self.addBlock(ProductBlock(block_name="Square"))
		self.addBlock(InverterBlock(block_name="Invert"))
		self.addBlock(ProductBlock(block_name="Divide"))
		# t+2
		self.addConnection("t", "PlusTwo")
		self.addConnection("Two", "PlusTwo")
		# t+3
		self.addConnection("t", "PlusThree")
		self.addConnection("Three", "PlusThree")
		# 1/(t+3)^2
		self.addConnection("PlusThree", "Square")
		self.addConnection("PlusThree", "Square")
		self.addConnection("Square", "Invert")
		# (t+2)/(t+3)^2
		self.addConnection("PlusTwo", "Divide")
		self.addConnection("Invert", "Divide")
		self.addConnection("Divide", "g")

class BackwardsEulerSystem(CBD):
	def __init__(self, name="system"):
		CBD.__init__(self, name, output_ports=["OUT"])
		self.addBlock(FunctionGBlock())
		self.addBlock(TimeBlock("time"))
		self.addBlock(BackwardEulerIntegrator("euler"))
		self.addBlock(ConstantBlock("zero", 0))

		self.addConnection("time", "FunctionG", input_port_name="t", output_port_name="OUT1")
		self.addConnection("FunctionG", "euler", output_port_name="g")
		self.addConnection("zero", "euler", input_port_name="IC")
		self.addConnection("euler", "OUT", output_port_name="OUT1")

class ForwardsEulerSystem(CBD):
	def __init__(self, name="system"):
		CBD.__init__(self, name, output_ports=["OUT"])
		self.addBlock(FunctionGBlock())
		self.addBlock(TimeBlock("time"))
		self.addBlock(ForwardEulerIntegrator("euler"))
		self.addBlock(ConstantBlock("zero", 0))

		self.addConnection("time", "FunctionG", input_port_name="t", output_port_name="OUT1")
		self.addConnection("FunctionG", "euler", output_port_name="g")
		self.addConnection("zero", "euler", input_port_name="IC")
		self.addConnection("euler", "OUT", output_port_name="OUT1")

class TrapezoidSystem(CBD):
	def __init__(self, name="system"):
		CBD.__init__(self, name, output_ports=["OUT"])
		self.addBlock(FunctionGBlock())
		self.addBlock(TimeBlock("time"))
		self.addBlock(TrapezoidIntegrator("euler"))
		self.addBlock(ConstantBlock("zero", 0))

		self.addConnection("time", "FunctionG", input_port_name="t", output_port_name="OUT1")
		self.addConnection("FunctionG", "euler", output_port_name="g")
		self.addConnection("zero", "euler", input_port_name="IC")
		self.addConnection("euler", "OUT", output_port_name="OUT1")

b_e = BackwardsEulerSystem("backwardsEuler")
f_e = ForwardsEulerSystem("forwardEuler")
tr = TrapezoidSystem("trapezoid")

for sys in [b_e, f_e, tr]:
    print(f"{sys.getBlockName()}:")
    for deltaT in [0.1, 0.01, 0.001]:
        cloned_sys = sys.clone()

        sim = Simulator(cloned_sys)
        sim.setDeltaT(deltaT)
        sim.run(100)
        
        data = cloned_sys.getSignalHistory("OUT")
        result = data[-1][1]
        error = abs(result - 3.212492104)
        
        print(f"deltaT={deltaT}: result={result}, error={error}")

