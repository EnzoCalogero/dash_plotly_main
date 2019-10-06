# -*- coding: utf-8 -*-
import DBQueries

##########################
# Collect dataframe DBs  #
##########################
dbs = DBQueries.dictDB()

dbs = dbs.sort_values(['DB', 'Date'], ascending=[True, False])
dbs = dbs.groupby('DB').first().reset_index()

with open('data/current.ini', 'w') as the_file:
    the_file.write('[DBs]\n')
    the_file.write('number={}\n'.format(len(dbs)))
    the_file.write('[first_edition]\n')
    the_file.write('host=database\n')
    the_file.write('database=enzo\n')
    the_file.write('user=postgres\n')
    the_file.write('port=5432\n')

    for index, row in dbs.iterrows():
        the_file.write('[{}]\n'.format(row['DB']))
        the_file.write('host=10.9.0.50\n')
        the_file.write('database={}\n'.format(row['Hash']))
        the_file.write('user=postgres\n')
        the_file.write('port=5432\n')
        the_file.write('password=xxxxxx\n')
    the_file.write('[ElasticSearch]\n')
    # the_file.write('server=elk.enzo.net\n')
    the_file.write('server=10.9.0.200\n')
    the_file.write('index_name=first_edition*\n')
    the_file.write('filter_host=first_edition.enzo.net\n')
the_file.close()
