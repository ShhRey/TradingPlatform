import pymongo

client = pymongo.MongoClient('mongodb://mongodbuser:wpytGAfnq%40%24%23P93Yt2y@mongo.profitsla.com:27017/?authMechanism=DEFAULT')
db = client['TradeKeen']

col1 = db['Users']
col2 = db['Admins']
col3 = db['Wallets']
col4 = db['Markets']
col5 = db['Exchanges']
col6 = db['User_APIs']
col7 = db['Strategies']