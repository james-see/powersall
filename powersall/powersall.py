"""Gets the powerball numbers."""
import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
import argparse
from pathlib import Path
import datetime
from .functions import randomeyes

__version__ = "1.0.8"


def prep():
    """Get all the argparse stuff setup."""
    parser = argparse.ArgumentParser(description='simple get powerball info\
                                     for specific date, example: powersall -d\
                                     "05-12-2019"')
    parser.add_argument('-d', '--date', dest='powerdate',
                        help='yyyy-mm-dd', default='2019-01-19',
                        required=False)
    parser.add_argument('-p', '--pick', dest='pick',
                        help='pick your next powerball card',
                        action="store_true", default=False)
    parser.add_argument('-s', '--save-db', dest='db',
                        action="store_true", default=False)
    args = parser.parse_args()
    return args


def checkdate(powerdate):
    """Date parsing."""
    userinput = datetime.datetime.strptime(powerdate, '%Y-%m-%d')
    datedata = pd.read_csv(
        f'{Path.home()}/powerball.csv', sep=",")['Date'].tolist()
    realdatelist = []
    for item in datedata:
        realdatelist.append(datetime.datetime.strptime(item, '%d-%B-%Y'))
    # for item in realdatelist:
    #     print(item.strftime("%Y-%m-%d"))
    # if userinput in realdatelist:
    #     print("FOUND")
    return userinput

    # print(datedata.tolist())


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
                if len(alinkdate[0].split()[1]) == 1:
                    fixednum = f"{str(0)}{alinkdate[0].split()[1]}"
                else:
                    fixednum = alinkdate[0].split()[1]
                datefixer = "-".join([fixednum,
                                      alinkdate[2].split()[0], alinkdate[2].split()[1]])
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
            # print(justcontents)
            powerballs.append(int(justcontents[-1]))
            dates.append([alinkdate[0], alinkdate[2],
                          ','.join(map(str, justcontents))])
            spamwriter.writerow(
                [datefixer] + list(map(int, justcontents)))

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

    plt.savefig(f'{name}.png', bbox_inches='tight')
    plt.close()


def main():
    """Gets the powerball numbers."""
    args = prep()
    my_file = Path(f'{Path.home()}/powerball.csv')
    if my_file.is_file() and args.pick:
        with open(f'{Path.home()}/powerball.csv') as f:
            powerballdata = list(csv.reader(f))[1:]
            print(randomeyes(args.db))
            exit()
    if my_file.is_file():
        userdate = checkdate(args.powerdate)
        powerballdata = pd.read_csv(
            f'{Path.home()}/powerball.csv', sep=",")['Powerball']
        df = pd.read_csv(f'{Path.home()}/powerball.csv', sep=",")
        print(df[df['Date'].str.contains(userdate.strftime("%d-%B-%Y"))])
        regularballdata = df['choice 1'].values.tolist() + df['choice 2'].values.tolist() + \
            df['choice 3'].values.tolist() + df['choice 4'].values.tolist() + \
            df['choice 5'].values.tolist()
    else:
        powerballdata, regularballdata = getnumbers()
        userdate = checkdate(args.powerdate)
        df = pd.read_csv(f'{Path.home()}/powerball.csv', sep=",")
        print(df[df['Date'].str.contains(userdate.strftime("%d-%B-%Y"))])
    getplot(regularballdata, "regular")
    getplot(powerballdata, "powerball")


if __name__ == "__main__":
    main()
