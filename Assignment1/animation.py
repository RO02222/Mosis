#!/usr/bin/env python
__author__ = "Rakshit Mittal"
__copyright__ = "Copyright 2024, MSDL, University of Antwerp, Belgium"
__credits__ = ["Hans Vangheluwe", "Joost Mertens"]
__license__ = "MIT"
__maintainer__ = "Rakshit Mittal"
__email__ = "rakshit.mittal@uantwerpen.be"
"""
This Python module is used to animate the gantry system Modelica model based on its solution from the 
executed Modelica-compiled code.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from simulate import readMat
matplotlib.use('TkAgg')


def animate_gantry_system(x_array, theta_array, length=1, interval=1):
    """
    Create an animation of a gantry system based on arrays of x positions and pendulum angles theta.

    :param x_array: Array of cart positions along the x-axis.
    :param theta_array: Array of pendulum angles (in radians).
    :param length: optional, Length of the pendulum (rope), default is 1.0.
    :param interval : optional, Delay between frames in milliseconds, default is 1ms.
    """
    # Set ambiguous cart width
    cart_width = 0.4
    cart_height = 0.2

    # Calculate figure limits
    x_min = np.min(x_array) - 1.0
    x_max = np.max(x_array) + 1.0
    y_min = -length - 1.0
    y_max = cart_height + 1.0

    # Create figure of appropriate size
    fig, ax = plt.subplots()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal')
    ax.grid()

    # Draw rails
    ax.plot([x_min, x_max], [0, 0], 'k--', lw=2)

    # Initialize cart
    cart = Rectangle((x_array[0] - cart_width / 2, 0), cart_width, cart_height, fc='blue', ec='black')
    ax.add_patch(cart)

    # Initialize pendulum line and bob
    pendulum_line, = ax.plot([], [], lw=2, c='red')
    pendulum_bob, = ax.plot([], [], 'o', c='black')

    def init():
        # Initialize cart position
        cart.set_xy((x_array[0] - cart_width / 2, 0))

        # Calculate initial pendulum end point
        pendulum_x = x_array[0] + length * np.sin(theta_array[0])
        pendulum_y = -length * np.cos(theta_array[0])

        # Initialize pendulum line
        pendulum_line.set_data([x_array[0], pendulum_x], [0, pendulum_y])

        # Initialize pendulum bob
        pendulum_bob.set_data([pendulum_x], [pendulum_y])  # Wrap in lists

        return cart, pendulum_line, pendulum_bob

    def animate(i):
        # Update cart position
        cart.set_xy((x_array[i] - cart_width / 2, 0))

        # Calculate pendulum end point
        pendulum_x = x_array[i] + length * np.sin(theta_array[i])
        pendulum_y = -length * np.cos(theta_array[i])

        # Update pendulum line
        pendulum_line.set_data([x_array[i], pendulum_x], [0, pendulum_y])

        # Update pendulum bob
        pendulum_bob.set_data([pendulum_x], [pendulum_y])  # Wrap in lists

        return cart, pendulum_line, pendulum_bob

    ani = animation.FuncAnimation(fig, animate, frames=len(x_array), init_func=init, blit=True, interval=interval)

    plt.show()


# Example usage:
if __name__ == '__main__':
    # Call the animation function with sample data
    values = readMat("pendulum/Assignment1.pendulum/pendulum_res.mat")
    mapping = {var: val for var, val in zip(values[0], values[1])}
    animate_gantry_system(mapping["x"], mapping["th"], length=1, interval=1)
