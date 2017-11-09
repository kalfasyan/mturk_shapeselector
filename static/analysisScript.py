from sqlalchemy import create_engine, MetaData, Table
import json
import pandas as pd

#db_url = "mysql://username:password@host.org/database_name"
#db_url = "mysql://rsd:CognizanT@bluemoonF.cvvfhjuzanct.us-west-2.rds.amazonaws.com:3306/psiData"
db_url = "sqlite:///participantsTest.db"
table_name = 'psiExpfinal_data11'
data_column_name = 'datastring'
# boilerplace sqlalchemy setup
engine = create_engine(db_url)
metadata = MetaData()
metadata.bind = engine
table = Table(table_name, metadata, autoload=True)
# make a query and loop through
s = table.select()
rows = s.execute()

data = []
#status codes of subjects who completed experiment
statuses = [3,4,5,7]
# if you have workers you wish to exclude, add them here
exclude = []
for row in rows:
    # only use subjects who completed experiment and aren't excluded
    if row['status'] in statuses and row['uniqueid'] not in exclude:
        data.append(row[data_column_name])

# parse each participant's datastring as json object
# and take the 'data' sub-object
data = [json.loads(part)['data'] for part in data]

# insert uniqueid field into trialdata in case it wasn't added
# in experiment:
for part in data:
    for record in part:
        record['trialdata']['uniqueid'] = record['uniqueid']

# flatten nested list to create a list of the trialdata recorded
# each time psiturk.recordTrialData(trialdata) was called.
data = [record['trialdata'] for part in data for record in part]


# Put all subjects' trial data into a dataframe object from the
# 'pandas' python library
data_frame = pd.DataFrame(data)
data_frame.to_csv('/data/local/tempz/resultsFinal_exp11.csv');
