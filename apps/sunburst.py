# -*- coding: utf-8 -*-
import pandas as pd
from datetime import timedelta
import datetime
from apps import general_configurations


def templates_sunburts(db):
    from apps import db_onnections
    #print("###################################################################")
    #print(db)
    #print("###################################################################")

    #######################################################
    # Queries Needed for Creating the Sunburst Charts     #
    #######################################################
    FROM = (pd.to_datetime(datetime.datetime.now()) - timedelta(days=120)).strftime("%Y-%m-%d")
    #print(FROM)

    #######################################################
    # Queries Needed for Creating the Sunburst Charts     #
    #######################################################

    #################
    # First Layer   #
    #################
    query01 = '''
    select types.name as typeslName, count(ch.deleted_at)
         from channels ch,devices dev,devicetemplates templ, devicetypes types,devicevendors vendor 
    where ch.device_id=dev.id and dev.devicetemplate_id=templ.id
    and vendor.id= templ.devicevendor_id and types.id = templ.devicetype_id
    and ch.deleted_at >  '{} 00:00:00.000000'
    group by types.name;
    '''.format(FROM)

    #################
    # Second Layer  #
    #################
    query02 = '''
    select count(ch.deleted_at), lower(types.name) as typeslName, lower(vendor.name) as vendor
        from channels ch,devices dev,devicetemplates templ, devicetypes types,devicevendors vendor 
    where ch.device_id=dev.id and dev.devicetemplate_id=templ.id
    and vendor.id= templ.devicevendor_id and types.id = templ.devicetype_id 
    and ch.deleted_at >  '{} 00:00:00.000000'
    group by lower(vendor.name), lower(types.name);
    '''.format(FROM)

    #################
    # Third Layer   #
    #################
    query03 = '''
    select count(ch.deleted_at), lower(types.name) as typeslName, lower(vendor.name) as vendor,
    lower(templ.display_name) as dispalynameTemp 
             from channels ch,devices dev,devicetemplates templ, devicetypes types,devicevendors vendor 
    where ch.device_id=dev.id and dev.devicetemplate_id=templ.id
    and vendor.id= templ.devicevendor_id and types.id = templ.devicetype_id
    and ch.deleted_at >  '{} 00:00:00.000000'
    group by vendor.name, types.name,templ.display_name ;
    '''.format(FROM)

    #######################
    # HTML components     #
    #######################

    ##########################
    #  Building the Charts   #
    ##########################

    # First Layer
    first_layer = db_onnections.runquery(query01, section=db)
    first_layer['count'] = first_layer['count'].apply(str)

    first_layer['dato'] = "{name: '" + first_layer.typeslname + "', value: " + first_layer['count']

    # Second Layer
    second_layer = db_onnections.runquery(query02, section=db)
    second_layer['count'] = second_layer['count'].apply(str)

    second_layer['dato'] = "{name: '" + second_layer.vendor + "', value: " + second_layer['count']

    # Third Layer
    third_layer = db_onnections.runquery(query03, section=db)

    third_layer['count'] = third_layer['count'].apply(str)
    third_layer['dato'] = "{name: '" + third_layer.dispalynametemp + "', value: " + third_layer['count'] + "}"

    ############################################
    #  Creating the data element for the chart #
    ############################################
    text = 'var data = ['
    for index, row in first_layer.iterrows():
        text = text + row['dato'] + ','
        temploc = second_layer[second_layer['typeslname'] == row['typeslname']]
        if not temploc.empty:
            text2 = 'children: ['
            for index2, row2 in temploc.iterrows():
                text2 = text2 + row2['dato'] + ','
                lastloc = third_layer[third_layer['vendor'] == row2['vendor']]
                if not lastloc.empty:
                    text3 = 'children: ['
                    for index3, row3 in lastloc.iterrows():
                        text3 = text3 + row3['dato'] + ','
                    text3 = text3 + '],'
                    text2 = text2 + text3
                text2 = text2 + '},'
            text2 = text2 + ']'
            text = text + text2
        text = text + "},"
    text = text + '];'

    return text
