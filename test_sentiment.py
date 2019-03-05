from sentimentAnalysis import SentimentAnalysis

def test():
    print('entered')
    sentiment = SentimentAnalysis()
    #print(sentiment.vaderAnalysis("The phone is super cool."))
    #print(sentiment.vaderAnalysis("The food here is good!"))

    posts = ["The phone is super cool.", "The food here is good!"]

    #sentiment.textBlobAnalysesmulti(posts)
    post = "I'm having a great day!"
    print("this is textblob")
    sentiment.textBlobAnalyses(post)

    print("this is vader")
    vader = sentiment.vaderAnalysis(post)
    print(sentiment.get_compound(vader))
    difference = sentiment.comparisonAnalyses(post)
    #print("the difference for '{}' comparing textBlob to vader is {}".format(post, difference))

test()
