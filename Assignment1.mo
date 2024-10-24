package Assignment1
  model pendulum
    // Types
    type Factor = Real(unit = "");
    // Parameters
    parameter Modelica.Units.SI.Mass m = 0.2;
    parameter Modelica.Units.SI.Mass M = 10;
    parameter Modelica.Units.SI.Length r = 1;
    parameter Factor dp = 0.12;
    parameter Factor dc = 4.79;
    constant Modelica.Units.SI.Acceleration g = 9.80665;
    // Variables
    Modelica.Units.SI.Length x;
    Modelica.Units.SI.Velocity v;
    Modelica.Units.SI.Angle th;
    Modelica.Units.SI.AngularVelocity ohm;
    Real u;
  initial equation
    u = 0;
    x = 0;
    v = 0;
    th = 0;
    ohm = 0;
  equation
    der(x) = v;
    der(th) = ohm;
    der(v) = (r*(dc*v - m*(g*sin(th)*cos(th) + r*sin(th)*ohm^2) - u) - (dp*cos(th))*ohm)/(-r*(M + m*sin(th)^2));
    der(ohm) = (dp*ohm*(m + M) + (m^2*r^2*sin(th)*cos(th)*ohm^2) + m*r*(g*sin(th)*(m + M)) + (cos(th)*(u - dc*v)))/((m*r^2)*(-M - (m*sin(th)^2)));
  end pendulum;

  model calibration_dc
    //Types
    type Factor = Real(unit = "");
    // Parameters
    parameter Modelica.Units.SI.Mass M = 10;
    parameter Factor dc = 2;
    // Variables
    Modelica.Units.SI.Length x;
    Modelica.Units.SI.Velocity v;
  initial equation
    x = 0;
    v = 5;
  equation
    der(x) = v;
    der(v) = -(dc/M)*v;
  end calibration_dc;

  model calibration_dp
    // Types
    type Factor = Real(unit = "");
    // Parameters
    parameter Modelica.Units.SI.Mass m = 0.2;
    parameter Modelica.Units.SI.Length r = 1;
    parameter Factor dp = 0.5;
    constant Modelica.Units.SI.Acceleration g = 9.80665;
    // Variables
    Modelica.Units.SI.Angle th;
    Modelica.Units.SI.AngularVelocity ohm;
  initial equation
    th = Modelica.Constants.pi/6;
    ohm = 0;
  equation
    der(th) = ohm;
    der(ohm) = -((dp*ohm) + (m*g*r*sin(th)))/(m*r^2);
  end calibration_dp;

  block plant
    extends Modelica.Blocks.Icons.Block;
    extends pendulum;
    Modelica.Blocks.Interfaces.RealInput u_input "Input signal connector" annotation(
      Placement(transformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}}), iconTransformation(origin = {-90, -6}, extent = {{-20, -20}, {20, 20}})));
    Modelica.Blocks.Interfaces.RealOutput x_output "Output signal connector" annotation(
      Placement(transformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {118, -4}, extent = {{-10, -10}, {10, 10}})));
  equation
    u_input = u;
    x_output = x;
  end plant;

  block pid
    parameter Real kp = 7;
    parameter Real ki = 0;
    parameter Real kd = 10;
  Modelica.Blocks.Sources.Constant const(k = kp)  annotation(
      Placement(transformation(origin = {-30, 90}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Product product2 annotation(
      Placement(transformation(origin = {10, 80}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Continuous.Integrator integrator annotation(
      Placement(transformation(origin = {-30, 20}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Continuous.Derivative derivative annotation(
      Placement(transformation(origin = {-30, -40}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.Constant const1(final k = ki) annotation(
      Placement(transformation(origin = {-30, 50}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Product product21 annotation(
      Placement(transformation(origin = {10, 40}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.Constant const11(k = kd) annotation(
      Placement(transformation(origin = {-30, -10}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Product product211 annotation(
      Placement(transformation(origin = {10, -20}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealInput u annotation(
      Placement(transformation(origin = {-130, 40}, extent = {{-20, -20}, {20, 20}}), iconTransformation(origin = {-120, 40}, extent = {{-20, -20}, {20, 20}})));
  Modelica.Blocks.Interfaces.RealOutput y annotation(
      Placement(transformation(origin = {110, 20}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {96, 8}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.MultiSum multiSum(nu = 2)  annotation(
      Placement(transformation(origin = {-80, 20}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.MultiSum multiSum1(nu = 3)  annotation(
      Placement(transformation(origin = {50, 20}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealInput x annotation(
      Placement(transformation(origin = {-140, -24}, extent = {{-20, -20}, {20, 20}}), iconTransformation(origin = {-120, -40}, extent = {{-20, -20}, {20, 20}})));
  Modelica.Blocks.Math.Product product annotation(
      Placement(transformation(origin = {-98, -18}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.Constant const12(final k = -1) annotation(
      Placement(transformation(origin = {-132, 4}, extent = {{-10, -10}, {10, 10}})));
  equation
    connect(const.y, product2.u1) annotation(
      Line(points = {{-19, 90}, {-11.5, 90}, {-11.5, 86}, {-2, 86}}, color = {0, 0, 127}));
    connect(const1.y, product21.u1) annotation(
      Line(points = {{-19, 50}, {-11.5, 50}, {-11.5, 46}, {-2, 46}}, color = {0, 0, 127}));
    connect(integrator.y, product21.u2) annotation(
      Line(points = {{-18, 20}, {-12, 20}, {-12, 34}, {-2, 34}}, color = {0, 0, 127}));
    connect(const11.y, product211.u1) annotation(
      Line(points = {{-18, -10}, {-10, -10}, {-10, -14}, {-2, -14}}, color = {0, 0, 127}));
    connect(derivative.y, product211.u2) annotation(
      Line(points = {{-18, -40}, {-12, -40}, {-12, -26}, {-2, -26}}, color = {0, 0, 127}));
    connect(multiSum.y, integrator.u) annotation(
      Line(points = {{-68, 20}, {-42, 20}}, color = {0, 0, 127}));
    connect(multiSum.y, product2.u2) annotation(
      Line(points = {{-68, 20}, {-52, 20}, {-52, 74}, {-2, 74}}, color = {0, 0, 127}));
    connect(multiSum.y, derivative.u) annotation(
      Line(points = {{-68, 20}, {-52, 20}, {-52, -40}, {-42, -40}}, color = {0, 0, 127}));
    connect(u, multiSum.u[1]) annotation(
      Line(points = {{-130, 40}, {-110, 40}, {-110, 20}, {-90, 20}}, color = {0, 0, 127}));
    connect(product2.y, multiSum1.u[1]) annotation(
      Line(points = {{22, 80}, {30, 80}, {30, 20}, {40, 20}}, color = {0, 0, 127}));
    connect(product21.y, multiSum1.u[2]) annotation(
      Line(points = {{22, 40}, {30, 40}, {30, 20}, {40, 20}}, color = {0, 0, 127}));
    connect(product211.y, multiSum1.u[3]) annotation(
      Line(points = {{22, -20}, {30, -20}, {30, 20}, {40, 20}}, color = {0, 0, 127}));
  connect(multiSum1.y, y) annotation(
      Line(points = {{62, 20}, {110, 20}}, color = {0, 0, 127}));
  connect(x, product.u2) annotation(
      Line(points = {{-140, -24}, {-110, -24}}, color = {0, 0, 127}));
  connect(const12.y, product.u1) annotation(
      Line(points = {{-120, 4}, {-118, 4}, {-118, -12}, {-110, -12}}, color = {0, 0, 127}));
  connect(product.y, multiSum.u[2]) annotation(
      Line(points = {{-86, -18}, {-76, -18}, {-76, 2}, {-110, 2}, {-110, 20}, {-90, 20}}, color = {0, 0, 127}));
    annotation(
      Diagram);
  end pid;

  model pid_control_loop
  plant plant1 annotation(
      Placement(transformation(origin = {44, 0}, extent = {{-10, -10}, {10, 10}})));
  pid pid1 annotation(
      Placement(transformation(extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.Constant const(k = 10)  annotation(
      Placement(transformation(origin = {-54, 10}, extent = {{-10, -10}, {10, 10}})));
  equation
  connect(pid1.y, plant1.u_input) annotation(
      Line(points = {{10, 0}, {36, 0}}, color = {0, 0, 127}));
  connect(plant1.x_output, pid1.x) annotation(
      Line(points = {{56, 0}, {80, 0}, {80, -34}, {-34, -34}, {-34, -4}, {-12, -4}}, color = {0, 0, 127}));
  connect(const.y, pid1.u) annotation(
      Line(points = {{-42, 10}, {-24, 10}, {-24, 4}, {-12, 4}}, color = {0, 0, 127}));
  end pid_control_loop;
  annotation(
    uses(Modelica(version = "4.0.0")));
end Assignment1;