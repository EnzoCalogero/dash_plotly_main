# -*- coding: utf-8 -*-
from py2neo import Graph

from apps import db_onnections

neo4j_config = db_onnections.config(section='neo4j')

neo4j_connector = neo4j_config['connector']

NEO4J_SERVER = "bolt://172.17.0.1:7687" #  "bolt://" + neo4j_connector
#NEO4J_SERVER = "bolt://neo4j:7687" #  "bolt://" + neo4j_connector
#NEO4J_SERVER = "bolt://neo4j:7687"


# Generic Function to interogate the Neo4j DB
def ne4jquery(query):
    graph = Graph(NEO4J_SERVER)
    return graph.run(query).to_data_frame()


# Function for Populating the value for the User Metadata
def neo4j_prop_user_metadata(metadata="Team"):
    if metadata =="_Group":
        q = "MATCH (n:Group) RETURN n.Name"
        k = ne4jquery(query=q)
    else:
        q = "MATCH (n:User) RETURN distinct n.{}".format(metadata)
        k = ne4jquery(query=q)
    return k


#Function for Populating the value for the Devices Metadata
def neo4j_prop_device_metadata(metadata="Team"):
    if metadata =="_Template":
        q = "MATCH (n:Template)  RETURN n.Display_Name"
        k = ne4jquery(query=q)
    else:
        q = "MATCH (n:Device) RETURN distinct n.{}".format(metadata)
        k = ne4jquery(query=q)
    return k


# Function for Filteringing the users
def ne4j_userfilter(column="Employment", metaval="Contractor"):
    if column == "---":
        return 0
    elif column == "_Group":
        q = 'MATCH p=(u:User)-[r:Belong]->(g:Group) where g.Name = "{}" RETURN u.Display_Name'.format(metaval)
        k = ne4jquery(query=q)
        return list(k.iloc[:, 0])
    else:
        q = 'MATCH (n:User) where n.{} = "{}" RETURN distinct n.Display_Name'.format(column, metaval)
        k = ne4jquery(query=q)
        return list(k.iloc[:, 0])


# Function for Filteringing the Devices
def ne4j_devicefilter(column="Location", metaval="Theale"):
    if column == "---":
        return 0
    elif column == "_Template":
        q = '''
            MATCH(n: Template)-[: Associated]-(d:Device)
            where n.Display_Name = "{}"
            RETURN d.HostName
        '''.format(metaval)

        k = ne4jquery(query=q)

        return list(k.iloc[:, 0])
    else:
        q = 'MATCH (n:Device) where n.{} = "{}" RETURN distinct n.HostName'.format(column, metaval)
        k = ne4jquery(query=q)
        return list(k.iloc[:, 0])


if __name__ == "__main__":
   q = "MATCH (n:User)  RETURN distinct n.{}".format("Employment")
   k = ne4jquery(query=q)