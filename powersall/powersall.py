"""Advanced Powerball lottery analysis and number generator tool."""
import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
import argparse
from pathlib import Path
import datetime
import json
import numpy as np
from collections import Counter
from .functions import randomeyes, analyze_frequency, get_hot_cold_numbers, detect_patterns

try:
    from importlib.metadata import version
    __version__ = version("powersall")
except ImportError:
    # Fallback for older Python versions or development
    __version__ = "2.0.0"


def prep():
    """Get all the argparse stuff setup."""
    parser = argparse.ArgumentParser(
        description='Advanced Powerball lottery analysis and number generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  powersall --date 2023-12-01     # Show numbers for specific date
  powersall --pick                # Generate random numbers
  powersall --analysis           # Show frequency analysis
  powersall --hot-cold           # Show hot/cold numbers
  powersall --patterns           # Show pattern analysis
  powersall --web                # Launch web interface
        """)
    parser.add_argument('-d', '--date', dest='powerdate',
                        help='yyyy-mm-dd', default='2019-01-19',
                        required=False)
    parser.add_argument('-p', '--pick', dest='pick',
                        help='pick your next powerball card',
                        action="store_true", default=False)
    parser.add_argument('-s', '--save-db', dest='db',
                        action="store_true", default=False)
    parser.add_argument('-a', '--analysis', dest='analysis',
                        help='show frequency analysis',
                        action="store_true", default=False)
    parser.add_argument('-hc', '--hot-cold', dest='hot_cold',
                        help='show hot/cold number analysis',
                        action="store_true", default=False)
    parser.add_argument('-pt', '--patterns', dest='patterns',
                        help='show pattern analysis',
                        action="store_true", default=False)
    parser.add_argument('-w', '--web', dest='web',
                        help='launch web interface',
                        action="store_true", default=False)
    parser.add_argument('-v', '--visualize', dest='visualize',
                        help='create interactive visualizations',
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

    # fixed bin size
    bins = np.arange(-100, 100, 5)  # fixed bin size

    plt.xlim([min(data)-0, max(data)+0])

    plt.hist(data, bins=bins, alpha=0.5)
    plt.title('Distribution of balls selected (non-powerball) and powerballs')
    plt.xlabel('variable X (bin size = 5)')
    plt.ylabel('count')

    plt.savefig(f'{name}.png', bbox_inches='tight')
    plt.close()


def create_visualizations(df):
    """Create interactive visualizations using plotly."""
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        from plotly.subplots import make_subplots

        # Prepare data
        regular_numbers = []
        for col in ['choice 1', 'choice 2', 'choice 3', 'choice 4', 'choice 5']:
            regular_numbers.extend(df[col].tolist())

        # Create frequency analysis
        regular_freq = Counter(regular_numbers)
        powerball_freq = Counter(df['Powerball'].tolist())

        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Regular Numbers Frequency', 'Powerball Frequency',
                          'Regular Numbers Distribution', 'Powerball Distribution'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "histogram"}, {"type": "histogram"}]]
        )

        # Regular numbers frequency
        fig.add_trace(
            go.Bar(x=list(regular_freq.keys()), y=list(regular_freq.values()),
                  name="Regular Numbers"),
            row=1, col=1
        )

        # Powerball frequency
        fig.add_trace(
            go.Bar(x=list(powerball_freq.keys()), y=list(powerball_freq.values()),
                  name="Powerball"),
            row=1, col=2
        )

        # Regular numbers histogram
        fig.add_trace(
            go.Histogram(x=regular_numbers, name="Regular Distribution"),
            row=2, col=1
        )

        # Powerball histogram
        fig.add_trace(
            go.Histogram(x=df['Powerball'].tolist(), name="Powerball Distribution"),
            row=2, col=2
        )

        fig.update_layout(height=800, title_text="Powerball Analysis Dashboard")
        fig.write_html("powerball_analysis.html")
        print("Interactive visualization saved to powerball_analysis.html")

    except ImportError:
        print("Plotly not available. Install with: uv add plotly")


def launch_web_interface(df):
    """Launch a web interface for interactive analysis."""
    try:
        import streamlit as st

        # Create a simple streamlit app
        with open('powerball_app.py', 'w') as f:
            f.write('''
import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

st.title("Powerball Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("~/powerball.csv")

df = load_data()

st.header("Dataset Overview")
st.dataframe(df.head())

# Frequency analysis
st.header("Number Frequency Analysis")
regular_numbers = []
for col in ['choice 1', 'choice 2', 'choice 3', 'choice 4', 'choice 5']:
    regular_numbers.extend(df[col].tolist())

regular_freq = Counter(regular_numbers)
powerball_freq = Counter(df['Powerball'].tolist())

col1, col2 = st.columns(2)
with col1:
    st.subheader("Most Common Regular Numbers")
    for num, freq in regular_freq.most_common(10):
        st.write(f"**{num}**: {freq} times")

with col2:
    st.subheader("Most Common Powerballs")
    for num, freq in powerball_freq.most_common(10):
        st.write(f"**{num}**: {freq} times")

# Visualizations
st.header("Visualizations")
tab1, tab2 = st.tabs(["Frequency Charts", "Distribution"])

with tab1:
    fig1 = px.bar(x=list(regular_freq.keys()), y=list(regular_freq.values()),
                  title="Regular Numbers Frequency")
    st.plotly_chart(fig1)

    fig2 = px.bar(x=list(powerball_freq.keys()), y=list(powerball_freq.values()),
                  title="Powerball Frequency")
    st.plotly_chart(fig2)

with tab2:
    fig3 = px.histogram(regular_numbers, title="Regular Numbers Distribution")
    st.plotly_chart(fig3)

    fig4 = px.histogram(df['Powerball'].tolist(), title="Powerball Distribution")
    st.plotly_chart(fig4)
''')

        print("Streamlit app created: powerball_app.py")
        print("Run with: streamlit run powerball_app.py")

    except ImportError:
        print("Streamlit not available. Install with: uv add streamlit")
        print("Create a simple web interface instead...")

        # Fallback to static HTML
        create_visualizations(df)


def main():
    """Main function for Powerball analysis tool."""
    args = prep()
    my_file = Path(f'{Path.home()}/powerball.csv')

    # Load data if it exists, otherwise fetch it
    if not my_file.is_file():
        print("Downloading Powerball data...")
        getnumbers()

    df = pd.read_csv(f'{Path.home()}/powerball.csv', sep=",")

    # Handle different modes
    if args.pick:
        result = randomeyes(args.db)
        print("Your Powerball numbers:")
        print(f"Regular numbers: {', '.join(map(str, [result[i] for i in range(1, 6)]))}")
        print(f"Powerball: {result['powerball']}")
        return

    if args.analysis:
        analyze_frequency(df)
        return

    if args.hot_cold:
        get_hot_cold_numbers(df)
        return

    if args.patterns:
        detect_patterns(df)
        return

    if args.visualize:
        create_visualizations(df)
        return

    if args.web:
        launch_web_interface(df)
        return

    # Default behavior: show specific date
    try:
        userdate = checkdate(args.powerdate)
        result = df[df['Date'].str.contains(userdate.strftime("%d-%B-%Y"))]
        if result.empty:
            print(f"No data found for date: {args.powerdate}")
            print("Available dates range from the data in powerball.csv")
        else:
            print(f"Powerball numbers for {args.powerdate}:")
            print(result.to_string(index=False))

        # Show some basic analysis
        regular_numbers = []
        for col in ['choice 1', 'choice 2', 'choice 3', 'choice 4', 'choice 5']:
            regular_numbers.extend(df[col].tolist())

        print(f"\nBasic Statistics:")
        print(f"Most common regular number: {Counter(regular_numbers).most_common(1)[0]}")
        print(f"Most common Powerball: {df['Powerball'].mode().iloc[0]}")

    except ValueError as e:
        print(f"Error: {e}")
        print("Please use format YYYY-MM-DD")


if __name__ == "__main__":
    main()
