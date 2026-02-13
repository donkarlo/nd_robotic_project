import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# Function to draw a 3D-perspective drone with shadowed rotors but NO shadows for connecting lines
def draw_perspective_drone_no_shadow_lines(ax, drone_x, drone_y, size=1.5, shadow_offset=0.1, line_thickness=12):
    """
    Draws a 2D drone with perspective, keeping connecting lines in their correct locations,
    while ensuring shadowed rotors remain but NO shadow for the connecting lines.
    """
    # Define rotor positions with reversed perspective (bottom rotors larger, top rotors smaller)
    rotor_positions = [
        (drone_x - size, drone_y - size * 0.6, size * 1.6, 0.8),  # Bottom-left rotor (closer, much larger)
        (drone_x + size, drone_y - size * 0.6, size * 1.6, 0.8),  # Bottom-right rotor (closer, much larger)
        (drone_x - size * 0.8, drone_y + size * 0.6, size * 1.2, 0.6),  # Top-left rotor (further, still larger)
        (drone_x + size * 0.8, drone_y + size * 0.6, size * 1.2, 0.6)  # Top-right rotor (further, still larger)
    ]

    # Connect diagonal rotors (counter-opposite) with only MAIN thick lines (no shadow lines)
    rotor_pairs = [(0, 3), (1, 2)]

    # Draw main thick lines (NO shadowed lines)
    for i, j in rotor_pairs:
        ax.plot([rotor_positions[i][0], rotor_positions[j][0]],
                [rotor_positions[i][1], rotor_positions[j][1]],
                color='black', linewidth=line_thickness)  # Main thick lines only

    # Draw the lower shadow-like discs for 3D effect (unaltered)
    for pos in rotor_positions:
        lower_disc = patches.Ellipse((pos[0], pos[1] - shadow_offset), width=pos[2], height=pos[3],
                                     color='gray', alpha=0.5)  # Slightly transparent gray disc below
        ax.add_patch(lower_disc)

    # Draw the main rotors as large discs (ensuring they are **always** on top)
    for pos in rotor_positions:
        rotor = patches.Ellipse((pos[0], pos[1]), width=pos[2], height=pos[3], color='black', alpha=1)
        ax.add_patch(rotor)


# Create a standalone 2D drone drawing with properly trimmed shadowed rotors and NO shadowed lines
fig, ax = plt.subplots(figsize=(6, 6))

# Define drone position at center
drone_x, drone_y = 0, 0

# Draw the perspective drone with shadowed rotors but NO shadowed lines
draw_perspective_drone_no_shadow_lines(ax, drone_x, drone_y, size=1.5, shadow_offset=0.1, line_thickness=12)

# Adjust plot limits and remove axis for a clean view
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

plt.show()
