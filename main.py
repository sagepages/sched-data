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
|\   ____\|\   ____\|\  \|\  \|\   ___ \               |\   ____\|\   __  \|\  \     |\  ___ \ |\   ____\\___   ___\\   __  \    
\ \  \___|\ \  \___|\ \  \\\  \ \  \_|\ \  ____________\ \  \___|\ \  \|\  \ \  \    \ \   __/|\ \  \___\|___ \  \_\ \  \|\  \   
 \ \_____  \ \  \    \ \   __  \ \  \ \\ \|\____________\ \  \    \ \  \\\  \ \  \    \ \  \_|/_\ \  \       \ \  \ \ \   _  _\  
  \|____|\  \ \  \____\ \  \ \  \ \  \_\\ \|____________|\ \  \____\ \  \\\  \ \  \____\ \  \_|\ \ \  \____   \ \  \ \ \  \\  \| 
    ____\_\  \ \_______\ \__\ \__\ \_______\              \ \_______\ \_______\ \_______\ \_______\ \_______\  \ \__\ \ \__\\ _\ 
   |\_________\|_______|\|__|\|__|\|_______|               \|_______|\|_______|\|_______|\|_______|\|_______|   \|__|  \|__|\|__|
   \|_________|                                                                                                                  
            """
    )
    main()
