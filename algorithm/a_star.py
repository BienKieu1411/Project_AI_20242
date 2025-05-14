import heapq
import csv
from typing import Dict, List, Tuple, Optional

nodes_file = "data/fileCsv/nodes.csv"

def astar(adj_list: Dict[int, Dict[int, float]], 
          source: int, 
          destination: int,
          num_iterations: int = 10000
          ) -> Tuple[Optional[List[int]], List[int], Optional[float]]:

    node_coordinates: Dict[int, Tuple[float, float]] = {}
    try:
        with open(nodes_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    node_id = int(row['node_id'])
                    x, y = float(row['x']), float(row['y']) 
                    node_coordinates[node_id] = (x, y)
                except ValueError:
                    continue
    except FileNotFoundError:
        print(f"LỖI (A*): Không tìm thấy file tọa độ node: {nodes_file}")
        return None, [], None
    except Exception as e:
        print(f"LỖI (A*): Không thể đọc file tọa độ node {nodes_file}: {e}")
        return None, [], None

    def euclidean_heuristic(node1_id: int, node2_id: int) -> float:
        if node1_id not in node_coordinates or node2_id not in node_coordinates:
            return float('inf')
        coord1 = node_coordinates[node1_id]
        coord2 = node_coordinates[node2_id]
        return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5

    open_list: List[Tuple[float, int]] = []
    heapq.heappush(open_list, (euclidean_heuristic(source, destination), source))

    came_from: Dict[int, Optional[int]] = {source: None}
    
    all_potential_nodes = set(adj_list.keys())
    all_potential_nodes.add(source)
    all_potential_nodes.add(destination)
    g_score = {node_id: float('inf') for node_id in all_potential_nodes}
    g_score[source] = 0.0
    
    f_score: Dict[int, float] = {node_id: float('inf') for node_id in all_potential_nodes}
    f_score[source] = euclidean_heuristic(source, destination)

    explored_order: List[int] = []
    iterations_count = 0

    while open_list and iterations_count < num_iterations:
        iterations_count += 1
        current_f_score, current_node = heapq.heappop(open_list)

        if current_f_score > f_score.get(current_node, float('inf')):
            continue

        explored_order.append(current_node)

        if current_node == destination:
            path: List[int] = []
            temp: Optional[int] = destination
            while temp is not None:
                path.append(temp)
                temp = came_from.get(temp)
            if not path or path[-1] != source:
                if source == destination and g_score.get(source) == 0.0:
                    return [source], explored_order, 0.0
                return None, explored_order, None
            return path[::-1], explored_order, g_score[destination]

        if current_node not in adj_list:
            continue

        for neighbor, weight in adj_list[current_node].items():
            if neighbor not in g_score:
                continue
            tentative_g_score = g_score.get(current_node, float('inf')) + weight
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + euclidean_heuristic(neighbor, destination)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None, explored_order, None
