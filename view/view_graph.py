from neo4j import GraphDatabase
from pyvis.network import Network
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')

driver = GraphDatabase.driver(uri, auth=(user, password))

# Sample Cypher query to retrieve nodes and relationships
cypher_query = """
MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 100
"""

# Execute the query and fetch the results

with driver.session() as session:
    result = session.run(cypher_query)

    net = Network(cdn_resources="remote", directed=True, height='500px', width='100%', notebook=True)

    for record in result:
        node_a = record["n"]
        node_b = record["m"]
        relationship = record["r"]

        # add nodes
        net.add_node(node_a.element_id, label=list(node_a.labels)[0])
        net.add_node(node_b.element_id, label=list(node_a.labels)[0])
        net.add_edge(node_a.element_id, node_b.element_id, title=relationship.type)

# save html format
net.show("out.html", notebook=False)

driver.close()
