import sys
sys.path.append('../')
from fns import *

engine, conn, metadata = connect()
tblname = 'symballs2'
upload_symbols(tblname,metadata, conn)
metadata.reflect()
symbolsDF = get_DB_data(tblname, conn)

print(symbolsDF.head())

big_table = Table('pricedata_t1', metadata,
    Column('Date', Date, nullable=False),
    Column('Price', Integer, nullable=False),
    Column('Ticker', String, nullable=False)
)

start='2010-01-01'
end = '2016-03-16'
for i in range(len(symbolsDF)):
    print(symbolsDF.iloc[i].symbols)
    symbol= symbolsDF.iloc[i].symbols
 #   print(symbol)
    df = get_formated_data(symbol, start, end)
    df.to_sql('pricedata_t1', conn, if_exists='append')
