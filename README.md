# Euwax-Sentiment
Euwax Sentiment Scaper from Stuttgart Exchange
EUWAX Sentiment Analysis

This Python script performs sentiment analysis on the EUWAX Sentiment Index by retrieving real-time data from the Boerse Stuttgart website and the ONVISTA API. The script utilizes various libraries, including BeautifulSoup for web scraping, pandas for data manipulation, and pykalman for Kalman filtering. The results are then visualized using matplotlib and sent via Telegram for easy monitoring.
Dependencies

Make sure you have the following Python libraries installed:

    requests
    BeautifulSoup
    numpy
    pandas
    matplotlib
    pykalman
    telegram-send

You can install them using:

bash

pip install requests BeautifulSoup4 numpy pandas matplotlib pykalman telegram-send

Usage

    Clone the repository:

bash

git clone https://github.com/yourusername/repo.git
cd repo

    Run the script:

bash

python euwax_sentiment_analysis.py

Configuration

Adjust the following parameters in the script to customize your analysis:

    G_BASEURL: The base URL for the ONVISTA API.
    G_BASEURL2 and G_BASEURL3: Date formatting for API requests.
    G_EUWPeriod: The period for calculating the moving average.
    TelegramFLAG: Set to True if you want to send results via Telegram.

Results

The script generates a plot of EUWAX Sentiment with the daily price, moving average, and Kalman-filtered values. The resulting image is saved as a JPEG file for further analysis.
Disclaimer

This script is for educational and informational purposes only. It is not financial advice, and the developer is not responsible for any trading decisions made based on its results.

Feel free to contribute to and enhance the script. Happy analyzing!
