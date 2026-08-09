import os
import re

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# The dataset does not include column names, so they are added while reading it.
columns = ["tweet_id", "brand", "sentiment", "tweet"]

train_data = pd.read_csv("twitter_training.csv", names=columns)
validation_data = pd.read_csv("twitter_validation.csv", names=columns)

# Using both files gives a larger picture of the sentiment in the dataset.
data = pd.concat([train_data, validation_data], ignore_index=True)

# Remove rows with no tweet and repeated rows before doing the analysis.
data = data.dropna(subset=["tweet"])
data = data.drop_duplicates()


def clean_tweet(tweet):
    """Make tweets easier to read by removing links and extra spaces."""
    tweet = str(tweet)
    tweet = re.sub(r"http\S+|www\.\S+", "", tweet)
    tweet = re.sub(r"@\w+", "", tweet)
    tweet = re.sub(r"\s+", " ", tweet)
    return tweet.strip()


data["clean_tweet"] = data["tweet"].apply(clean_tweet)

print("Number of tweets after cleaning:", len(data))
print("\nSentiment count:")
print(data["sentiment"].value_counts())

# Folder for the graphs made by this program.
os.makedirs("output", exist_ok=True)

sns.set_theme(style="whitegrid")
order = ["Positive", "Neutral", "Negative", "Irrelevant"]

# Chart 1: total tweets in each sentiment class.
plt.figure(figsize=(8, 5))
sns.countplot(
    data=data,
    x="sentiment",
    hue="sentiment",
    order=order,
    palette="Set2",
    legend=False,
)
plt.title("Overall Sentiment in Twitter Data")
plt.xlabel("Sentiment")
plt.ylabel("Number of Tweets")
plt.tight_layout()
plt.savefig("output/sentiment_count.png")
plt.close()

# Chart 2: the ten brands with the most tweets.
top_brands = data["brand"].value_counts().head(10).index
brand_data = data[data["brand"].isin(top_brands)]

plt.figure(figsize=(12, 6))
sns.countplot(
    data=brand_data,
    y="brand",
    hue="sentiment",
    hue_order=order,
    order=top_brands,
    palette="Set2",
)
plt.title("Sentiment for the 10 Most Discussed Brands")
plt.xlabel("Number of Tweets")
plt.ylabel("Brand")
plt.legend(title="Sentiment")
plt.tight_layout()
plt.savefig("output/brand_sentiment.png")
plt.close()

# Chart 3: percentage distribution of sentiment.
sentiment_percent = data["sentiment"].value_counts(normalize=True).reindex(order) * 100

plt.figure(figsize=(7, 7))
plt.pie(
    sentiment_percent,
    labels=sentiment_percent.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=sns.color_palette("Set2", 4),
)
plt.title("Sentiment Distribution")
plt.tight_layout()
plt.savefig("output/sentiment_pie_chart.png")
plt.close()

print("\nGraphs saved in the output folder.")
