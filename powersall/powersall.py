"""Gets the powerball numbers."""
import pandas as pd
from bs4 import BeautifulSoup
import requests
from statistics import mean
import csv
import argparse
from pathlib import Path


__version__ = "1.0.1"


def prep():
    """Get all the argparse stuff setup."""
    parser = argparse.ArgumentParser(description='simple get powerball info\
                                     for specific date, example: powersall -d\
                                     "05-12-2019"')
    parser.add_argument('-d', '--date', dest='powerdate',
                        help='yyyy-mm-dd', default='2019-07-06',
                        required=False)
    args = parser.parse_args()
    return args


def checkdate(powerdate):
    """Date parsing."""
    datedata = pd.read_csv('~/powerball.csv', sep=",")['Date']


def getnumbers():
    soup = BeautifulSoup(requests.get(
        "https://www.lottonumbers.com/past-powerball-results").text, "lxml")
    powerballs = []
    regballs = []
    totals = []
    dates = []
    with open(f'{Path.home()}/powerball.csv', 'w+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Date", "choice 1", "choice 2",
                             "choice 3", "choice 4", "choice 5", "Powerball"])
        for item in soup.findAll("tr"):
            try:
                alinkdate = item.find("a").contents
                datefixer = "-".join([alinkdate[0].split()[1], alinkdate[2].split()[0],alinkdate[2].split()[1]])
                # print(datefixer)
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
                [datefixer] + list(map(int, justcontents)))
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
    args = prep()
    from pathlib import Path

    my_file = Path("~/powerball.csv")
    if my_file.is_file():
        checkdate(args.powerdate)
    powerballdata, regularballdata = getnumbers()
    getplot(regularballdata, "regular")
    getplot(powerballdata, "powerball")


if __name__ == "__main__":
    main()
