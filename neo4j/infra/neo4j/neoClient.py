from py2neo import Graph, Relationship, Node

# from config.base import *
NEO4J_URL = "http://172.25.67.143:7476"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "asdc_2023"
NEO4J_DB = "neo4j"


def graph_conn():
    graph = Graph(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASSWORD), name=NEO4J_DB)
    return graph


if __name__ == "__main__":
    node_1 = Node(label="book", name="黄帝内经")
    node_2 = Node(label="book", name="伤寒论")
    node_1_include_node_2 = Relationship(node_1, "包括", node_2)
