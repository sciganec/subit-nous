"""Knowledge graph construction and visualization"""

from pathlib import Path
import networkx as nx
import plotly.graph_objects as go
from .core import text_to_subit, subit_to_name, archetype_color

def build_graph(folder_path: str, chunk_size: int = 1000) -> nx.DiGraph:
    """Будує граф архетипів з усіх текстових файлів у папці."""
    graph = nx.DiGraph()
    file_archetypes = []
    path = Path(folder_path)
    
    text_extensions = {'.txt', '.md', '.py', '.json', '.yaml', '.yml', '.rst', '.csv', '.html', '.css', '.js'}
    
    # Якщо це файл, а не папка
    if path.is_file():
        files = [path]
    else:
        files = [f for f in path.rglob('*') if f.is_file() and f.suffix.lower() in text_extensions]
    
    if not files:
        print("[WARN] Текстові файли не знайдено.")
        return graph
    
    for filepath in files:
        try:
            text = filepath.read_text(encoding='utf-8', errors='ignore')
            subit = text_to_subit(text, chunk_size)
            file_archetypes.append((filepath.name, subit))
        except Exception as e:
            print(f"Помилка читання {filepath}: {e}")
    
    # Підрахунок кількості кожного архетипу
    counts = {}
    for _, subit in file_archetypes:
        counts[subit] = counts.get(subit, 0) + 1
    
    # Додавання вузлів
    for subit, count in counts.items():
        graph.add_node(subit,
                       name=subit_to_name(subit),
                       color=archetype_color(subit),
                       count=count)
    
    # Додавання ребер (переходи між файлами в порядку сортування за ім'ям)
    for i in range(len(file_archetypes) - 1):
        from_subit = file_archetypes[i][1]
        to_subit = file_archetypes[i+1][1]
        if graph.has_edge(from_subit, to_subit):
            graph[from_subit][to_subit]['weight'] += 1
        else:
            graph.add_edge(from_subit, to_subit, weight=1)
    
    print(f"[GRAPH] Graph built: {len(graph.nodes)} archetypes, {graph.number_of_edges()} transitions")
    return graph

def visualize_4d(graph: nx.Graph, output_file: str = "graph.html"):
    """Створює 3D-візуалізацію графа."""
    if not graph.nodes:
        print("[WARN] Немає вузлів для візуалізації.")
        return
    
    nodes = list(graph.nodes)
    x = [(n >> 6) & 0b11 for n in nodes]
    y = [(n >> 4) & 0b11 for n in nodes]
    z = [(n >> 2) & 0b11 for n in nodes]
    colors = [graph.nodes[n].get('color', '#888') for n in nodes]
    sizes = [20 + graph.nodes[n].get('count', 0) * 5 for n in nodes]
    names = [graph.nodes[n].get('name', str(n)) for n in nodes]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers+text',
        marker=dict(size=sizes, color=colors, opacity=0.8),
        text=[name.split('_')[0] for name in names],
        hovertext=names,
        name='Archetypes'
    ))
    
    # Додавання ребер
    for u, v in graph.edges():
        ux, uy, uz = (u>>6)&3, (u>>4)&3, (u>>2)&3
        vx, vy, vz = (v>>6)&3, (v>>4)&3, (v>>2)&3
        fig.add_trace(go.Scatter3d(
            x=[ux, vx], y=[uy, vy], z=[uz, vz],
            mode='lines',
            line=dict(color='gray', width=1),
            showlegend=False
        ))
    
    fig.update_layout(
        title="SUBIT-NOUS Knowledge Graph",
        scene=dict(
            xaxis_title="WHO (ME=10, WE=11, YOU=01, THEY=00)",
            yaxis_title="WHERE (EAST=10, SOUTH=11, WEST=01, NORTH=00)",
            zaxis_title="WHEN (SPRING=10, SUMMER=11, AUTUMN=01, WINTER=00)"
        )
    )
    fig.write_html(output_file)
    print(f"[OK] Visualization: {output_file}")

def get_semantic_clusters(graph: nx.Graph, max_distance: int = 2) -> dict:
    """
    Group nodes into clusters based on Hamming distance.
    Returns dict: cluster_id -> list of node ids
    """
    nodes = list(graph.nodes)
    clusters = {}
    visited = set()
    
    for node in nodes:
        if node in visited:
            continue
        
        # Find all nodes within max_distance from current node
        cluster = [node]
        visited.add(node)
        
        for other in nodes:
            if other not in visited:
                dist = bin(node ^ other).count('1')
                if dist <= max_distance:
                    cluster.append(other)
                    visited.add(other)
        
        clusters[len(clusters)] = cluster
    
    return clusters


def add_cluster_metadata(graph: nx.Graph, max_distance: int = 2) -> nx.Graph:
    """Add cluster_id and cluster_size to each node in the graph."""
    clusters = get_semantic_clusters(graph, max_distance)
    for cluster_id, nodes_list in clusters.items():
        for node in nodes_list:
            graph.nodes[node]['cluster_id'] = cluster_id
            graph.nodes[node]['cluster_size'] = len(nodes_list)
    return graph

def visualize_clifford_torus(graph: nx.Graph, output_file: str = "torus.html") -> None:
    """
    Project 256 archetypes onto a Clifford torus in 3D.
    Each archetype becomes a point on a 4D torus projected to 3D.
    """
    import plotly.graph_objects as go
    import numpy as np
    from .core import archetype_color, subit_to_name
    
    if not graph.nodes:
        print("[WARN] No nodes to visualize.")
        return
    
    nodes = list(graph.nodes)
    colors = [archetype_color(n) for n in nodes]
    sizes = [15 + graph.nodes[n].get('count', 0) * 2 for n in nodes]
    
    # Convert 8 bits to 4 angles (0 to 2π) for torus projection
    x_vals, y_vals, z_vals = [], [], []
    
    for node in nodes:
        # Get 4 pairs of bits
        bits = [(node >> (7 - i)) & 1 for i in range(8)]
        # Convert each pair to angle (0, π/2, π, 3π/2)
        angles = []
        for i in range(0, 8, 2):
            pair_value = (bits[i] << 1) | bits[i+1]
            angles.append(pair_value * np.pi / 2)
        
        # Clifford torus projection: x = cos(θ₁) + cos(θ₂), y = sin(θ₁) + sin(θ₂), z = cos(θ₃) + sin(θ₄)
        x = np.cos(angles[0]) + np.cos(angles[1])
        y = np.sin(angles[0]) + np.sin(angles[1])
        z = np.cos(angles[2]) + np.sin(angles[3])
        
        x_vals.append(x)
        y_vals.append(y)
        z_vals.append(z)
    
    # Create interactive 3D plot
    fig = go.Figure(data=go.Scatter3d(
        x=x_vals, y=y_vals, z=z_vals,
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=colors,
            opacity=0.8,
            line=dict(width=1, color='white')
        ),
        text=[subit_to_name(n).split('_')[0] for n in nodes],
        textposition="top center",
        hovertext=[f"{subit_to_name(n)}<br>ID: {n}<br>Bits: {n:08b}" for n in nodes],
        hoverinfo='text'
    ))
    
    # Update layout (without edges for simplicity)
    fig.update_layout(
        title="SUBIT Clifford Torus – All Archetypes in 3D",
        scene=dict(
            xaxis_title="X = cos(θ₁) + cos(θ₂)",
            yaxis_title="Y = sin(θ₁) + sin(θ₂)",
            zaxis_title="Z = cos(θ₃) + sin(θ₄)",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5),
                up=dict(x=0, y=0, z=1)
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=800,
        width=1200
    )
    
    fig.write_html(output_file)
    print(f"[OK] Clifford torus visualization saved to {output_file}")

def visualize_umap(graph: nx.Graph, output_file: str = "umap.html") -> None:
    """
    Project archetypes into 3D using UMAP (preserves semantic topology).
    Shows how archetypes cluster in a continuous space.
    """
    import plotly.graph_objects as go
    import numpy as np
    from .core import archetype_color, subit_to_name
    
    try:
        import umap
        from sklearn.preprocessing import StandardScaler
    except ImportError:
        print("[WARN] umap-learn not installed. Run: pip install umap-learn scikit-learn")
        return
    
    if len(graph.nodes) < 3:
        print("[WARN] Not enough nodes for UMAP (need at least 3)")
        return
    
    nodes = list(graph.nodes)
    
    # Create feature matrix from 8 bits (0/1)
    features = np.array([[(n >> i) & 1 for i in range(8)] for n in nodes], dtype=np.float32)
    
    # Standardize features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Reduce to 3D with UMAP
    reducer = umap.UMAP(
        n_components=3,
        n_neighbors=min(15, len(nodes) - 1),
        min_dist=0.1,
        random_state=42,
        metric='hamming'  # Use Hamming distance for binary data
    )
    embedding = reducer.fit_transform(features_scaled)
    
    # Normalize embedding to [-1, 1] range for consistent display
    embedding = (embedding - embedding.min(axis=0)) / (embedding.max(axis=0) - embedding.min(axis=0))
    embedding = embedding * 2 - 1
    
    # Prepare visualization
    colors = [archetype_color(n) for n in nodes]
    sizes = [15 + graph.nodes[n].get('count', 0) * 2 for n in nodes]
    names = [subit_to_name(n) for n in nodes]
    
    # Create hover text with archetype info
    hover_texts = []
    for i, node in enumerate(nodes):
        mode = "MICRO" if node == 0b10101010 else "MACRO" if node == 0b11111111 else "MESO" if node == 0b01010101 else "META" if node == 0 else "mixed"
        hover_texts.append(f"{names[i]}<br>ID: {node}<br>Bits: {node:08b}<br>Mode: {mode}")
    
    fig = go.Figure(data=go.Scatter3d(
        x=embedding[:, 0], y=embedding[:, 1], z=embedding[:, 2],
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=colors,
            opacity=0.8,
            line=dict(width=1, color='white')
        ),
        text=[n.split('_')[0][:4] for n in names],
        textposition="top center",
        hovertext=hover_texts,
        hoverinfo='text'
    ))
    
    # Add edges (optional, only if not too many)
    edges = list(graph.edges())
    if len(edges) < 200 and len(edges) > 0:
        # Map node to index in embedding
        node_to_idx = {node: i for i, node in enumerate(nodes)}
        edge_x, edge_y, edge_z = [], [], []
        for u, v in edges:
            if u in node_to_idx and v in node_to_idx:
                i, j = node_to_idx[u], node_to_idx[v]
                edge_x.extend([embedding[i, 0], embedding[j, 0], None])
                edge_y.extend([embedding[i, 1], embedding[j, 1], None])
                edge_z.extend([embedding[i, 2], embedding[j, 2], None])
        
        fig.add_trace(go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(color='gray', width=1),
            hoverinfo='none',
            name='Transitions'
        ))
    
    fig.update_layout(
        title="SUBIT UMAP Projection – Semantic Topology of Archetypes",
        scene=dict(
            xaxis_title="UMAP 1",
            yaxis_title="UMAP 2",
            zaxis_title="UMAP 3",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5),
                up=dict(x=0, y=0, z=1)
            )
        ),
        height=800,
        width=1200
    )
    
    fig.write_html(output_file)
    print(f"[OK] UMAP visualization saved to {output_file}")