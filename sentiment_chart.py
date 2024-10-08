import matplotlib.pyplot as plt
import io
import base64


def create_sentiment_plot(positive, negative, neutral):
    # Data for the pie chart
    sentiments = [positive, negative, neutral]
    labels = ["Positive", "Negative", "Neutral"]
    colors = ["#007bff", "#ff7f0e", "#2ca02c"]  # Adjust the colors to match your theme

    # Plot
    fig, ax = plt.subplots()
    ax.pie(sentiments, labels=labels, autopct="%1.1f%%", colors=colors)
    ax.set_title("Sentiment Analysis")

    # Save the plot to a file
    plt.savefig(
        "static/sentiment_plot.png"
    )  # Save it in the static directory for serving via HTML
    plt.close()
