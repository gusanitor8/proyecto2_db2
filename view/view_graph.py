from neo4j import GraphDatabase
from pyvis.network import Network
import webbrowser
import os


def display_trans_history(session, node_info):
    def make_query(node_info_):
        query = f"""
        MATCH (n:Cuenta{{ {node_info_['key_property']}: {node_info_['key_value']} }} )-[r:TRANSACCION]->(m:Cuenta)
        RETURN n, r, m
        """
        return query

    query = make_query(node_info)
    result = session.run(query)
    net = Network(cdn_resources="remote", directed=True, height='1000px', width='100%', notebook=True)

    for record in result:
        node_a = record["n"]
        node_b = record["m"]
        relationship = record["r"]

        # add nodes
        net.add_node(node_a.element_id, label='Cuenta: ' + str(node_a._properties['no_cuenta']))
        net.add_node(node_b.element_id, label='Cuenta: ' + str(node_b._properties['no_cuenta']))
        net.add_edge(node_a.element_id, node_b.element_id, title=relationship.type, label='QTQ ' + str(relationship._properties['monto']))

    net.show("out.html", notebook=False)
    current_path = os.getcwd()
    webbrowser.open('file://' + current_path + '/out.html')
