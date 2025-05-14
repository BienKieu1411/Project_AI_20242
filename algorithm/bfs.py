from collections import deque
from typing import Dict, List, Tuple, Optional, Set

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

def bfs(adj_list: Dict[int, Dict[int, float]], 
        source: int, 
        destination: int
        ) -> Tuple[Optional[List[int]], List[int], Optional[float]]:

    queue: deque[Tuple[int, List[int]]] = deque([(source, [source])])  
    visited_nodes: Set[int] = {source}  
    explored_order: List[int] = [] 

    while queue:
        current_vertex, path_to_current = queue.popleft()
        explored_order.append(current_vertex)

        if current_vertex == destination:
            cost_on_adj_list = _calculate_path_cost(adj_list, path_to_current)
            return path_to_current, explored_order, cost_on_adj_list

        if current_vertex not in adj_list:
            continue

        for neighbor in adj_list[current_vertex].keys():
            if neighbor not in visited_nodes:
                visited_nodes.add(neighbor)
                new_path = list(path_to_current)
                new_path.append(neighbor)
                queue.append((neighbor, new_path))
    
    return None, explored_order, None
