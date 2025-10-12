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
        # Handle both old format (%d-%B-%Y) and new format (%Y-%m-%d)
        try:
            # Try new format first (YYYY-MM-DD)
            realdatelist.append(datetime.datetime.strptime(str(item), '%Y-%m-%d'))
        except ValueError:
            try:
                # Fall back to old format (DD-MMM-YYYY)
                realdatelist.append(datetime.datetime.strptime(str(item), '%d-%B-%Y'))
            except ValueError:
                # Skip invalid dates
                continue
    return userinput

    # print(datedata.tolist())


def getnumbers():
    """Fetch Powerball numbers from website with robust error handling."""
    try:
        # Add headers to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(
            "https://www.lottonumbers.com/powerball/past-numbers",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.text, "lxml")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Powerball data: {e}")
        print("Please check your internet connection or try again later.")
        return [], []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return [], []

    powerballs = []
    regballs = []
    totals = []
    dates = []

    with open(f'{Path.home()}/powerball.csv', 'w+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Date", "choice 1", "choice 2",
                             "choice 3", "choice 4", "choice 5", "Powerball", "PowerPlay"])

        # Find the results table
        results_table = soup.find("table", class_="past-results")
        if not results_table:
            print("Could not find results table on the webpage")
            return [], []

        # Process each row in the table
        for row in results_table.find_all("tr"):
            # Skip header row
            if row.find("th"):
                continue

            try:
                # Get date from the date cell
                date_cell = row.find("td", class_="date-row")
                if not date_cell:
                    continue

                date_text = date_cell.get_text().strip()
                if not date_text:
                    continue

                # Parse date (format: "Sat, Oct 11 2025")
                date_parts = date_text.replace(",", "").split()
                if len(date_parts) < 4:
                    continue

                day_name = date_parts[0]
                month_name = date_parts[1]
                day_num = date_parts[2]
                year = date_parts[3]

                # Convert month name to number
                month_map = {
                    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                }

                month_num = month_map.get(month_name, '01')

                # Handle single digit days
                if len(day_num) == 1:
                    day_num = f"0{day_num}"

                datefixer = f"{year}-{month_num}-{day_num}"

            except (AttributeError, IndexError, KeyError, ValueError) as e:
                # Skip malformed date rows
                continue

            try:
                # Get numbers from the balls cell
                balls_cell = row.find("td", class_="balls-row")
                if not balls_cell:
                    continue

                balls_ul = balls_cell.find("ul", class_="balls")
                if not balls_ul:
                    continue

                # Get all ball elements
                ball_elements = balls_ul.find_all("li", class_="ball")

                # Separate regular balls from special balls (powerball, power-play)
                regular_balls = []
                powerball = None
                powerplay = None

                for ball in ball_elements:
                    ball_class = ball.get("class", [])
                    ball_text = ball.get_text().strip()

                    if "powerball" in ball_class:
                        if ball_text.isdigit():
                            powerball = int(ball_text)
                    elif "power-play" in ball_class:
                        if ball_text.isdigit():
                            powerplay = int(ball_text)
                    else:
                        # Regular ball
                        if ball_text.isdigit():
                            regular_balls.append(int(ball_text))

                if len(regular_balls) != 5 or powerball is None:
                    continue

                # Sort regular balls for consistency
                regular_balls.sort()

                # Add to our collections
                regballs.extend(regular_balls)
                powerballs.append(powerball)

                # Write to CSV (always include PowerPlay column)
                powerplay_value = powerplay if powerplay is not None else ""
                csv_row = [datefixer] + regular_balls + [powerball, powerplay_value]
                spamwriter.writerow(csv_row)

                # For compatibility with old format
                totals.append(sum(regular_balls))

            except (AttributeError, IndexError, ValueError) as e:
                # Skip malformed number rows
                continue

    print(f"Successfully downloaded {len(powerballs)} Powerball records")
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

    df = pd.read_csv(f'{Path.home()}/powerball.csv', sep=",", dtype=str)

    # Convert numeric columns to integers for analysis
    numeric_columns = ['choice 1', 'choice 2', 'choice 3', 'choice 4', 'choice 5', 'Powerball', 'PowerPlay']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

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
        # Search for the date in YYYY-MM-DD format (new format)
        target_date = userdate.strftime("%Y-%m-%d")
        # Ensure Date column is treated as string for pattern matching
        result = df[df['Date'].astype(str).str.contains(target_date)]
        if result.empty:
            print(f"No data found for date: {args.powerdate}")
            print("Available dates range from the data in powerball.csv")
            # Show available dates for debugging
            available_dates = df['Date'].astype(str).unique()[:10]  # Show first 10 dates
            print(f"Available date formats: {available_dates}")
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
