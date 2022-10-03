from CourseScraper import CourseScraper
from Pipeline import Pipeline
from multiprocessing.pool import Pool


def handleSubjectAndInsertToDB(subj):

    results = CourseScraper.startScraping(subj)
    pipeline = Pipeline()
    for res in results:
        pipeline.insert_data(res)
        print(f"Wrote new entry: {res} ")


def main():

    pipeline = Pipeline()
    pipeline.execute_test()
    pipeline.drop_existing_table()
    pipeline.create_new_table()

    subjectList = CourseScraper.getListOfSubjects()
    # create and configure the process pool
    with Pool() as pool:
        # execute tasks in order
        for subj in pool.map(handleSubjectAndInsertToDB, subjectList):
            print(f"Subject: {subj} has been completed.", flush=True)
    # process pool is closed automatically


if __name__ == "__main__":
    print(
        """
          _              _                                         
 ___  ___| |__   ___  __| |      ___  ___ _ __ __ _ _ __   ___ _ __ 
/ __|/ __| '_ \ / _ \/ _` |_____/ __|/ __| '__/ _` | '_ \ / _ \ '__|
\__ \ (__| | | |  __/ (_| |_____\__ \ (__| | | (_| | |_) |  __/ |   
|___/\___|_| |_|\___|\__,_|     |___/\___|_|  \__,_| .__/ \___|_|   
                                                   |_|
            """
    )
    main()
