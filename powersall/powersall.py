"""Gets the powerball numbers."""
from bs4 import BeautifulSoup
import requests
from statistics import mean
import csv


__version__ = "1.0.0"


def getnumbers():
    soup = BeautifulSoup(requests.get(
        "https://www.lottonumbers.com/past-powerball-results").text, "lxml")
    powerballs = []
    regballs = []
    totals = []
    dates = []
    with open('powerball.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Day", "Month", "Year", "choice 1", "choice 2",
                             "choice 3", "choice 4", "choice 5", "Powerball"])
        for item in soup.findAll("tr"):
            try:
                alinkdate = item.find("a").contents
                print(alinkdate[0], alinkdate[2])
            except AttributeError:
                continue
            # print(item.find("a"))
            try:
                numbers = item.find("ul").find_all("li")
                del numbers[-1]
                justcontents = []
                for val in numbers:
                    justcontents.append(int(val.contents[0]))
                    regballs.append(int(val.contents[0]))
                del regballs[-1]
                # print(sum(justcontents))
                totals.append(sum(justcontents))
            except AttributeError:
                continue
            print(justcontents)
            powerballs.append(int(justcontents[-1]))
            dates.append([alinkdate[0], alinkdate[2],
                          ','.join(map(str, justcontents))])
            spamwriter.writerow(
                [alinkdate[0]] + alinkdate[2].split() + list(map(int, justcontents)))
    print(mean(totals))
    print(dates[0])

    return powerballs, regballs


def getplot(data, name):
    """Plot data."""
    import numpy as np
    from matplotlib import pyplot as plt
    data = np.array(data)
    # data = np.random.normal(0, 20, 1000)

    # fixed bin size
    bins = np.arange(-100, 100, 5)  # fixed bin size

    plt.xlim([min(data)-0, max(data)+0])

    plt.hist(data, bins=bins, alpha=0.5)
    plt.title('Distribution of balls selected (non-powerball) and powerballs')
    plt.xlabel('variable X (bin size = 5)')
    plt.ylabel('count')

    # plt.show()
    # num = uuid4()
    plt.savefig(f'{name}.png', bbox_inches='tight')
    plt.close()


def main():
    """Gets the powerball numbers."""
    powerballdata, regularballdata = getnumbers()
    getplot(regularballdata, "regular")
    getplot(powerballdata, "powerball")


if __name__ == "__main__":
    main()
