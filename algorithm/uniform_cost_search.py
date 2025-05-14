import heapq
from typing import Dict, List, Tuple, Optional, Set

def uniform_cost_search(adj_list: Dict[int, Dict[int, float]], 
                          source: int, 
                          destination: int
                          ) -> Tuple[Optional[List[int]], List[int], Optional[float]]:
    priority_queue: List[Tuple[float, int, List[int]]] = []
    heapq.heappush(priority_queue, (0.0, source, [source])) 
    
    visited_or_settled: Set[int] = set()
    explored_order: List[int] = [] 

    while priority_queue:
        current_cost, current_vertex, path_to_current = heapq.heappop(priority_queue)

        if current_vertex in visited_or_settled:
            continue
        
        visited_or_settled.add(current_vertex)
        explored_order.append(current_vertex)

        if current_vertex == destination:
            return path_to_current, explored_order, current_cost 

        if current_vertex not in adj_list:
            continue

        for neighbor, weight in adj_list[current_vertex].items():
            if neighbor not in visited_or_settled:
                new_cost = current_cost + weight
                new_path = list(path_to_current)
                new_path.append(neighbor)
                heapq.heappush(priority_queue, (new_cost, neighbor, new_path))
            
    return None, explored_order, None
