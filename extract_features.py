import csv
import numpy as np
from scipy import stats

from brossessment.models import *

course_id_maper = {
    "1": "568",
    "2": "833",
    "3": "841",
    "4": "820",
    "5": "830",
    "6": "826",
    "7": "586",
}


def parse_ccs_outcome():
    ccs = {}
    with open("data/ccs/ccs.csv") as f:
        reader = csv.reader(f)
        next(reader, None)
        lines = list(reader)

        for class_id, score in lines:
            if ccs.get(class_id, None):
                ccs[class_id] += [int(score)]
            else:
                ccs[class_id] = [int(score)]

    for class_id, responses in ccs.items():
        ccs[class_id] = np.mean(responses, dtype=np.float32)

    return ccs

def get_ccs_std():
    ccs = {}
    with open("data/ccs/ccs.csv") as f:
        reader = csv.reader(f)
        next(reader, None)
        lines = list(reader)

        for class_id, score in lines:
            if ccs.get(class_id, None):
                ccs[class_id] += [int(score)]
            else:
                ccs[class_id] = [int(score)]

    for class_id, responses in ccs.items():
        ccs[class_id] = np.std(responses, dtype=np.float32)

    return ccs


def main():
    ccs = parse_ccs_outcome()
    std = get_ccs_std()
    class_stat = Post.select(
        Post.class_id,
        Post.post_id,
        Post.user_id,
        # Post.google_sentiment_score,
        # Post.google_sentiment_magnitude,
        # Post.textblob_sentiment_score,
        # Post.vader_sentiment_score,
        Post.bro_sentiment,
        Post.lsi_similarity_score,
        Post.private,
        Post.shared,
        Post.wordcount,
        Post.verbs,
        Post.nouns,
        Post.adjectives,
    ).where(Post.content != "").dicts()

    row = class_stat[0]
    header = [k for k, v in row.items()]
    header.append("avg_ccs")
    header.append("std_ccs")
    header.append("word_zscore")

    data = []
    for c in class_stat:
        real_class_id = course_id_maper[str(c["class_id"])]
        for k, v in c.items():
            if isinstance(v, bool):
                c[k] = 1 if v is True else 0
        metrics = list(c.values())[1:]
        metrics.insert(0, real_class_id)
        metrics.append(ccs[real_class_id])
        metrics.append(std[real_class_id])
        data.append(metrics)

    data.sort(key=lambda x: x[0])  # sort by ID desc order

    # calculate wordcount zscore
    wordcount_arr = np.array([c[7] for c in data])
    wordcount_zscore = stats.zscore(wordcount_arr)
    sorted_wordcount_zscore = [[c] for c in wordcount_zscore]
    data = list(np.append(data, sorted_wordcount_zscore, axis=1))

    data.insert(0, header)  # insert header

    with open("data/features.csv", "w") as output_f:
        writer = csv.writer(output_f)
        writer.writerows(data)

if __name__ == "__main__":
    main()
