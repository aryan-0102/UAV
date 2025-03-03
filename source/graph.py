import pandas as pd
import networkx as nx
import plotly.graph_objects as go


df = pd.read_csv(r'C:\Users\aryan\PycharmProjects\UAV\data\distance_matrix.csv', index_col=0)
df.index = df.index.str.strip()
df.columns = df.columns.str.strip()


G = nx.from_pandas_adjacency(df)


pos = nx.spring_layout(G, seed=51)


edge_x, edge_y = [], []
for u, v in G.edges():
    x0, y0 = pos[u]
    x1, y1 = pos[v]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='#888'),
    hoverinfo='none',
    mode='lines'
)


node_x, node_y, node_text = [], [], []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(node)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=node_text,
    textposition='bottom center',
    marker=dict(size=10, color='skyblue', line_width=2)
)


fig = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        title='Network Graph',
        showlegend=False,
        hovermode='closest',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
)
fig.show()
print("Nodes:", G.nodes())      
print("Edges:", G.edges())
print("Number of Nodes:", G.number_of_nodes())
print("Number of Edges:", G.number_of_edges())
