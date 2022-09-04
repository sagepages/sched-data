import requests
from bs4 import BeautifulSoup
from datetime import datetime


class CourseScraper:
    def getListOfSubjects():
        page = requests.get(
            "https://m.fiu.edu/catalog/index.php?action=subjectList&letter="
        )
        soup = BeautifulSoup(page.content, "html5lib")
        response = soup.find_all("div", attrs={"class": "listButton listButton35"})
        subjectList = []
        for row in response:
            subjectList.append(row.text)
        return subjectList

    def getListOfCourseNumbersFromSubjectList(subj):
        page = requests.get(
            "https://m.fiu.edu/catalog/index.php?"
            + "action=courseList&subject={subj}".format(subj=subj)
        )
        soup = BeautifulSoup(page.content, "html5lib")
        courseList = soup.find_all("div", attrs={"class": "listButton listButton55"})
        courseNumberList = []
        for course in courseList:
            courseInfo = course.text.split()
            courseNumberList.append(courseInfo[1])

        return courseNumberList

    def getListOfLinksToCourses(subj, courseNumberList):

        links = []
        for number in courseNumberList:

            # ---------------------------------------------------------#
            # Change the path variable strm to the current semester    #
            # ---------------------------------------------------------#

            pageURL = (
                "https://m.fiu.edu/catalog/index.php?"
                + "action=sectionList&subject={subj}"
                + "&number={number}&crseId=&strm=1228"
            ).format(subj=subj, number=number)

            page = requests.get(pageURL)
            soup = BeautifulSoup(page.content, "html5lib")
            fieldset = soup.find("fieldset")
            aTags = fieldset.find_all("a", href=True)
            for a in aTags:
                links.append(a["href"])
        return links

    def getCourseData(link):

        baseURL = "https://m.fiu.edu/catalog/"
        URL = baseURL + link
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html5lib")
        divContent = soup.find("div", attrs={"id": "content"})

        fieldSets = divContent.find_all("fieldset")
        pTagsInFeildSetOne = fieldSets[0].find_all("p", attrs={"class": "data"})

        if "Modesto" in pTagsInFeildSetOne[3].text:
            pTagsInFieldSetTwo = fieldSets[1].find_all("p", attrs={"class": "data"})
            fieldSetThree = fieldSets[2].find_all("li", attrs={"class": "subheading"})
            try:
                dateTime = fieldSetThree[-1].find("p").text
            except IndexError:
                return []

            if len(dateTime) > 1:
                result = []
                timeFields = CourseScraper.parseDayOfTheWeek(dateTime)

                classNbr = pTagsInFeildSetOne[1].text

                if len(pTagsInFieldSetTwo) < 2:
                    capacity = int(pTagsInFieldSetTwo[0].text)
                    enrolled = 0
                else:
                    capacity = int(pTagsInFieldSetTwo[-2].text)
                    enrolled = int(pTagsInFieldSetTwo[-1].text)

                for entry in timeFields:
                    course = {
                        "classNbr": classNbr,
                        "capacity": capacity,
                        "enrolled": enrolled,
                    }

                    result.append(course | entry)
                return result
        return []

    def parseDayOfTheWeek(data):
        dateArr = data.split()
        startTime = CourseScraper.parseTime(dateArr[1])
        endTime = CourseScraper.parseTime(dateArr[3])

        if len(dateArr[0]) > 2:

            days = []
            numOfDays = len(dateArr[0]) // 2
            daysOfWeek = dateArr[0]
            for i in range(numOfDays):
                obj = {"startTime": startTime, "endTime": endTime}
                day = daysOfWeek[:2]
                obj["dow"] = day
                days.append(obj)
                daysOfWeek = daysOfWeek[2:]
            return days

        obj = {"startTime": startTime, "endTime": endTime}
        obj["dow"] = dateArr[0]
        return [obj]

    def parseTime(data):
        n = len(data)
        if n != 6:
            newTime = data[:5] + " " + data[5:]
        else:
            newTime = data[:4] + " " + data[4:]
        in_time = datetime.strptime(newTime, "%I:%M %p")
        out_time = datetime.strftime(in_time, "%H:%M")
        return out_time

    def startScraping(subj):
        data = []
        numbers = CourseScraper.getListOfCourseNumbersFromSubjectList(subj)
        links = CourseScraper.getListOfLinksToCourses(subj, numbers)
        for link in links:
            result = CourseScraper.getCourseData(link)
            for res in result:
                if res:
                    res["subject"] = subj
                    data.append(res)
        return data


if __name__ == "__main__":

    testCourseNumberList = ["2021"]

    # Test getSubjectList()
    # print(CourseScraper.getSubjectList())

    # Test getCourseNumbersFromSubject()
    # testSubject = "ACG"
    # print(CourseScraper.getCourseNumbersFromSubject(testSubject))

    # Test getLinksToCourses()
    # testSubject = "ACG"
    # testArr = ['2021', '3024', '3301', '4101', '4111', '4341', '4401', '4651', '7177', '7436', '7980', '7981']
    # print(CourseScraper.getLinksToCourses(testSubject, testArr))

    # Test getCourseData()
    # testLink = "index.php?action=section&classNbr=84035&strm=1228"
    # testLink2 = "index.php?action=section&classNbr=88848&strm=1228"
    # testLink3 = "index.php?action=section&classNbr=83743&strm=1228"
    # testLink4 = "index.php?action=section&classNbr=90391&strm=1228"
    # testLink5 = "index.php?action=section&classNbr=89226&strm=1228"
    # testLink6 = "index.php?action=section&classNbr=88066&strm=1228"
    # testLink7 = "index.php?action=section&classNbr=88063&strm=1228"
    # print(CourseScraper.getCourseData(testLink))
    # print(CourseScraper.getCourseData(testLink2))
    # print(CourseScraper.getCourseData(testLink3))
    # print(CourseScraper.getCourseData(testLink4))
    # print(CourseScraper.getCourseData(testLink5))
    # print(CourseScraper.getCourseData(testLink6))
    # print(CourseScraper.getCourseData(testLink7))

    # print(
    #     CourseScraper.startScraping("index.php?action=section&classNbr=88848&strm=1228")
    # )

    # data = CourseScraper.run()
    # f = open("demofile.json", "w+")
    # for datapoint in data:
    # f.write(datapoint)
    # f.close()
