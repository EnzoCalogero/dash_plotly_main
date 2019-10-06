#!/usr/bin/python
def customer_templatesinglefile(path):
    # Crete the Dataframes for the Templates analytics
    templ=templateDB()

    templ.to_csv('data/templetes_all.csv'.format(path))
    templ=CreateDataframetemplatesinglefile(path=path)
    templ.to_csv('data/templetes_allbis.csv'.format(path))
    return 0


def customer_loadingsinglefile(path):
    # Crete the list of the customers available
    df= dictDB()
    df.to_csv('data/dblist.csv'.format(path))
    return 0


def CreateDataframetemplatesinglefile(path):
    df = pd.read_csv('data/templetes_all.csv'.format(path))
    #Remapping the name of the customer from its hash
    dblist = pd.read_csv('data/dblist.csv'.format(path))
    translation = dict(zip(dblist.Hash, dblist.DB))

    df['DB'] = df['db'].map(translation)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_at'] = df['created_at'].dt.date
    return df


from  import_steams import *
if __name__ == '__main__':
    path = ""

    customer_loadingsinglefile(path=path)
    print('loading')

    customer_templatesinglefile(path)