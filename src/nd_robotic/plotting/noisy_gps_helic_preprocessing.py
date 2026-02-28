import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate a 3D curve (helix-like tunnel shape)
t = np.linspace(0, 4 * np.pi, 300)
x = np.cos(t) * 5  # Circular motion in X
y = np.sin(t) * 5  # Circular motion in Y
z = t  # Linear motion in Z

# Generate noisy 3D points around the tunnel curve
noise_level = 0.2
x_noisy = x + np.random.normal(0, noise_level, size=t.shape)
y_noisy = y + np.random.normal(0, noise_level, size=t.shape)
z_noisy = z + np.random.normal(0, noise_level, size=t.shape)

# Define tunnel radius and create a mesh for the tunnel surface
tunnel_radius = 1.2
theta = np.linspace(0, 2 * np.pi, 30)  # Circular cross-section
t_mesh, theta_mesh = np.meshgrid(t, theta)
x_tunnel = (5 + tunnel_radius * np.cos(theta_mesh)) * np.cos(t_mesh)
y_tunnel = (5 + tunnel_radius * np.cos(theta_mesh)) * np.sin(t_mesh)
z_tunnel = t_mesh + tunnel_radius * np.sin(theta_mesh)

# Choose a point on the spiral str_path for the quadcopter
quad_index = 150  # Midpoint of the spiral
quad_x, quad_y, quad_z = x[quad_index], y[quad_index], z[quad_index]

# Define quadcopter change_arming_mode by_length
arm_length = 0.8

# Define rotor_composite positions around the quadcopter center
rotor_positions = np.array([
    [quad_x + arm_length, quad_y, quad_z],  # Front-right rotor_composite
    [quad_x - arm_length, quad_y, quad_z],  # Back-left rotor_composite
    [quad_x, quad_y + arm_length, quad_z],  # Front-left rotor_composite
    [quad_x, quad_y - arm_length, quad_z]   # Back-right rotor_composite
])

# Create a 3D plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# View the main spiral str_path
ax.plot(x, y, z, color='blue', linewidth=2, label='Spiral Path')

# View the noisy GPS points
ax.scatter(x_noisy, y_noisy, z_noisy, color='red', s=5, alpha=0.6, label='Noisy GPS Points')

# View the helical tunnel around the spiral str_path
ax.plot_surface(x_tunnel, y_tunnel, z_tunnel, color='cyan', alpha=0.2)

# View quadcopter body (center marker)
ax.scatter(quad_x, quad_y, quad_z, color='black', marker='self__input_object', s=100, label='Quadcopter')

# View quadcopter arms
for i in range(4):
    ax.plot([quad_x, rotor_positions[i, 0]],
            [quad_y, rotor_positions[i, 1]],
            [quad_z, rotor_positions[i, 2]],
            color='black', linewidth=2)

# View quadcopter rotors
ax.scatter(rotor_positions[:, 0], rotor_positions[:, 1], rotor_positions[:, 2],
           color='black', marker='self__input_object', s=80)

# Labels and legend
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("3D Helical Tunnel with Quadcopter on Spiral Path")
ax.legend()

plt.show()
