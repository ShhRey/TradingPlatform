import pymongo

client = pymongo.MongoClient('mongodb://mongodbuser:')
db = client['TradeKeen']

col1 = db['Users']
col2 = db['Admins']
col3 = db['Wallets']
col4 = db['Markets']
col5 = db['Exchanges']
col6 = db['User_APIs']
col7 = db['Strategies']
col8 = db['BS_Live_Orders']
col9 = db['BF_Live_Orders']
col10 = db['Paper_APIs']
