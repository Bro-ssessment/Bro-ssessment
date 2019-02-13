from sentimentAnalysis import SentimentAnalysis

def main():
    print('entered')
    sentiment = SentimentAnalysis()
    print(sentiment.vaderAnalysis("The phone is super cool."))
    print(sentiment.vaderAnalysis("The food here is good!"))

    posts = ["The phone is super cool.", "The food here is good!"]

    sentiment.textBlobAnalysesmulti(posts)
    post = "The phone is super cool."
    sentiment.textBlobAnalyses(post)
    difference = sentiment.comparisonAnalyses(post)
    print("the difference for '{}' comparing textBlob to vader is {}".format(post, difference))
main()
