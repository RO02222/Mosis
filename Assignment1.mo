package Assignment1

  model pendulum
    // Types
    type Factor = Real(unit = "");
    // Parameters
    parameter Modelica.Units.SI.Mass m = 0.2;     // Mass of the pendulum, (kg)
    parameter Modelica.Units.SI.Mass M = 10;      // Mass of the cart, (kg)
    parameter Modelica.Units.SI.Length r = 1;     // Length of rope, (m)
    parameter Factor dp = 0.12;                   // Damping factor of the pendulum, no unit
    parameter Factor dc = 4.79;                   // Damping factor of the cart, no unit
    constant Modelica.Units.SI.Acceleration g = 9.80665;  // Gravitational acceleration on Earth, (m/(s^2))
    // Variables
    Modelica.Units.SI.Length x;                   // displacement of the cart, (m)
    Modelica.Units.SI.Velocity v;                 // Velocity of the cart, (m/s)
    Modelica.Units.SI.Angle th;                   // Angular displacement of the pendulum, (rad)
    Modelica.Units.SI.AngularVelocity ohm;        // Angular velocity of the pendulum, (rad/s)
    Real u;                                       // Control signal to move the cart, no unit
    
    initial equation
    x=0;
    v=0;
    th=0;
    ohm=0;
    
    
    equation
    if time < 0.5 then u = 100; else u = 0; end if;
    
    der(x) = v;
    der(th) = ohm;
    der(v) = (r*(dc*v - m*(g*sin(th)*cos(th) + r*sin(th)*ohm^2) -u)-(dp*cos(th))*ohm) / (-r*(M+m*sin(th)^2));
    der(ohm) = (dp*ohm*(m+M)+(m^2*r^2*sin(th)*cos(th)*ohm^2) + m*r*(g*sin(th)*(m+M)) + (cos(th)*(u-dc*v))) / ((m*r^2)*(-M-(m*sin(th)^2)));
  
    
  end pendulum;

  model calibration_dc
    //Types
    type Factor = Real(unit = "");
    // Parameters
    parameter Modelica.Units.SI.Mass M = 10;  // Mass of the cart, (kg)
    parameter Factor dc = 2;                  // Damping factor of the cart, no unit
    
    // Variables
    Modelica.Units.SI.Length x;               // displacement of the cart, (m)
    Modelica.Units.SI.Velocity v;             // Velocity of the cart, (m/s)
  
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
    parameter Modelica.Units.SI.Mass m = 0.2; // Mass of the pendulum, (kg)
    parameter Modelica.Units.SI.Length r = 1; // Length of rope, (m)
    parameter Factor dp = 0.5;                // Damping factor of the pendulum, no unit
    constant Modelica.Units.SI.Acceleration g = 9.80665;  // Gravitational acceleration on Earth, (m/(s^2))
  
    // Variables
    Modelica.Units.SI.Angle th;               // Angular displacement of the pendulum, (rad)
    Modelica.Units.SI.AngularVelocity ohm;    // Angular velocity of the pendulum, (rad/s)
    
    initial equation
      th=Modelica.Constants.pi/6;
      ohm=0;
    
    
    equation
      der(th) = ohm;
      der(ohm) = -((dp*ohm)+(m*g*r*sin(th)))/(m*r^2);
  
    
  end calibration_dp;
  annotation(
    uses(Modelica(version = "4.0.0")));
end Assignment1;
