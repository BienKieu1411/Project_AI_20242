import pandas as pd
import csv
import numpy as np

def load_node_data(nodes_file):
    """Loads node data from a CSV file and returns node positions."""
    print("Đang đọc dữ liệu từ file nodes.csv...")
    nodes_df = pd.read_csv(nodes_file)
    print(f"Đọc được {len(nodes_df)} nodes từ file nodes.csv")
    print(f"Các cột trong file nodes.csv: {nodes_df.columns.tolist()}")
    print("Mẫu dữ liệu nodes:")
    print(nodes_df.head())

    required_columns = ['node_id', 'x', 'y', 'added']
    for col in required_columns:
        if col not in nodes_df.columns:
            raise ValueError(f"Thiếu cột {col} trong file nodes.csv")

    positions = {}
    for _, row in nodes_df.iterrows():
        try:
            node_id = int(row['node_id'])
            x = float(row['x']) * 10  # Scale lên cho dễ nhìn
            y = float(row['y']) * 10
            positions[node_id] = (x, y, int(row['added']))
        except Exception as e:
            print(f"Lỗi khi đọc node {row['node_id']}: {e}")

    print(f"Đã đọc được tọa độ cho {len(positions)} nodes")
    return nodes_df, positions

def load_adj_list(edges_file):
    """Loads the adjacency list with weights from a CSV file."""
    print("\nĐang đọc dữ liệu từ file adj_list_with_weights.csv...")
    with open(edges_file, 'r') as f:
        header = next(f)
        sample_line = next(f)
        print(f"Header: {header.strip()}")
        print(f"Dòng mẫu: {sample_line.strip()}")

    adj_dict = {}
    with open(edges_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        for row in reader:
            try:
                node = int(row[0])
                neighbors = {}
                raw_text = row[1]

                if node < 5:
                    print(f"Node {node}, raw text: {raw_text}")

                try:
                    parsed_data = eval(raw_text.replace('np.float64', ''))
                    for neighbor_id, weight in parsed_data:
                        neighbors[int(neighbor_id)] = float(weight)
                except:
                    raw = raw_text.replace('[', '').replace(']', '').replace('np.float64', '') \
                                .replace('(', '').replace(')', '')
                    parts = raw.split(',')
                    for i in range(0, len(parts) - 1, 2):
                        if parts[i].strip() and parts[i+1].strip():
                            neighbor_id = int(parts[i].strip())
                            weight = float(parts[i+1].strip())
                            neighbors[neighbor_id] = weight

                adj_dict[node] = neighbors

            except Exception as e:
                print(f"Lỗi khi xử lý node {row[0]}: {e}")
                continue

    print(f"Đã đọc được {len(adj_dict)} nodes từ adj_list")
    return adj_dict

def reconcile_data(positions, adj_dict):
    """Ensures all nodes in the adjacency list have positions and vice versa."""
    nodes_in_positions = set(positions.keys())
    nodes_in_adj = set(adj_dict.keys())

    print(f"\nSố node có trong positions nhưng không có trong adj_dict: {len(nodes_in_positions - nodes_in_adj)}")
    print(f"Số node có trong adj_dict nhưng không có trong positions: {len(nodes_in_adj - nodes_in_positions)}")

    all_nodes = nodes_in_positions.union(nodes_in_adj)
    print(f"Tổng số node hợp nhất: {len(all_nodes)}")

    x_values = [pos[0] for pos in positions.values()]
    y_values = [pos[1] for pos in positions.values()]

    if len(nodes_in_adj - nodes_in_positions) > 0:
        print("Đang tạo tọa độ cho các node thiếu...")
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)

        for node in nodes_in_adj - nodes_in_positions:
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            positions[node] = (x, y, 0)  # Assume 'added' is 0 for these

        print(f"Đã tạo tọa độ cho {len(nodes_in_adj - nodes_in_positions)} node thiếu")

    for node in nodes_in_positions - nodes_in_adj:
        adj_dict[node] = {}

    return positions, adj_dict