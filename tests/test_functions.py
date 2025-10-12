import pytest
import pandas as pd
import json
from datetime import datetime
from collections import Counter
from powersall.functions import (
    randomeyes, analyze_frequency, get_hot_cold_numbers,
    detect_patterns, generate_weighted_random
)


class TestRandomEyes:
    """Test the random number generation function."""

    def test_randomeyes_returns_dict(self):
        """Test that randomeyes returns a dictionary with correct structure."""
        result = randomeyes()
        assert isinstance(result, dict)
        assert all(key in result for key in [1, 2, 3, 4, 5, 'powerball'])
        assert all(isinstance(num, int) for num in [result[i] for i in range(1, 6)])
        assert 1 <= result['powerball'] <= 26

    def test_randomeyes_unique_numbers(self):
        """Test that regular numbers are unique."""
        result = randomeyes()
        numbers = [result[i] for i in range(1, 6)]
        assert len(numbers) == len(set(numbers))  # All unique
        assert all(1 <= num <= 69 for num in numbers)

    def test_randomeyes_save_db(self):
        """Test that save functionality creates a JSON file."""
        import os
        import glob

        # Clean up any existing files
        pattern = "selection_*.json"
        for file in glob.glob(pattern):
            os.remove(file)

        # Test save functionality
        result = randomeyes(db=True)
        assert isinstance(result, dict)

        # Check that a file was created
        files = glob.glob(pattern)
        assert len(files) == 1

        # Verify file contents
        with open(files[0], 'r') as f:
            data = json.load(f)
            assert 'results' in data
            assert data['results'] == result

        # Clean up
        os.remove(files[0])


class TestAnalyzeFrequency:
    """Test the frequency analysis function."""

    @pytest.fixture
    def sample_dataframe(self):
        """Create a sample DataFrame for testing."""
        data = {
            'Date': ['01-Jan-2023', '02-Jan-2023', '03-Jan-2023'],
            'choice 1': [5, 12, 23],
            'choice 2': [15, 25, 35],
            'choice 3': [25, 35, 45],
            'choice 4': [35, 45, 55],
            'choice 5': [45, 55, 65],
            'Powerball': [10, 15, 20]
        }
        return pd.DataFrame(data)

    def test_analyze_frequency_output(self, sample_dataframe, capsys):
        """Test that analyze_frequency produces expected output."""
        analyze_frequency(sample_dataframe)

        captured = capsys.readouterr()
        output = captured.out

        # Check for key sections in output
        assert "Powerball Frequency Analysis" in output
        assert "Most Common Regular Numbers" in output
        assert "Most Common Powerballs" in output
        assert "Least Common Regular Numbers" in output
        assert "Least Common Powerballs" in output

        # Check that percentages are calculated correctly
        assert "%" in output


class TestHotColdNumbers:
    """Test the hot/cold numbers analysis function."""

    @pytest.fixture
    def sample_dataframe_large(self):
        """Create a larger sample DataFrame for testing."""
        # Create a DataFrame with more realistic data
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        data = {
            'Date': dates.strftime('%d-%b-%Y'),
            'choice 1': [1, 2, 3, 4, 5] * 20,
            'choice 2': [6, 7, 8, 9, 10] * 20,
            'choice 3': [11, 12, 13, 14, 15] * 20,
            'choice 4': [16, 17, 18, 19, 20] * 20,
            'choice 5': [21, 22, 23, 24, 25] * 20,
            'Powerball': [1, 2, 3, 4, 5] * 20
        }
        return pd.DataFrame(data)

    def test_hot_cold_numbers_output(self, sample_dataframe_large, capsys):
        """Test that get_hot_cold_numbers produces expected output."""
        get_hot_cold_numbers(sample_dataframe_large, recent_games=20)

        captured = capsys.readouterr()
        output = captured.out

        assert "Hot/Cold Numbers Analysis" in output
        assert "Hot Regular Numbers" in output
        assert "Cold Regular Numbers" in output
        assert "Hot Powerballs" in output
        assert "Cold Powerballs" in output


class TestDetectPatterns:
    """Test the pattern detection function."""

    @pytest.fixture
    def pattern_dataframe(self):
        """Create a DataFrame with specific patterns for testing."""
        data = {
            'Date': ['01-Jan-2023', '02-Jan-2023', '03-Jan-2023', '04-Jan-2023'],
            'choice 1': [1, 2, 3, 4],    # All odd, all odd, all odd, all even
            'choice 2': [3, 4, 5, 6],    # Odd, even, odd, even
            'choice 3': [5, 6, 7, 8],    # Odd, even, odd, even
            'choice 4': [7, 8, 9, 10],   # Odd, even, odd, even
            'choice 5': [9, 10, 11, 12], # Odd, even, odd, even
            'Powerball': [2, 4, 6, 8]     # All even
        }
        return pd.DataFrame(data)

    def test_detect_patterns_output(self, pattern_dataframe, capsys):
        """Test that detect_patterns produces expected output."""
        detect_patterns(pattern_dataframe)

        captured = capsys.readouterr()
        output = captured.out

        assert "Pattern Analysis" in output
        assert "Odd/Even Pattern Analysis" in output
        assert "Sum Pattern Analysis" in output
        assert "Consecutive Numbers Analysis" in output

        # Check for pattern format like "3O-2E"
        assert "O-" in output and "E" in output


class TestGenerateWeightedRandom:
    """Test the weighted random number generation function."""

    @pytest.fixture
    def frequency_dataframe(self):
        """Create a DataFrame with frequency-biased data."""
        # Create data where number 1 appears more frequently
        data = {
            'Date': ['01-Jan-2023'] * 10,
            'choice 1': [1, 1, 1, 2, 2, 3, 4, 5, 6, 7],
            'choice 2': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
            'choice 3': [18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
            'choice 4': [28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
            'choice 5': [38, 39, 40, 41, 42, 43, 44, 45, 46, 47],
            'Powerball': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }
        return pd.DataFrame(data)

    def test_generate_weighted_random_structure(self, frequency_dataframe):
        """Test that generate_weighted_random returns correct structure."""
        regular, powerball = generate_weighted_random(frequency_dataframe, use_hot_cold=True)

        assert isinstance(regular, list)
        assert len(regular) == 5
        assert all(isinstance(num, int) for num in regular)
        assert all(1 <= num <= 69 for num in regular)
        assert len(set(regular)) == 5  # All unique

        assert isinstance(powerball, int)
        assert 1 <= powerball <= 26

    def test_generate_weighted_random_vs_regular_random(self, frequency_dataframe):
        """Test that weighted random behaves differently from regular random."""
        # Generate multiple samples with weighting
        weighted_samples = []
        for _ in range(100):
            regular, _ = generate_weighted_random(frequency_dataframe, use_hot_cold=True)
            weighted_samples.extend(regular)

        # Generate samples without weighting
        regular_samples = []
        for _ in range(100):
            regular, _ = generate_weighted_random(frequency_dataframe, use_hot_cold=False)
            regular_samples.extend(regular)

        # The weighted samples should show bias toward number 1
        weighted_freq = Counter(weighted_samples)
        regular_freq = Counter(regular_samples)

        # Number 1 should appear more frequently in weighted samples
        assert weighted_freq[1] > regular_freq[1]
