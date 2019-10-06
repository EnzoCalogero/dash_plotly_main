# -*- coding: utf-8 -*-
from neo4j.v1 import GraphDatabase
import populating
import postgress_connections
#driver = GraphDatabase.driver('bolt://10.9.99.66:7687')  # To be use from Pysharm
driver = GraphDatabase.driver('bolt://neo4j:7687') # To be use for Docker-compose

def main():

    #####################
    #    Creating the   #
    #    Constrains     #
    #####################
    constrains = ["CREATE CONSTRAINT ON (n:User) ASSERT n.Name IS UNIQUE;",
                  "CREATE CONSTRAINT ON (n:User) ASSERT n.Display_Name IS UNIQUE;",
                  "CREATE CONSTRAINT ON (n:Group) ASSERT n.Name IS UNIQUE;",
                  "CREATE CONSTRAINT ON (n:Profile) ASSERT n.Display_Name IS UNIQUE;",
                  "CREATE CONSTRAINT ON (n:Profile) ASSERT n.Name IS UNIQUE;",
                  "CREATE CONSTRAINT ON (n:Device) ASSERT n.Name IS UNIQUE;",
                  "CREATE CONSTRAINT ON (n:Device) ASSERT n.HostName IS UNIQUE;",
                  "CREATE CONSTRAINT ON (n:Task) ASSERT n.Name IS UNIQUE;",
                  "CREATE CONSTRAINT ON (n:Task) ASSERT n.Display_Name IS UNIQUE;",
                  "CREATE CONSTRAINT ON (n:Tool) ASSERT n.Name IS UNIQUE;",
                  "CREATE CONSTRAINT ON (n:Tool) ASSERT n.Display_Name IS UNIQUE;",
                  "CREATE CONSTRAINT ON (n:Template) ASSERT n.Name IS UNIQUE;",
                  "CREATE CONSTRAINT ON (n:Template) ASSERT n.Display_Name IS UNIQUE;"]
    sess = driver.session()
    for con in constrains:

        _ = sess.run(con)

    #####################
    # Creating the CSVs #
    #####################
    postgress_connections.profiles()
    postgress_connections.devices()
    postgress_connections.Profile_devices()
    postgress_connections.user_group()
    postgress_connections.profile_group()
    postgress_connections.profile_users()
    postgress_connections.profile_tasks()
    postgress_connections.profile_tools()
    postgress_connections.templates_device()
    postgress_connections.templates_tools()
    postgress_connections.templates_tasks()

    ######################
    # Importing the CSVs #
    ######################
    importers = ["""
LOAD CSV WITH HEADERS FROM  'file:///profiles.csv' AS line
CREATE (:Profile {Name: line.name, Display_Name: line.display_name})
                 """,
                 """
LOAD CSV WITH HEADERS FROM  'file:///devices.csv' AS line
CREATE (:Device {Name: line.name, HostName: line.hostname})
                 """,
                 """
                 LOAD CSV WITH HEADERS FROM "file:///prof_devices.csv" AS csvLine
MERGE (profile:Profile {Name: csvLine.profile_name,Display_Name: csvLine.prof_display })
MERGE (device:Device {Name:  csvLine.device_name, HostName: csvLine.hostname})
CREATE (profile)-[:Allow]->(device)
                 """,
                 """
                 LOAD CSV WITH HEADERS FROM "file:///user_group.csv" AS csvLine
MERGE (user:User {Name: csvLine.username, Display_Name: csvLine.userdispalyname })
MERGE (group:Group {Name:  csvLine.group_name})
CREATE (user)-[:Belong]->(group)
                 """,
                 """
                 LOAD CSV WITH HEADERS FROM "file:///prof_group.csv" AS csvLine
MERGE (profile:Profile {Name: csvLine.profile_name, Display_Name: csvLine.prof_display })
MERGE (group:Group {Name:  csvLine.group_name})
CREATE (group)-[:Linked]->(profile)
                 """,
                 """
                 LOAD CSV WITH HEADERS FROM "file:///prof_users.csv" AS csvLine
MERGE (user:User {Name: csvLine.username, Display_Name: csvLine.userdispalyname })
MERGE (profile:Profile {Name: csvLine.profile_name, Display_Name: csvLine.prof_display })
CREATE (user)-[:Linked]->(profile)
                 """,
                 """
                 LOAD CSV WITH HEADERS FROM "file:///profile_tasks.csv" AS csvLine
MERGE (profile:Profile {Name: csvLine.profile_name, Display_Name: csvLine.profile_display_name})
MERGE (task:Task {Name: csvLine.task_name, Display_Name: csvLine.task_display_name})
CREATE (profile)-[:Action]->(task)
                 """,
                 """
                 LOAD CSV WITH HEADERS FROM "file:///profile_tools.csv" AS csvLine
MERGE (profile:Profile {Name: csvLine.profile_name, Display_Name: csvLine.profile_display_name})
MERGE (tool:Tool {Name: csvLine.tool_name, Display_Name: csvLine.tool_display_name})
CREATE (profile)-[:Action]->(tool)
                 """,
                 """
                 LOAD CSV WITH HEADERS FROM "file:///templates_device.csv" AS csvLine
MERGE (device:Device {Name:  csvLine.name_device, HostName: csvLine.dev_hostname})
MERGE (template:Template {Name: csvLine.teml_name, Display_Name: csvLine.teml_display_name})
CREATE (template)-[:Associated]->(device);
                 """,
                 """
                 LOAD CSV WITH HEADERS FROM "file:///templates_tools.csv" AS csvLine
MATCH (template:Template {Name: csvLine.devicetemplates_name, Display_Name: csvLine.devicetemplates_display_name})
MERGE (tool:Tool {Name: csvLine.tool_name, Display_Name: csvLine.tool_display_name})
CREATE (template)-[:Action]->(tool);
                 """,
                 """
                 LOAD CSV WITH HEADERS FROM "file:///templates_tasks.csv" AS csvLine
MATCH (template:Template {Name: csvLine.devicetemplates_name, Display_Name: csvLine.devicetemplates_display_name})
MERGE (task:Task {Name: csvLine.task_name, Display_Name: csvLine.task_display_name})
CREATE (template)-[:Action]->(task);
                 """
                 ]

    for i in importers:
    #    print(i)

        _ = sess.run(i)

    print(" Adding Metadata")
    populating.populating_metadata_devices()
    populating.populating_metadata_users()
    populating.populating_metadata_profiles()
    populating.entity_builder()
    print(" Added Metadata")


#if __name__ == "__main__":
#print("Main Starting")
main()
#print("Main Ending")
