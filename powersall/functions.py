import markovify
import random
import json
import datetime
import pandas as pd
from collections import Counter
import numpy as np


def markover(data):
    """Takes in data list of strings."""
    fixeddata = '\n'.join(map(str, data))
    text_model = markovify.NewlineText(fixeddata)
    return text_model.make_sentence()


def randomeyes(db=False):
    """Gets random numbers for powerball and return as list."""
    selection = dict()
    for counter in range(1, 6):
        selected = random.randint(1, 69)
        if selected not in selection.values():
            selection[counter] = selected
        else:
            return randomeyes()
    selection['powerball'] = random.randint(1, 26)
    if db:
        outjson = {}
        outjson['results'] = selection
        with open(f'selection_{datetime.datetime.now().strftime("%m-%d-%y-%h-%m-%s")}.json', 'w+') as f:
            f.write(json.dumps(outjson))
    return selection


def analyze_frequency(df):
    """Analyze number frequency in the Powerball dataset."""
    print("Powerball Frequency Analysis")
    print("=" * 40)

    # Regular numbers (1-69)
    regular_numbers = []
    for col in ['choice 1', 'choice 2', 'choice 3', 'choice 4', 'choice 5']:
        regular_numbers.extend(df[col].tolist())

    regular_freq = Counter(regular_numbers)
    powerball_freq = Counter(df['Powerball'].tolist())

    print("\nMost Common Regular Numbers (1-69):")
    for num, freq in regular_freq.most_common(10):
        percentage = (freq / len(df)) * 100
        print(f"  {num:2d}: {freq:3d} times ({percentage:5.1f}%)")

    print("\nMost Common Powerballs (1-26):")
    for num, freq in powerball_freq.most_common(10):
        percentage = (freq / len(df)) * 100
        print(f"  {num:2d}: {freq:3d} times ({percentage:5.1f}%)")

    print(f"\nLeast Common Regular Numbers (1-69):")
    for num, freq in regular_freq.most_common()[-10:]:
        percentage = (freq / len(df)) * 100
        print(f"  {num:2d}: {freq:3d} times ({percentage:5.1f}%)")

    print(f"\nLeast Common Powerballs (1-26):")
    for num, freq in powerball_freq.most_common()[-10:]:
        percentage = (freq / len(df)) * 100
        print(f"  {num:2d}: {freq:3d} times ({percentage:5.1f}%)")


def get_hot_cold_numbers(df, recent_games=50):
    """Identify hot and cold numbers based on recent draws."""
    print("Hot/Cold Numbers Analysis")
    print("=" * 40)

    # Get recent games
    recent_df = df.head(recent_games)

    # Regular numbers
    recent_regular = []
    for col in ['choice 1', 'choice 2', 'choice 3', 'choice 4', 'choice 5']:
        recent_regular.extend(recent_df[col].tolist())

    recent_regular_freq = Counter(recent_regular)
    recent_powerball_freq = Counter(recent_df['Powerball'].tolist())

    # All-time frequencies for comparison
    all_regular = []
    for col in ['choice 1', 'choice 2', 'choice 3', 'choice 4', 'choice 5']:
        all_regular.extend(df[col].tolist())

    all_regular_freq = Counter(all_regular)
    all_powerball_freq = Counter(df['Powerball'].tolist())

    print(f"\nHot Regular Numbers (last {recent_games} games):")
    hot_regular = [num for num, _ in recent_regular_freq.most_common(10)]
    for num in hot_regular:
        recent_count = recent_regular_freq[num]
        all_count = all_regular_freq[num]
        print(f"  {num:2d}: {recent_count} times recently, {all_count} times total")

    print(f"\nCold Regular Numbers (missing from last {recent_games} games):")
    all_numbers = set(range(1, 70))
    recent_numbers = set(recent_regular_freq.keys())
    cold_regular = list(all_numbers - recent_numbers)
    cold_regular.sort()
    for num in cold_regular[:10]:
        all_count = all_regular_freq[num]
        print(f"  {num:2d}: {all_count} times total")

    print(f"\nHot Powerballs (last {recent_games} games):")
    hot_powerballs = [num for num, _ in recent_powerball_freq.most_common(5)]
    for num in hot_powerballs:
        recent_count = recent_powerball_freq[num]
        all_count = all_powerball_freq[num]
        print(f"  {num:2d}: {recent_count} times recently, {all_count} times total")

    print(f"\nCold Powerballs (missing from last {recent_games} games):")
    all_powerballs = set(range(1, 27))
    recent_powerballs = set(recent_powerball_freq.keys())
    cold_powerballs = list(all_powerballs - recent_powerballs)
    cold_powerballs.sort()
    for num in cold_powerballs[:5]:
        all_count = all_powerball_freq[num]
        print(f"  {num:2d}: {all_count} times total")


def detect_patterns(df):
    """Detect patterns in Powerball numbers."""
    print("Pattern Analysis")
    print("=" * 40)

    # Analyze odd/even patterns
    print("\nOdd/Even Pattern Analysis:")

    total_draws = len(df)
    odd_even_patterns = []

    for _, row in df.iterrows():
        numbers = [row['choice 1'], row['choice 2'], row['choice 3'],
                  row['choice 4'], row['choice 5'], row['Powerball']]
        odd_count = sum(1 for num in numbers[:-1] if num % 2 == 1)
        even_count = 5 - odd_count
        powerball_odd = numbers[-1] % 2 == 1

        pattern = f"{odd_count}O-{even_count}E"
        if powerball_odd:
            pattern += "-PB-Odd"
        else:
            pattern += "-PB-Even"
        odd_even_patterns.append(pattern)

    pattern_freq = Counter(odd_even_patterns)
    for pattern, freq in pattern_freq.most_common(10):
        percentage = (freq / total_draws) * 100
        print(f"  {pattern}: {freq:3d} times ({percentage:5.1f}%)")

    # Analyze sum patterns
    print("\nSum Pattern Analysis (regular numbers):")
    sums = []
    for _, row in df.iterrows():
        numbers = [row['choice 1'], row['choice 2'], row['choice 3'],
                  row['choice 4'], row['choice 5']]
        sums.append(sum(numbers))

    sum_ranges = [(0, 100), (101, 150), (151, 200), (201, 250), (251, 350)]
    for range_min, range_max in sum_ranges:
        count = sum(1 for s in sums if range_min <= s <= range_max)
        percentage = (count / total_draws) * 100
        print(f"  Sum {range_min:3d}-{range_max:3d}: {count:3d} times ({percentage:5.1f}%)")

    # Analyze consecutive numbers
    print("\nConsecutive Numbers Analysis:")
    consecutive_counts = []
    for _, row in df.iterrows():
        numbers = sorted([row['choice 1'], row['choice 2'], row['choice 3'],
                         row['choice 4'], row['choice 5']])
        consecutive = 0
        for i in range(len(numbers) - 1):
            if numbers[i + 1] - numbers[i] == 1:
                consecutive += 1
        consecutive_counts.append(consecutive)

    for cons in range(5):  # Max possible consecutive is 4 pairs
        count = consecutive_counts.count(cons)
        percentage = (count / total_draws) * 100
        print(f"  {cons} consecutive pairs: {count:3d} times ({percentage:5.1f}%)")


def generate_weighted_random(df, use_hot_cold=False, recent_games=100):
    """Generate numbers using weighted randomness based on frequency."""
    if use_hot_cold:
        # Use recent games for hot/cold analysis
        recent_df = df.head(recent_games)

        # Get recent frequencies
        recent_regular = []
        for col in ['choice 1', 'choice 2', 'choice 3', 'choice 4', 'choice 5']:
            recent_regular.extend(recent_df[col].tolist())

        recent_freq = Counter(recent_regular)

        # Weight numbers by their recent frequency
        numbers = list(range(1, 70))
        weights = [recent_freq.get(num, 1) for num in numbers]  # Minimum weight of 1

        selection = set()
        while len(selection) < 5:
            selected = random.choices(numbers, weights=weights)[0]
            selection.add(selected)

        # Powerball (less weighting for recency)
        powerball = random.randint(1, 26)
    else:
        # Simple random
        selection = set()
        while len(selection) < 5:
            selection.add(random.randint(1, 69))

        powerball = random.randint(1, 26)

    return sorted(list(selection)), powerball
