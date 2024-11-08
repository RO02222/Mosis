from pyCBD.Core import *
from pyCBD.lib.std import *
from pyCBD.simulator import Simulator
from matplotlib import pyplot as plt

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

class system(CBD):
	def __init__(self, name="system"):
		CBD.__init__(self, name, output_ports=["OUT"])
		self.addBlock(FunctionGBlock())
		self.addBlock(TimeBlock("time"))
		self.addBlock(IntegratorBlock("euler"))
		self.addBlock(ConstantBlock("zero", 0))

		self.addConnection("time", "FunctionG", input_port_name="t", output_port_name="OUT1")
		self.addConnection("FunctionG", "euler", output_port_name="g")
		self.addConnection("zero", "euler", input_port_name="IC")
		self.addConnection("euler", "OUT", output_port_name="OUT1")

sys = system()
sim = Simulator(sys)
sim.setDeltaT(0.1)
sim.run(100)
data = sys.getSignalHistory("OUT")
x, y = [x for x, _ in data], [y for _, y in data]
print(x, y)
plt.plot(x, y)
plt.show()