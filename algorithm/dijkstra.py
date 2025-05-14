import heapq
from typing import Dict, List, Tuple, Optional, Set 

def dijkstra(adj_list: Dict[int, Dict[int, float]], 
             source: int, 
             destination: int
             ) -> Tuple[Optional[List[int]], List[int], Optional[float]]:
    
    priority_queue: List[Tuple[float, int]] = []
    heapq.heappush(priority_queue, (0.0, source))
    
    all_nodes_in_graph: Set[int] = set(adj_list.keys())
    all_nodes_in_graph.add(source)
    all_nodes_in_graph.add(destination)
    for node_id in adj_list:
        all_nodes_in_graph.update(adj_list[node_id].keys())

    distances: Dict[int, float] = {node: float('inf') for node in all_nodes_in_graph}
    distances[source] = 0.0 
    
    predecessors: Dict[int, Optional[int]] = {node: None for node in all_nodes_in_graph}
    
    explored_order: List[int] = [] 

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        if current_distance > distances.get(current_vertex, float('inf')):
            continue

        if current_vertex not in explored_order:
             explored_order.append(current_vertex)

        if current_vertex == destination:
            if distances[destination] == float('inf'):
                return None, explored_order, None

            path: List[int] = []
            temp_node: Optional[int] = destination
            while temp_node is not None:
                path.append(temp_node)
                if temp_node == source:
                    break
                temp_node = predecessors.get(temp_node)
                if temp_node is None and path[-1] != source:
                    return None, explored_order, None
            
            if not path or path[-1] != source:
                 if source == destination:
                     return [source], explored_order, 0.0
                 return None, explored_order, None

            return path[::-1], explored_order, distances[destination]

        if current_vertex in adj_list:
            for neighbor, weight in adj_list[current_vertex].items():
                if neighbor not in distances:
                    continue

                distance_through_current = current_distance + weight
                
                if distance_through_current < distances[neighbor]:
                    distances[neighbor] = distance_through_current
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance_through_current, neighbor))
            
    return None, explored_order, None
