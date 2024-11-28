import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Step 1: Define the parameters of the pendulum
length = 1.0  # Length of the pendulum
g = 9.81  # Acceleration due to gravity
theta0 = np.pi / 4  # Initial angle (45 degrees)
omega0 = 0.0  # Initial angular velocity

# Step 2: Define the time parameters
dt = 0.05  # Time step
t = 0.0  # Initial time

# Step 3: Initialize the state of the pendulum
theta = theta0
omega = omega0

# Step 4: Create the figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
line, = ax.plot([], [], 'o-', lw=2)

# Step 5: Create the button
ax_button = plt.axes([0.8, 0.05, 0.1, 0.075])
button = Button(ax_button, 'Next Frame')

# Step 6: Define the update function
def update(frame):
    global theta, omega, t
    t += dt
    omega += - (g / length) * np.sin(theta) * dt
    theta += omega * dt
    x = length * np.sin(theta)
    y = -length * np.cos(theta)
    line.set_data([0, x], [0, y])
    return line,

# Step 7: Define the button click event handler
def on_button_click(event):
    update(0)
    plt.draw()

button.on_clicked(on_button_click)

# Step 8: Initialize the animation
def init():
    line.set_data([], [])
    return line,

# Step 9: Show the plot
plt.show()