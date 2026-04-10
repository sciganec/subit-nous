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
        print("⚠️ Текстові файли не знайдено.")
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
    
    print(f"📊 Graph built: {len(graph.nodes)} archetypes, {graph.number_of_edges()} transitions")
    return graph

def visualize_4d(graph: nx.Graph, output_file: str = "graph.html"):
    """Створює 3D-візуалізацію графа."""
    if not graph.nodes:
        print("⚠️ Немає вузлів для візуалізації.")
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
    print(f"✅ Visualization: {output_file}")