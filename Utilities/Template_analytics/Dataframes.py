import pandas as pd
from datetime import datetime as dt

def CreateDataframeCache(path):
    df=pd.read_csv('{}/data/session_.csv'.format(path))

    #Generic Cleaning Data
    col=str(df.columns)
    col=col.replace(' ', '').replace('\n','').replace("'","").replace('Index([','').replace('],dtype=object)','')
    df.columns=col.split(',')
    df['display_name']=df['display_name'].str.strip()
    df['subnet']=df['subnet'].str.strip()
    df['peer_address']=df['peer_address'].str.strip()
    df['created_at']=pd.to_datetime(df['created_at'])

    df=df[df['created_at']>="2018-01-01  00:00:00.000000"]

    df['WDay'] = df['created_at'].dt.weekday_name
    df['WDay'] = df['WDay'].astype('category',
                                   categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", 'Sunday',
                                               'Saturday'], ordered=False)
    # Extending the dataframe
    nuovo = pd.DataFrame()
    for index, row in df.iterrows():
        valori = [x for x in range(int(row['hourin']), int(row['hourout']) + 1)]
        for i in valori:
            row['hourin'] = i
            nuovo = nuovo.append(row)
    df = nuovo

    #Remapping the name of the cusstomer from its hash
    dblist = pd.read_csv('{}/data/dblist.csv'.format(path))
    translation = dict(zip(dblist.Hash, dblist.DB))
    df['DB'] = df['db'].map(translation)

    df['Duration'] = df.hourout - df.hourin
    df['WDay'] = df['created_at'].dt.weekday_name
    df['WDay'] = df['WDay'].astype('category',
                                   categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", 'Sunday',
                                               'Saturday'], ordered=False)
    return df


def CreateDataframesession(path):
    df=pd.read_csv('{}/data/session_.csv'.format(path))
    #Generic Cleaning Data
    col=str(df.columns)
    col=col.replace(' ', '').replace('\n','').replace("'","").replace('Index([','').replace('],dtype=object)','')
    df.columns=col.split(',')
    df['display_name']=df['display_name'].str.strip()
    df['subnet']=df['subnet'].str.strip()
    df['peer_address']=df['peer_address'].str.strip()
    df['created_at']=pd.to_datetime(df['created_at'])

    df['WDay'] = df['created_at'].dt.weekday_name
    df['WDay'] = df['WDay'].astype('category',
                                   categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", 'Sunday',
                                               'Saturday'], ordered=False)
     #Remapping the name of the cusstomer from its hash
    dblist = pd.read_csv('{}/data/dblist.csv'.format(path))
    translation = dict(zip(dblist.Hash, dblist.DB))
    df['DB'] = df['db'].map(translation)

    df['Duration'] = df.hourout - df.hourin
    df['WDay'] = df['created_at'].dt.weekday_name
    df['WDay'] = df['WDay'].astype('category',
                                   categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", 'Sunday',
                                               'Saturday'], ordered=False)
    return df


def CreateDataframeChannel(path):
    df = pd.read_csv('{}/data/Channels_.csv'.format(path))
    df = df[['device', 'devicetype_id', 'display_name', 'hostname', 'access_role_id', 'protocol', 'db']]
    df['devicetype_id'] = df['devicetype_id'].astype('category', ordered=True)
    typeList = [1, 16, 17, 20, 21]
    elelmenti = "firewall,linuxserver,windows,other,hypervisor".split(',')
    translation = dict(zip(typeList, elelmenti))
    df['devicetype_id'] = df['devicetype_id'].map(translation)
    df['display_name'] = df['display_name'].apply(lambda x: str(x).strip())
    df['protocol'] = df['protocol'].apply(lambda x: str(x).strip())
    df['hostname'] = df['hostname'].apply(lambda x: str(x).strip())

    # Remapping the name of the customer from its hash
    dblist = pd.read_csv('{}/data/dblist.csv'.format(path))
    translation = dict(zip(dblist.Hash, dblist.DB))

    df['DB'] = df['db'].map(translation)

    return df


def CreateDataframetemplate(path):
    df = pd.read_csv('{}/data/templetes_.csv'.format(path))
    #Remapping the name of the customer from its hash
    dblist = pd.read_csv('{}/data/dblist.csv'.format(path))
    translation = dict(zip(dblist.Hash, dblist.DB))

    df['DB'] = df['db'].map(translation)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_at'] = df['created_at'].dt.date
    return df


def CreateDataframetasks(path):
    df = pd.read_csv('{}/data/tasks_.csv'.format(path))
    #Remapping the name of the cusrstomer from its hash
    dblist = pd.read_csv('{}/data/dblist.csv'.format(path))
    translation = dict(zip(dblist.Hash, dblist.DB))
    df['DB'] = df['db'].map(translation)

    df['event_time'] = pd.to_datetime(df['event_time'])
    df['event_time'] = df['event_time'].dt.date
    df=df[df['last_event']=='SUCCESS']
    df = df[df['display_name'] != 'Osirium Server']
    df['args.task_name']=df['task_name']
    df['name'] = df['task_name']
    df['args.actioned_by_username'] = df['display_name']
    df['args.device_display_name'] = df['device_name']

    df=df[['name','args.task_name', 'args.actioned_by_username','args.device_display_name','event_time','db','DB']]
    return df


def CreateDataframeGraphCharts(path):
    df = pd.read_csv('{}/data/Graph_.csv'.format(path))
    #Remapping the name of the cusrstomer from its hash
    dblist = pd.read_csv('{}/data/dblist.csv'.format(path))
    #dblist['nameWithDate']="{}-_-{}".format(dblist.DB,dblist.Date)
    #dblist['DB']=str(dblist['DB'])
    #dblist['Date'] = str(dblist['Date'])

    dblist['nameWithDate'] = dblist[['DB', 'Date']].apply(lambda x: '_-_'.join(x), axis=1)
    translation = dict(zip(dblist.Hash,dblist.nameWithDate))#, dblist.DB))
    df['DB'] = df['db'].map(translation)

    df=df[['devicetype_id','display_name','hostname','account','protocol','dursession','durchanel','peer_address','subnet','channel_count','templatename','dispalynametemp','typeslname','typesdisplayname','vendor','db','DB']]
    return df
