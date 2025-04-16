import matplotlib.pyplot as plt

def initialize_plot(positions):
    """Initializes the Matplotlib figure and axes."""
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.subplots_adjust(bottom=0.15)  # Make space for buttons
    ax.set_aspect('equal')
    plt.title(f"Visualization ({len(positions)} nodes) - Click to select start and end points")
    plt.axis('off')
    return fig, ax

def plot_nodes(ax, nodes_df, positions):
    """Plots all the nodes on the graph with different colors."""
    for node_id, (x, y, added_value) in positions.items():
        color = (
            'red' if added_value == 1 else
            'blue'
        )
        ax.plot(x, y, 'o', color=color, markersize=8, alpha=0.7)

def plot_edges(ax, adj_dict, positions):
    """Plots the base graph edges in light gray."""
    edge_count = 0
    for u in adj_dict:
        for v in adj_dict[u]:
            if u in positions and v in positions:
                x0, y0 = positions[u][:2]
                x1, y1 = positions[v][:2]
                ax.plot([x0, x1], [y0, y1], color='lightgray', linewidth=0.8)
                edge_count += 1
    print(f"Đã vẽ {edge_count} cạnh trên đồ thị")

def add_legend(ax):
    """Adds a legend to the plot."""
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Node thông thường'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Node được thêm'),
    ]
    ax.legend(handles=legend_elements, loc='upper right')

def find_nearest_node(ax, positions, event):
    """Finds the nearest node to a mouse click event."""
    if event.inaxes != ax:
        return None
    min_dist = float('inf')
    nearest_node = None
    x, y = event.xdata, event.ydata
    for node_id, (node_x, node_y, _) in positions.items():
        dist_sq = (node_x - x)**2 + (node_y - y)**2
        if dist_sq < min_dist:
            min_dist = dist_sq
            nearest_node = node_id
    return nearest_node