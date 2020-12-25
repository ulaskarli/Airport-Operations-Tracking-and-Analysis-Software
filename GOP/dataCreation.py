import pandas as pd
import mysql.connector



def refactorData():
    df = pd.read_excel (r'/Users/ulasberkkarli/Desktop/ops.xls')

    cnx = mysql.connector.connect(user='bytechde', password='B100Franklin123',
                                  host='89.252.185.4',
                                  database='bytechde_airport_comp491')
    cursor = cnx.cursor()

    for index,row in df.iterrows():

        sqlite_select_query = """INSERT INTO `ground_operation` (`operation_id`, `is_consecutive`, `is_boarding_stairs`, `plane_parked`, `plane_pushback`, `boarding_started`, `boarding_ended`, `catering_service_started`, `catering_service_ended`, `baggage_started`, `baggage_ended`, `created_on`, `created_by`, `modified_on`, `modified_by`, `video_file_name`) VALUES (NULL, '1', '0', """ \
                          + "'" + row["plane_parked"].strftime('%Y-%m-%d %H:%M:%S') + "'," + "'" + row["plane_pushback"].strftime('%Y-%m-%d %H:%M:%S') + "'," + "'" + row["boarding_started"].strftime('%Y-%m-%d %H:%M:%S') + "'," + "'" + row["boarding_ended"].strftime('%Y-%m-%d %H:%M:%S') + "'," + "'" + row["catering_service_started"].strftime('%Y-%m-%d %H:%M:%S') + "'," + "'" + row["catering_service_ended"].strftime('%Y-%m-%d %H:%M:%S') + "'," + "'" + row["baggage_started"].strftime('%Y-%m-%d %H:%M:%S') + "',"+ "'" + row["baggage_ended"].strftime('%Y-%m-%d %H:%M:%S') + "', current_timestamp(), 'SYSTEM', NULL, NULL, '')"

        print(sqlite_select_query)


        cursor.execute(sqlite_select_query)


if __name__ == "__main__":
   refactorData()