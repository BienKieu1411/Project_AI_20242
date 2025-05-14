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

def dfs(adj_list: Dict[int, Dict[int, float]], 
        source: int, 
        destination: int
        ) -> Tuple[Optional[List[int]], List[int], Optional[float]]:

    stack: List[Tuple[int, List[int]]] = []
    stack.append((source, [source]))
    explored_order: List[int] = []
    visited_nodes_fully_explored: Set[int] = set()

    while stack:
        current_vertex, path_to_current = stack.pop()

        if current_vertex not in explored_order:
             explored_order.append(current_vertex)

        if current_vertex == destination:
            cost_on_adj_list = _calculate_path_cost(adj_list, path_to_current)
            return path_to_current, explored_order, cost_on_adj_list

        if current_vertex not in adj_list:
            continue
            
        sorted_neighbors = sorted(list(adj_list[current_vertex].keys()), reverse=True)
        for neighbor in sorted_neighbors:
            if neighbor not in path_to_current:
                new_path = list(path_to_current)
                new_path.append(neighbor)
                stack.append((neighbor, new_path))
    
    return None, explored_order, None
