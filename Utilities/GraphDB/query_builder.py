from py2neo import Graph
import pandas as pd
q = 'match (a1:User)-[r]-(a2) where a1.Employment= "Permanent" return DISTINCT a1.Name'


def ne4jquery(query=q):
    graph = Graph("'bolt://localhost:7687", auth=("neo4j", "enzo"))

    ######################
    # Queries Side      ##
    ######################

    #query = 'match (a1:User)-[r]-(a2) where a1.Employment= "Permanent" return DISTINCT a1.Name'
    k = graph.run(query).to_data_frame()
    return(k)


def ne4jquery(query=q):
    graph = Graph("'bolt://localhost:7687") #, auth=("neo4j", "psswrd"))

    ######################
    # Queries Side      ##
    ######################

    #query = 'match (a1:User)-[r]-(a2) where a1.Employment= "Permanent" return DISTINCT a1.Name'
    k = graph.run(query).to_data_frame()
    return(k)

if __name__ == "__main__":
   q='MATCH (n:User) where n.{}="{}" RETURN distinct n.Display_Name'.format("Employment", "Permanent")
   k = ne4jquery(query=q)
