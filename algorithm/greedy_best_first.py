import heapq
import csv
from typing import Dict, List, Tuple, Optional, Set

nodes_file = "data/fileCsv/nodes.csv" 

def _calculate_path_cost(adj_list: Dict[int, Dict[int, float]], path: List[int]) -> Optional[float]:
    if not path or len(path) < 2:
        return 0.0 

    total_cost = 0.0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        if u in adj_list and v in adj_list.get(u, {}): 
            edge_weight = adj_list[u].get(v) 
            if edge_weight is None: 
                return float('inf') 
            total_cost += edge_weight
        else:
            return float('inf') 
    return total_cost

def greedy_best_first(adj_list: Dict[int, Dict[int, float]], 
                        source: int, 
                        destination: int
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
        print(f"LỖI (GreedyBFS): Không tìm thấy file tọa độ node: {nodes_file}")
        return None, [], None
    except Exception as e:
        print(f"LỖI (GreedyBFS): Không thể đọc file tọa độ node {nodes_file}: {e}")
        return None, [], None

    def heuristic(node1_id: int, node2_id: int) -> float:
        if node1_id not in node_coordinates or node2_id not in node_coordinates:
            return float('inf')
        
        coord1 = node_coordinates[node1_id]
        coord2 = node_coordinates[node2_id]
        return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5

    priority_queue: List[Tuple[float, int]] = []
    heapq.heappush(priority_queue, (heuristic(source, destination), source))
    
    came_from: Dict[int, Optional[int]] = {source: None}
    
    explored_order: List[int] = []
    
    visited_nodes: Set[int] = set()

    while priority_queue:
        h_value, current_node = heapq.heappop(priority_queue)

        if current_node in visited_nodes:
            continue
        
        visited_nodes.add(current_node)
        explored_order.append(current_node)

        if current_node == destination:
            path: List[int] = []
            temp: Optional[int] = destination
            while temp is not None:
                path.append(temp)
                temp = came_from.get(temp) 
            
            if not path or path[-1] != source:
                 if source == destination: return [source], explored_order, 0.0
                 return None, explored_order, None

            path.reverse()
            cost_on_adj_list = _calculate_path_cost(adj_list, path)
            return path, explored_order, cost_on_adj_list

        if current_node not in adj_list:
            continue

        sorted_neighbors_by_heuristic: List[Tuple[float, int]] = []
        for neighbor in adj_list[current_node]:
            if neighbor not in visited_nodes:
                if neighbor in node_coordinates:
                    h_neighbor = heuristic(neighbor, destination)
                    sorted_neighbors_by_heuristic.append((h_neighbor, neighbor))
        
        for h_val_neighbor, neighbor_node in sorted(sorted_neighbors_by_heuristic):
            if neighbor_node not in visited_nodes:
                if neighbor_node not in came_from:
                     came_from[neighbor_node] = current_node
                heapq.heappush(priority_queue, (h_val_neighbor, neighbor_node))

    return None, explored_order, None
