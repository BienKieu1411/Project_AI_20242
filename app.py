# Tệp: app.py
import csv
from flask import Flask, request, jsonify
from flask_cors import CORS
from copy import deepcopy
from typing import Dict, List, Optional, Tuple, Set 
import ast # Sử dụng ast.literal_eval thay cho eval

# Import các thuật toán của bạn
from algorithm.a_star import astar
from algorithm.dijkstra import dijkstra
from algorithm.bfs import bfs
from algorithm.dfs import dfs
from algorithm.greedy_best_first import greedy_best_first
from algorithm.iterative_deepening_dfs import iddfs
from algorithm.uniform_cost_search import uniform_cost_search

app = Flask(__name__)
CORS(app)

# --- Cấu hình và Đồ thị gốc ---
adj_dict_original: Dict[int, Dict[int, float]] = {}
edges_file_original: str = 'data/fileCsv/adj_list_with_weights.csv'

# VẬN TỐC MẶC ĐỊNH (mét trên giây)
DEFAULT_SPEED_MPS: float = 4.17  # (Khoảng 40 km/h)
# Bạn có thể điều chỉnh giá trị này hoặc thậm chí làm cho nó linh hoạt hơn sau này (ví dụ: dựa trên loại đường)

try:
    with open(edges_file_original, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        # print(f"Đọc file: {edges_file_original}")
        # print(f"Header: {header}")

        for row_idx, row in enumerate(reader):
            if not row or len(row) < 2: continue
            try:
                node_id_str = row[0].strip()
                if not node_id_str: continue
                node = int(node_id_str)
                
                neighbors_str = row[1].strip()
                neighbors: Dict[int, float] = {}

                if not neighbors_str or neighbors_str == '[]':
                    adj_dict_original[node] = neighbors
                    continue
                
                try:
                    cleaned_neighbors_str = neighbors_str.replace('np.float64(', '').replace(')', '')
                    if cleaned_neighbors_str.startswith('[') and cleaned_neighbors_str.endswith(']'):
                        parsed_data = ast.literal_eval(cleaned_neighbors_str)
                        if not isinstance(parsed_data, list):
                             raise ValueError("Dữ liệu parse không phải là list")
                        for item in parsed_data:
                            if isinstance(item, (list, tuple)) and len(item) == 2:
                                neighbor_id, weight = item # weight ở đây là KHOẢNG CÁCH
                                neighbors[int(neighbor_id)] = float(weight)
                            else:
                                pass 
                    else:
                        raise ValueError("Chuỗi không phải là danh sách các tuple.")
                except (ValueError, SyntaxError) as e_eval: 
                    raw = neighbors_str.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('np.float64', '')
                    parts = raw.split(',')
                    temp_neighbors_list = []
                    if len(parts) >= 2 and len(parts) % 2 == 0: 
                        for i in range(0, len(parts), 2):
                            try:
                                neighbor_id_part = parts[i].strip()
                                weight_part = parts[i+1].strip()
                                if neighbor_id_part and weight_part:
                                    temp_neighbors_list.append((int(neighbor_id_part), float(weight_part)))
                            except ValueError:
                                continue 
                        for neighbor_id, weight in temp_neighbors_list:
                             neighbors[neighbor_id] = weight
                adj_dict_original[node] = neighbors
            except ValueError:
                # print(f"Dòng {row_idx+2}: Lỗi xử lý dòng (ValueError): {row} - {ve_row}")
                continue
            except Exception:
                # print(f"Dòng {row_idx+2}: Lỗi không xác định khi xử lý dòng: {row} - {e_row}")
                continue
    # print(f"Đã đọc thành công {len(adj_dict_original)} nút từ {edges_file_original} vào adj_dict_original.")
    if not adj_dict_original:
        print("CẢNH BÁO: adj_dict_original rỗng sau khi đọc file. Kiểm tra lại file CSV và logic đọc file.")
except FileNotFoundError:
    print(f"LỖI: Không tìm thấy file {edges_file_original}.")
except Exception as e_file:
    print(f"LỖI không mong muốn khi đọc file {edges_file_original}: {e_file}")

def calculate_path_cost_on_graph(graph: Dict[int, Dict[int, float]], path: List[int]) -> Optional[float]:
    if not path or len(path) < 2: return 0.0
    total_cost = 0.0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        if u in graph and v in graph.get(u, {}): 
            edge_weight = graph[u].get(v)
            if edge_weight is None: return float('inf') 
            total_cost += edge_weight
        else: return float('inf') 
    return total_cost

# --- API Endpoint ---
@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Yêu cầu không chứa dữ liệu JSON."}), 400

    start_node_id = data.get('start')
    end_node_id = data.get('end')
    algorithm_name = data.get('algorithm', 'A Star')
    
    blocked_edges = data.get('blocked_edges', [])
    traffic_edges = data.get('traffic_edges', [])
    traffic_level = int(data.get('traffic_level', 1))
    flood_edges = data.get('flood_edges', [])
    flood_level = int(data.get('flood_level', 1))
    one_way_edges = data.get('one_way_edges', [])
    max_depth_iddfs = int(data.get('max_depth_iddfs', 20)) 
    num_iterations_astar = int(data.get('iterations', 10000))

    if start_node_id is None or end_node_id is None:
        return jsonify({"error": "Thiếu node 'start' hoặc 'end'."}), 400
    try:
        start_node = int(start_node_id)
        end_node = int(end_node_id)
    except ValueError:
        return jsonify({"error": "Node 'start' hoặc 'end' phải là số nguyên."}), 400

    if not adj_dict_original:
         return jsonify({"error": "Lỗi: Dữ liệu đồ thị gốc chưa được tải hoặc rỗng."}), 500
    
    all_nodes_in_original_graph = set(adj_dict_original.keys())
    for u_node in adj_dict_original:
        all_nodes_in_original_graph.update(adj_dict_original[u_node].keys())
    if start_node not in all_nodes_in_original_graph or end_node not in all_nodes_in_original_graph:
         return jsonify({"error": f"Node bắt đầu ({start_node}) hoặc kết thúc ({end_node}) không tồn tại trong dữ liệu đồ thị."}), 400

    # ----- BƯỚC 1: Tạo adj_list_filtered với TRỌNG SỐ LÀ THỜI GIAN CƠ BẢN -----
    adj_list_filtered = {}
    for u, neighbors in adj_dict_original.items():
        adj_list_filtered[u] = {}
        for v, distance in neighbors.items():
            if DEFAULT_SPEED_MPS > 0:
                base_time_seconds = distance / DEFAULT_SPEED_MPS
                adj_list_filtered[u][v] = base_time_seconds
            else: # Tránh chia cho 0 nếu tốc độ không hợp lệ
                adj_list_filtered[u][v] = float('inf') 
    
    # ----- BƯỚC 2: Áp dụng các điều kiện lên adj_list_filtered (trọng số giờ là thời gian) -----
    # 2.1. Xử lý đường một chiều
    for one_way_edge in one_way_edges:
        if len(one_way_edge) == 2:
            source_ow, destination_ow = one_way_edge
            if destination_ow in adj_list_filtered and source_ow in adj_list_filtered.get(destination_ow, {}):
                del adj_list_filtered[destination_ow][source_ow]

    # 2.2. Xử lý cạnh bị cấm
    for edge in blocked_edges:
        if len(edge) == 2:
            u, v = edge
            if u in adj_list_filtered and v in adj_list_filtered.get(u, {}):
                del adj_list_filtered[u][v]
            if v in adj_list_filtered and u in adj_list_filtered.get(v, {}):
                del adj_list_filtered[v][u]
    
    is_direct_blocked = False
    for edge in blocked_edges: 
        if (edge[0] == start_node and edge[1] == end_node) or \
           (edge[1] == start_node and edge[0] == end_node):
            is_direct_blocked = True
            break
    if is_direct_blocked:
         return jsonify({"error": "Không thể tìm đường: Tuyến đường trực tiếp giữa điểm đầu và điểm cuối đã bị cấm."}), 400

    # 2.3. Xử lý tắc đường (nhân THỜI GIAN với hệ số k)
    k = 1.0
    if traffic_level == 1: k = 1.75
    elif traffic_level == 2: k = 2.25
    elif traffic_level == 3: k = 2.75 
    
    if k != 1.0: 
        for edge_nodes in traffic_edges: # Đổi tên biến để tránh nhầm lẫn với tuple (u,v)
            if len(edge_nodes) == 2:
                u, v = edge_nodes
                if u in adj_list_filtered and v in adj_list_filtered.get(u, {}):
                    adj_list_filtered[u][v] *= k
                if v in adj_list_filtered and u in adj_list_filtered.get(v, {}): 
                    adj_list_filtered[v][u] *= k
                
    # 2.4. Xử lý ngập lụt (nhân THỜI GIAN hoặc loại bỏ cạnh)
    f_factor = 1.0
    remove_edge_due_to_flood = False
    if flood_level == 1: f_factor = 2.25 
    elif flood_level == 2: f_factor = 2.75 
    elif flood_level == 3: remove_edge_due_to_flood = True 

    if remove_edge_due_to_flood or f_factor != 1.0:
        for edge_nodes in flood_edges: # Đổi tên biến
            if len(edge_nodes) == 2:
                u, v = edge_nodes
                if remove_edge_due_to_flood:
                    if u in adj_list_filtered and v in adj_list_filtered.get(u, {}):
                        del adj_list_filtered[u][v]
                    if v in adj_list_filtered and u in adj_list_filtered.get(v, {}):
                        del adj_list_filtered[v][u]
                elif f_factor != 1.0:
                    if u in adj_list_filtered and v in adj_list_filtered.get(u, {}):
                        adj_list_filtered[u][v] *= f_factor
                    if v in adj_list_filtered and u in adj_list_filtered.get(v, {}):
                        adj_list_filtered[v][u] *= f_factor
    
    algorithms = {
        'A Star': astar, 'Dijkstra': dijkstra, 'BFS': bfs, 'DFS': dfs,
        'Greedy Best First': greedy_best_first, 
        'Iterative Deepening DFS': iddfs,
        'Uniform Cost Search': uniform_cost_search,
    }

    if algorithm_name not in algorithms:
        return jsonify({"error": "Thuật toán không hợp lệ."}), 400

    path_finding_function = algorithms[algorithm_name]
    path_nodes: Optional[List[int]] = None
    explored_node_ids: List[int] = []
    cost_with_factors: Optional[float] = None # Đây sẽ là THỜI GIAN ƯỚC TÍNH (giây)

    try:
        # print(f"Gọi thuật toán: {algorithm_name} từ {start_node} đến {end_node}")
        if algorithm_name == 'Iterative Deepening DFS':
            path_nodes, explored_node_ids, cost_with_factors = path_finding_function(adj_list_filtered, start_node, end_node, max_depth=max_depth_iddfs)
        elif algorithm_name == 'A Star': 
             path_nodes, explored_node_ids, cost_with_factors = path_finding_function(adj_list_filtered, start_node, end_node, num_iterations=num_iterations_astar)
        else:
            path_nodes, explored_node_ids, cost_with_factors = path_finding_function(adj_list_filtered, start_node, end_node)
            
    except Exception as e_algo:
        print(f"Lỗi khi chạy thuật toán {algorithm_name} cho ({start_node} -> {end_node}): {e_algo}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Lỗi trong quá trình tìm đường với {algorithm_name}. Chi tiết: {str(e_algo)}"}), 500

    if not path_nodes:
        return jsonify({
            "error": f"Không tìm thấy đường đi từ {start_node} đến {end_node} bằng thuật toán {algorithm_name}.",
            "explored_nodes": list(set(explored_node_ids)) if explored_node_ids else [] 
            }), 404

    # Tính toán quãng đường thực tế (real_distance) dựa trên adj_dict_original (luôn là khoảng cách)
    real_distance = calculate_path_cost_on_graph(adj_dict_original, path_nodes) 
    
    if real_distance == float('inf'): 
        real_distance = None 
    if cost_with_factors == float('inf'):
        cost_with_factors = None

    return jsonify({
        "path": path_nodes,
        "explored_nodes": list(set(explored_node_ids)) if explored_node_ids else [], 
        "message": "Đường đi đã được tìm thấy.",
        "cost_with_factors": cost_with_factors, # Đơn vị là giây
        "real_distance": real_distance  # Đơn vị là mét (hoặc đơn vị gốc của weight)
    })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)