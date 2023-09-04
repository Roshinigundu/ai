from neo4j import GraphDatabase

class Neo4jDriver:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def add_node(self, node_type, node_name):
        with self._driver.session() as session:
            session.write_transaction(self._add_node, node_type, node_name)

    def add_relationship(self, node1_name, relationship_type, node2_name):
        with self._driver.session() as session:
            session.write_transaction(self._add_relationship, node1_name, relationship_type, node2_name)

    @staticmethod
    def _add_node(tx, node_type, node_name):
        query = f"CREATE (:Node {{type: '{node_type}', name: '{node_name}'}})"
        tx.run(query)

    @staticmethod
    def _add_relationship(tx, node1_name, relationship_type, node2_name):
        query = (
            f"MATCH (n1:Node {{name: '{node1_name}'}}), (n2:Node {{name: '{node2_name}'}}) "
            f"CREATE (n1)-[:{relationship_type}]->(n2)"
        )
        tx.run(query)

# Usage example
uri = "bolt://localhost:7687"
user = "your_username"
password = "your_password"

driver = Neo4jDriver(uri, user, password)

# Add nodes and relationships
driver.add_node("Government", "GovernmentEntityName")
driver.add_node("Company", "CompanyName")
driver.add_relationship("GovernmentEntityName", "collaborates_with", "CompanyName")

# Close the Neo4j driver when done
driver.close()
