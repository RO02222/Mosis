package Assignment1

  model pendulum
    // Types
    type Factor = Real(unit = "");
    // Parameters
    parameter Modelica.Units.SI.Mass m = 0.2;
    parameter Modelica.Units.SI.Mass M = 10;
    parameter Modelica.Units.SI.Length r = 1;
    parameter Factor dp = 0.5;
    parameter Factor dc = 2;
    constant Modelica.Units.SI.Acceleration g = 9.80665;
    // Variables
    Modelica.Units.SI.Length x;
    Modelica.Units.SI.Velocity v;
    Modelica.Units.SI.Angle th;
    Modelica.Units.SI.AngularVelocity ohm;
    Real u;
    
    initial equation
    x=0;
    v=0;
    th=0;
    ohm=0;
    
    
    equation
    if time < 0.5 then u = 1000; else u = 0; end if;
    
    der(x) = v;
    der(th) = ohm;
    der(v) = (r*(dc*v - m*(g*sin(th)*cos(th) + r*sin(th)*ohm^2) -u)-(dp*cos(th))*ohm) / (-r*(M+m*sin(th)^2));
    der(ohm) = (dp*ohm*(m+M)+(m^2*r^2*sin(th)*cos(th)*ohm^2) + m*r*(g*sin(th)*(m+M)) + (cos(th)*(u-dc*v))) / ((m*r^2)*(-M-(m*sin(th)^2)));
  
    
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
      x=0;
      v=5;
    
    equation  
      der(x) = v;
      der(v) = -(dc / M) * v;
  
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
      th=30;
      ohm=0;
    
    
    equation
      der(th) = ohm;
      der(ohm) = -((dp*ohm)+(m*g*r*sin(th)))/(m*r^2);
  
    
  end calibration_dp;
  annotation(
    uses(Modelica(version = "4.0.0")));
end Assignment1;