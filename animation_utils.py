import matplotlib.animation as animation
import matplotlib.pyplot as plt
import math

def update_frame(frame, all_edges, selected_nodes, positions, ax, lines, final_path_drawn, draw_final_path):
    """Updates each frame of the animation."""
    for ln in lines:
        if ln in ax.lines:
            ln.remove()
    lines[:] = []  # Clear the list in place

    if frame >= len(all_edges):
        if not final_path_drawn[0]:
            draw_final_path()
            final_path_drawn[0] = True
        return lines

    edges = all_edges[frame]

    if not edges or len(selected_nodes) < 2:
        return lines

    source = selected_nodes[0]
    max_dist = 1e-6
    dist_map = {}

    for u, _ in edges:
        if u in positions and source in positions:
            dx = positions[source][0] - positions[u][0]
            dy = positions[source][1] - positions[u][1]
            dist_map[u] = math.sqrt(dx*dx + dy*dy)
            max_dist = max(max_dist, dist_map[u])

    for u, v in edges:
        if u in positions and v in positions:
            fac = math.sqrt(dist_map.get(u, 0) / max_dist) if u in dist_map else 0.5
            r = 0.1 + 0.8 * fac
            g = 1.0 - 0.5 * fac
            b = 0.2 + 0.5 * fac
            x0, y0, _ = positions[u]
            x1, y1, _ = positions[v]
            ln, = ax.plot([x0, x1], [y0, y1], color=(r, g, b), linewidth=2)
            lines.append(ln)

    return lines

def animate_path(fig, update_frame_func, frames, interval=80):
    """Creates and returns the animation object."""
    return animation.FuncAnimation(fig, update_frame_func, frames=frames, interval=interval)

def save_animation(ani, selected_nodes, plt):
    """Saves the animation to a file."""
    if not ani or len(selected_nodes) != 2:
        plt.title("Please run the animation first before saving")
        plt.draw()
        return

    try:
        source = selected_nodes[0]
        destination = selected_nodes[1]
        filename = f"astar_from_{source}_to_{destination}.mp4"
        ani.save(filename, writer="ffmpeg", fps=10)
        plt.title(f"Animation saved as {filename}")
    except Exception as e:
        plt.title(f"Error saving animation: {str(e)}")

    plt.draw()

def draw_final_path(ax, adj_dict, positions, selected_nodes, astar_func, plt):
    """Draws the final shortest path on the graph."""
    if not astar_func or len(selected_nodes) != 2:
        print("Please run the animation first.")
        return

    try:
        final_path_nodes = astar_func(adj_dict, selected_nodes[0], selected_nodes[1], 1000)
        if isinstance(final_path_nodes, list) and len(final_path_nodes) > 1:
            print("\n✅ Đường đi ngắn nhất đã tìm được:")
            for i in range(len(final_path_nodes) - 1):
                u = final_path_nodes[i]
                v = final_path_nodes[i + 1]
                if u in positions and v in positions:
                    x0, y0, _ = positions[u]
                    x1, y1, _ = positions[v]
                    ax.plot([x0, x1], [y0, y1], color='darkorange', linewidth=4, linestyle='--')
                    print(f" - Từ node {u} đến node {v}")
            plt.title(f"✅ Đường đi ngắn nhất từ {selected_nodes[0]} đến {selected_nodes[1]} đã được hiển thị")
        else:
            print("⚠️ Không tìm được đường đi ngắn nhất.")
            plt.title("⚠️ Không tìm được đường đi ngắn nhất.")

        plt.draw()

    except Exception as e:
        print(f"❌ Lỗi khi tìm đường: {e}")