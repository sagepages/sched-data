import psycopg2
from decouple import config


class Pipeline:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=config("HOST"),
            database=config("DATABASE"),
            user=config("DBUSER"),
            password=config("PASSWORD"),
        )

        self.cur = self.conn.cursor()

    def drop_existing_table(self):
        self.cur.execute("DROP TABLE Classes")
        self.conn.commit()
        print("Existing table has been dropped...")

    def create_new_table(self):
        self.cur.execute(
            """ create table Classes(
                    classID serial UNIQUE Primary Key,
                    classNbr int,
                    capacity int,
                    enrolled int,
                    startTime time,
                    endTime time,
                    dow varchar(5),
                    subject varchar(10)
            ); """
        )
        self.conn.commit()
        print("New Classes table has been created.")

    def insert_data(self, classesObj):

        statement = """
        INSERT INTO classes
        Values(DEFAULT, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cur.execute(
            statement,
            (
                classesObj["classNbr"],
                classesObj["capacity"],
                classesObj["enrolled"],
                classesObj["startTime"],
                classesObj["endTime"],
                classesObj["dow"],
                classesObj["subject"],
            ),
        )

        self.conn.commit()

    def query_data(self, day, st, et):
        statement = """

        SELECT sum(enrolled) from Classes
        where dow = %s and startTime <= %s and endTime >= %s
        """
        self.cur.execute(statement, (day, st, et))
        result = self.cur.fetchall()
        return result[0][0]

    def queryCSCE(self, day, st, et):
        statement = """
        SELECT sum(enrolled) from Classes
        where subject in ('CAP','COP','CEN','CGS','CIS','COT','COT','MAD','MHF','CDA','CNT','CTS','EEL','IDC','COM','EGN','ESI','TCN', 'BME')
        and dow = %s and startTime <= %s and endTime >= %s
        """

        self.cur.execute(statement, (day, st, et))
        result = self.cur.fetchall()
        return result[0][0]

    def execute_test(self):
        print("PostgreSQL database Version: ")
        self.cur.execute("SELECT version()")
        db_version = self.cur.fetchone()
        print(db_version)


if __name__ == "__main__":
    pipeline = Pipeline()
    # pipline.execute_test()
    print(pipeline.query_data("Mo", "7:00", "7:30")[0][0])
