from collections import defaultdict
from pyvis.network import Network
import pandas as pd

def construct_network(df):
    
    g = Network("800px", "100%", bgcolor="#3c4647", font_color="white")
    for artist in df.artist:
        g.add_node(artist, label=artist, color="#26d18f")
    for related in df.related:
        g.add_node(related, label=related, color="#8965c7")
    g.add_edges(list(zip(df.artist, df.related)))
    counts = df.related.value_counts()
    for node in g.nodes:
        freq = str(counts.get(node['id'], 1))
        # nodes with a value will scale their size
        # nodes with a title will include a hover tooltip on the node
        node.update({"value": freq, "title": f"Frequency: {freq}"})
    g.inherit_edge_colors("to")
    for e in g.edges:
        edge_label = f'{e["from"]} ---> {e["to"]}'
        e.update({"title": edge_label})
    g.barnes_hut(
        gravity=-17950,
        central_gravity=4.1,
        spring_length=220,
        spring_strength=.140,
        damping=.66,
        overlap=1
    )
    g.show("spotify_example.html")

if __name__ == "__main__":
    artists_connected = pd.read_csv("spotify_data.csv")
    construct_network(artists_connected)