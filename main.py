import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib
matplotlib.use('TkAgg')
from data_loader import load_node_data, load_adj_list, reconcile_data
from visualization import initialize_plot, plot_nodes, plot_edges, add_legend
from interaction import handle_click, reset_selection
from animation_utils import update_frame, animate_path, save_animation, draw_final_path as draw_final_path_util

# File paths
nodes_file = r"nodes.csv"
edges_file = r"adj_list_with_weights.csv"

# Load data
nodes_df, positions = load_node_data(nodes_file)
adj_dict = load_adj_list(edges_file)
positions, adj_dict = reconcile_data(positions, adj_dict)

# Try importing A*
try:
    from a_star import astar
    a_star_available = True
    print("Đã import thành công module a_star")
except ImportError:
    print("Không tìm thấy module a_star, sẽ tắt tính năng tìm đường")
    astar = None
    a_star_available = False

# Global variables for interaction and animation
selected_points = []
selected_nodes = []
animation_running = [False]
ani = None
all_edges = []
lines = []
iterations = 200
final_path_drawn = [False] # Use a list for mutability in update_frame

# Initialize plot
fig, ax = initialize_plot(positions)

# Plot initial graph
plot_nodes(ax, nodes_df, positions)
plot_edges(ax, adj_dict, positions)
add_legend(ax)

# Connect click event
fig.canvas.mpl_connect('button_press_event', lambda event: handle_click(event, ax, positions, selected_points, selected_nodes, animation_running))

# Function to run A* animation
def run_animation(event):
    global animation_running, ani, all_edges, selected_nodes, iterations, final_path_drawn

    if len(selected_nodes) != 2 or animation_running[0] or not a_star_available:
        if not a_star_available:
            plt.title("A* module không khả dụng - Không thể chạy tìm đường")
            plt.draw()
        return

    animation_running[0] = True
    final_path_drawn[0] = False # Reset the flag
    source = selected_nodes[0]
    destination = selected_nodes[1]

    plt.title(f"A* Animation from Node {source} to Node {destination}")

    # Calculate A* steps
    all_edges = []
    try:
        for it in range(1, iterations + 1):
            result = astar(adj_dict, source, destination, it)
            if not isinstance(result, list):
                all_edges.append([])
                continue
            edge_set = []
            for i in range(len(result) - 1):
                u, v = result[i], result[i+1]
                if u in adj_dict and v in adj_dict.get(u, {}):
                    edge_set.append((u, v))
            all_edges.append(edge_set)

        # Create animation
        ani = animate_path(fig, lambda f: update_frame(f, all_edges, selected_nodes, positions, ax, lines, final_path_drawn, lambda: draw_final_path_util(ax, adj_dict, positions, selected_nodes, astar, plt)), frames=len(all_edges), interval=80)
    except Exception as e:
        plt.title(f"Lỗi khi chạy A*: {str(e)}")
        animation_running[0] = False

    plt.draw()

# Function to handle reset button click
def reset_button_clicked(event):
    global selected_points, selected_nodes, animation_running, ani, all_edges, lines, final_path_drawn
    reset_selection(ax, selected_points, selected_nodes, animation_running, ani, lines, all_edges, plt)
    final_path_drawn[0] = False # Reset the flag

# Function to handle save button click
def save_button_clicked(event):
    global ani, selected_nodes, animation_running
    if animation_running[0]:
        save_animation(ani, selected_nodes, plt)
    else:
        plt.title("Please run the animation before saving.")
        plt.draw()

# Add buttons
ax_reset = plt.axes([0.15, 0.05, 0.2, 0.05])
reset_button = Button(ax_reset, 'Reset Selection')
reset_button.on_clicked(reset_button_clicked)

ax_run = plt.axes([0.4, 0.05, 0.2, 0.05])
run_button = Button(ax_run, 'Run Animation')
run_button.on_clicked(run_animation)

ax_save = plt.axes([0.65, 0.05, 0.2, 0.05])
save_button = Button(ax_save, 'Save Animation')
save_button.on_clicked(save_button_clicked)

plt.show()