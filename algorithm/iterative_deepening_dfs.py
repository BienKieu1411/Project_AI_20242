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

def _dls_iterative(adj_list: Dict[int, Dict[int, float]], 
                   source: int, 
                   destination: int, 
                   depth_limit: int,
                   explored_nodes_accumulator: List[int], 
                   visited_overall_for_explored_order: Set[int]
                   ) -> Optional[List[int]]:
    stack: List[Tuple[int, List[int], int]] = [(source, [source], 0)]

    while stack:
        current_vertex, path_to_current, current_depth = stack.pop()

        if current_vertex not in visited_overall_for_explored_order:
            explored_nodes_accumulator.append(current_vertex)
            visited_overall_for_explored_order.add(current_vertex)

        if current_vertex == destination:
            return path_to_current 

        if current_depth < depth_limit:
            if current_vertex not in adj_list:
                continue 

            for neighbor in reversed(list(adj_list[current_vertex].keys())):
                if neighbor not in path_to_current:
                    new_path = list(path_to_current)
                    new_path.append(neighbor)
                    stack.append((neighbor, new_path, current_depth + 1))
    return None 

def iddfs(adj_list: Dict[int, Dict[int, float]], 
          source: int, 
          destination: int, 
          max_depth: int = 20
          ) -> Tuple[Optional[List[int]], List[int], Optional[float]]:
    explored_nodes_overall: List[int] = []
    visited_overall_for_explored_order: Set[int] = set() 

    for depth in range(max_depth + 1):
        path_found = _dls_iterative(adj_list, source, destination, depth, explored_nodes_overall, visited_overall_for_explored_order)
        
        if path_found:
            cost_on_adj_list = _calculate_path_cost(adj_list, path_found)
            return path_found, explored_nodes_overall, cost_on_adj_list
            
    return None, explored_nodes_overall, None
