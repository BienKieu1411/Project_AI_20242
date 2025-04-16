import matplotlib.pyplot as plt
from visualization import find_nearest_node

def handle_click(event, ax, positions, selected_points, selected_nodes, animation_running):
    """Handles mouse click events to select start and end points."""
    if animation_running[0]:
        return

    nearest_node = find_nearest_node(ax, positions, event)

    if nearest_node is not None:
        if len(selected_points) < 2:
            color = 'green' if len(selected_points) == 0 else 'red'
            x, y, _ = positions[nearest_node]
            point, = ax.plot(x, y, 'o', markersize=10, color=color, alpha=1.0)
            selected_points.append(point)
            selected_nodes.append(nearest_node)

            if len(selected_nodes) == 1:
                plt.title(f"Start point selected (Node {nearest_node}). Now select end point.")
            elif len(selected_nodes) == 2:
                plt.title(f"Start: Node {selected_nodes[0]}, End: Node {selected_nodes[1]} - Press 'Run Animation' to start")

            plt.draw()

def reset_selection(ax, selected_points, selected_nodes, animation_running, ani, lines, all_edges, plt):
    """Resets the selection of start and end points and clears animation."""
    if animation_running[0] and ani is not None:
        ani.event_source.stop()

    for point in selected_points:
        point.remove()
    selected_points.clear()
    selected_nodes.clear()

    for ln in lines:
        if ln in ax.lines:
            ln.remove()
    lines.clear()
    all_edges.clear()

    plt.title(f"Visualization - Click to select start and end points")
    animation_running[0] = False
    plt.draw()

