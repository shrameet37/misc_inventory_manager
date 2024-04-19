import os
import psycopg2

DG_DB_USER = os.environ["DG_DB_USER"]
DG_DB_PASSWORD = os.environ["DG_DB_PASSWORD"]
DG_DB_HOST = os.environ["DG_DB_HOST"]
DG_DB_PORT = os.environ["DG_DB_PORT"]
DG_DB_NAME = os.environ["DG_DB_NAME"]

HM_DB_USER = os.environ["HM_DB_USER"]
HM_DB_PASSWORD = os.environ["HM_DB_PASSWORD"]
HM_DB_HOST = os.environ["HM_DB_HOST"]
HM_DB_PORT = os.environ["HM_DB_PORT"]
HM_DB_NAME = os.environ["HM_DB_NAME"]

dgDbConnection = None
hmDbConnection = None

def getDgDbConnection():

    global dgDbConnection
    
    if dgDbConnection is None:
        dgDbConnection = psycopg2.connect(user=DG_DB_USER,password=DG_DB_PASSWORD,host=DG_DB_HOST,port=DG_DB_PORT,database=DG_DB_NAME)

    return dgDbConnection

def getHmDbConnection():

    global hmDbConnection
    
    if hmDbConnection is None:
        hmDbConnection = psycopg2.connect(user=HM_DB_USER,password=HM_DB_PASSWORD,host=HM_DB_HOST,port=HM_DB_PORT,database=HM_DB_NAME)

    return hmDbConnection