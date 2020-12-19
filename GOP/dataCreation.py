import pandas as pd
import numpy as np
import mysql.connector


# Load data
df = pd.read_csv(
    "https://raw.githubusercontent.com/roberthryniewicz/datasets/master/airline-dataset/flights/flights.csv",
    low_memory=False,
)

def writeToDB(df,airports):
    cnx = mysql.connector.connect(user='bytechde', password='B100Franklin123',
                                  host='89.252.185.4',
                                  database='bytechde_airport_comp491')
    cursor = cnx.cursor()

    for line in df:
        print(line)


    time=dict["plane"]["end"].strftime('%Y-%m-%d %H:%M:%S')
    sqlite_select_query ="""INSERT INTO ground_operation (operation_id, plane_parked) VALUES (6, """+"'"+time+"')"


    cursor.execute(sqlite_select_query)

def getCSV():
    cnx = mysql.connector.connect(user='bytechde', password='B100Franklin123',
                                  host='89.252.185.4',
                                  database='bytechde_airport_comp491')
    cursor = cnx.cursor()

    sqlite_select_query = """SELECT * FROM ground_operation WHERE plane_parked <= """+""""2020-12-"""+str(21)+"""" AND plane_parked >= """+""""2020-12-"""+str(20)+"""" """

    stringTest="""SELECT * FROM ground_operation WHERE plane_parked >= "2020-01-4" """

    query = """SELECT * FROM flight WHERE planned_departure_time <= """ + """"2020-12-""" + str(30) + """" AND planned_departure_time >= """ + """"2020-12-""" + str(1) + """" AND is_delayed = "N" """

    print(query)

    cursor.execute(query)

    airports=cursor.fetchall()

    print(airports.__len__())

if __name__ == "__main__":
    getCSV()
