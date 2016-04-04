#########connect to db
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

def connect():
    engine = create_engine('postgresql://ljrconnell:rocco1!1@liamsdatabase.cbjwfk4y5vix.us-east-1.rds.amazonaws.com:5432/firstdb')
    conn = engine.connect()     #do I need this?
    metadata = MetaData(bind=engine)
    return engine, conn, metadata

########get fin data
import pandas as pd
from pandas.io.data import DataReader

from datetime import datetime

def get_data(ticker, start, end):
    data = DataReader(ticker,'yahoo', start, end)
    return data

def format_findata(df, ticker):
    df['Price']=df['Adj Close']
    df = df['Price']
    df = pd.DataFrame(df)
    df['Ticker'] = ticker
    return df

def get_formated_data(ticker, start, end):
    return format_findata(get_data(ticker, start, end), ticker)


########put data on DB
from sqlalchemy import Table, Column, Integer, String, Date, MetaData, ForeignKey
import pandas as pd

def put_fin_data(tablename, data, conn, metadata):
    table = Table(tablename, metadata,
        Column('Date', Date, primary_key=True),
        Column('Price', Integer)
    )
    data['Adj Close'].to_sql(tablename, conn) 
    return

##########get fin data from DB
import pandas as pd
from sqlalchemy.sql import select

def get_DB_data(tablename, conn, query=None):
    if query==None:
        query = ''.join(('SELECT * FROM ', tablename))
    data = pd.read_sql(query, conn)#, index_col='Date')
    return data

###########get all symbols
import get_symbols
import pandas as pd
from sqlalchemy import Table, Column, Integer, Boolean, String, Date, MetaData, ForeignKey

def upload_symbols(tblname, metadata, conn):
    symbols=get_symbols.main()
    df = pd.DataFrame()
    df['symbols'] = symbols
    df['uptodate'] = False
#    df.index = df.symbols
    print(df)
    ##Put on database
    table = Table(tblname, metadata, 
        Column('symbol', String, primary_key=True),
        Column('uptodate', Boolean, nullable=False)
    )
    df.to_sql(tblname, conn, if_exists='replace')

