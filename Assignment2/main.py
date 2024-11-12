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
        self.addConnection("deltaT", "halfDelta")

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


class PID_Error(CBD):
    def __init__(self, name="PID_Error", setPoint=10.0):
        CBD.__init__(self, name, input_ports=["IN1"], output_ports=["OUT1"])

        self.addBlock(ConstantBlock("setPoint", value=setPoint))
        self.addBlock(NegatorBlock("Negate"))
        self.addBlock(AdderBlock("_Err"))
        self.addConnection("IN1", "Negate")
        self.addConnection("Negate", "_Err")
        self.addConnection("setPoint", "_Err")
        self.addConnection("_Err", "OUT1")


class PID_P(CBD):
    def __init__(self, name="PID_P", Kp=1.0):
        CBD.__init__(self, name, ["IN1"], ["OUT1"])
        self.addBlock(ConstantBlock("Kp", value=Kp))
        self.addBlock(ProductBlock("P"))
        self.addConnection("IN1", "P")
        self.addConnection("Kp", "P")
        self.addConnection("P", "OUT1")


class PID_I(CBD):
    def __init__(self, name="PID_I", Ki=1.0):
        CBD.__init__(self, name, ["IN1"], ["OUT1"])
        self.addBlock(ConstantBlock("Ki", value=Ki))
        self.addBlock(ConstantBlock("I_init", value=0))
        self.addBlock(IntegratorBlock("I_"))
        self.addBlock(ProductBlock("P"))
        self.addConnection("IN1", "I_", input_port_name="IN1")
        self.addConnection("I_init", "I_", output_port_name="OUT1", input_port_name="IC")
        self.addConnection("I_", "P")
        self.addConnection("Ki", "P")
        self.addConnection("P", "OUT1")

class PID_D(CBD):
    def __init__(self, name="PID_D", Kd=1.0):
        CBD.__init__(self, name, ["IN1"], ["OUT1"])
        self.addBlock(ConstantBlock("Kd", value=Kd))
        self.addBlock(ConstantBlock("D_init", value=0))
        self.addBlock(DerivatorBlock("D_"))
        self.addBlock(ProductBlock("P"))
        self.addConnection("IN1", "D_", input_port_name="IN1")
        self.addConnection("D_init", "D_", output_port_name="OUT1", input_port_name="IC")
        self.addConnection("D_", "P")
        self.addConnection("Kd", "P")
        self.addConnection("P", "OUT1")


class PIDBlock(CBD):
    def __init__(self, name="Controller", Kp=15.0, Ki=1.0, Kd=22.0, setPoint=10.0):
        CBD.__init__(self, name, ["IN"], ["OUT"])

        self.addBlock(PID_Error("Err", setPoint))
        self.addBlock(AdderBlock("Sum", 3))
        self.addBlock(PID_P("P_", Kp))
        self.addBlock(PID_I("I_", Ki))
        self.addBlock(PID_D("D_", Kd))
        self.addConnection("IN", "Err")
        self.addConnection("Err", "P_")
        self.addConnection("Err", "I_")
        self.addConnection("Err", "D_")
        self.addConnection("P_", "Sum", input_port_name="IN1")
        self.addConnection("I_", "Sum", input_port_name="IN2")
        self.addConnection("D_", "Sum", input_port_name="IN3")
        self.addConnection("Sum", "OUT")



class PIDTest(CBD):
    def __init__(self, name="PIDTIME"):
        CBD.__init__(self, name, [], ["OUT"])

        self.addBlock(PIDBlock("PID"))
        self.addBlock(TimeBlock("time"))
        self.addConnection("time", "PID", input_port_name="IN", output_port_name="OUT1")
        self.addConnection("PID", "OUT", output_port_name="OUT")



b_e = BackwardsEulerSystem("backwardsEuler")
f_e = ForwardsEulerSystem("forwardEuler")
tr = TrapezoidSystem("trapezoid")

"""
backwardsEuler:
	deltaT=0.1: result=3.222190908877023, error=0.009698804877023015
	deltaT=0.01: result=3.213459296657502, error=0.0009671926575021139
	deltaT=0.001: result=3.212588796472303, error=9.669247230315037e-05
forwardEuler:
	deltaT=0.1: result=3.223153281886757, error=0.010661177886757134
	deltaT=0.01: result=3.213555450684053, error=0.001063346684053279
	deltaT=0.001: result=3.212598411043006, error=0.0001063070430062929
trapezoid:
	deltaT=0.1: result=3.2226720953818915, error=0.010179991381891629
	deltaT=0.01: result=3.213507373670786, error=0.0010152696707863562
	deltaT=0.001: result=3.21259360375765, error=0.00010149975765028074
"""

pid = PIDBlock()
sim = Simulator(pid)
sim.setDeltaT(0.1)
sim.run(100)

# for sys in [b_e, f_e, tr]:
#     print(f"{sys.getBlockName()}:")
#     for deltaT in [0.1, 0.01, 0.001]:
#         cloned_sys = sys.clone()
#
#         sim = Simulator(cloned_sys)
#         sim.setDeltaT(deltaT)
#         sim.run(1000 * deltaT)
#
#         data = cloned_sys.getSignalHistory("OUT")
#         result = data[-1][1]
#         error = abs(result - 3.212492104)
#
#         print(f"deltaT={deltaT}: result={result}, error={error}")
