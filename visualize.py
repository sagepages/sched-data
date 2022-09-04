import seaborn as sns
import matplotlib.pylab as plt
from Pipeline import Pipeline


def getData(dow, timeRoll):

    pipeline = Pipeline()
    data = {"Mo": [], "Tu": [], "We": [], "Th": [], "Fr": [], "Sa": [], "Su": []}
    for day in dow:
        for st in range(len(timeRoll) - 1):
            et = st + 1
            result = pipeline.query_data(day, timeRoll[st], timeRoll[et])
            data[day].append(result)
    return data


def getCSData(dow, timeRoll):
    pipeline = Pipeline()
    data = {"Mo": [], "Tu": [], "We": [], "Th": [], "Fr": [], "Sa": [], "Su": []}
    for day in dow:
        for st in range(len(timeRoll) - 1):
            et = st + 1
            result = pipeline.queryCSCE(day, timeRoll[st], timeRoll[et])
            if result is None:
                data[day].append(0)
            else:
                data[day].append(result)
    return data


if __name__ == "__main__":
    dow = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    timeRoll = [
        "7:00",
        "7:30",
        "8:00",
        "8:30",
        "9:00",
        "9:30",
        "10:00",
        "10:30",
        "11:00",
        "11:30",
        "12:00",
        "12:30",
        "13:00",
        "13:30",
        "14:00",
        "14:30",
        "15:00",
        "15:30",
        "16:00",
        "16:30",
        "17:00",
        "17:30",
        "18:00",
        "18:30",
        "19:00",
        "19:30",
        "20:00",
        "20:30",
        "21:00",
    ]

    xAxisLabels = [
        "7",
        "7:30",
        "8",
        "8:30",
        "9",
        "9:30",
        "10",
        "10:30",
        "11",
        "11:30",
        "12",
        "12:30",
        "1",
        "13:30",
        "2",
        "14:30",
        "3",
        "15:30",
        "4",
        "16:30",
        "5",
        "17:30",
        "6",
        "18:30",
        "7",
        "19:30",
        "8",
        "20:30",
    ]
    # data = getData(dow, timeRoll)
    data = getCSData(dow, timeRoll)
    uniform_data = [
        data["Mo"],
        data["Tu"],
        data["We"],
        data["Th"],
        data["Fr"],
    ]

    yAxisLabels = ["Mo", "Tu", "We", "Th", "Fr"]

    ax = sns.heatmap(
        uniform_data, linewidth=1.5, xticklabels=xAxisLabels, yticklabels=yAxisLabels
    )

    for i, t in enumerate(ax.get_xticklabels()):
        if (i % 2) != 0:
            t.set_visible(False)

    for item in ax.get_xticklabels():
        item.set_rotation(45)
    for item in ax.get_yticklabels():
        item.set_rotation(45)

    # ax.set(title="Number of students on MMC by half hour")
    ax.set(title="Number of students on MMC by half hour - (CS/CE Only)")

    plt.show()
