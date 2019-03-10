"""
Perform LSA and measure the similarity of post content with syllabus

Prerequisites:
    - Syllabus files for a classes
    - Place all files under 'data/syllabus'
    - If the format is not plaintext file,
      use the script 'misc/extract_txt.py' to convert them in advanced
    - Filename should follow the convention of '<class_id>.txt'

Usage:
    python off_topic_analysis.py

References:
    - https://radimrehurek.com/gensim/tut3.html
    - http://www.cs.bham.ac.uk/~pxt/IDA/lsa_ind.pdf
"""
import os

from collections import defaultdict
from gensim import corpora, similarities
from gensim.models import LsiModel
from gensim.parsing import remove_stopwords

from brossessment.models import *

# A list of common English words
STOP_LIST = set(
    "for a of the and to in assignment project late online ocurse week discussion learning outline".split()
)


def prepare_index(doc_path):
    """
    Presist dictionary, corpus, and index into disk
    So they can be reused later on
    """
    with open(doc_path) as input_f:
        file_name, _ = os.path.splitext(doc_path)
        raw_syllabus = input_f.read().replace("\n", "")
        documents = [remove_stopwords(raw_syllabus)]
        texts = [
            [word for word in document.lower().split() if word not in STOP_LIST]
            for document in documents
        ]

        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        texts = [[token for token in text if frequency[token] > 1] for text in texts]

        dictionary = corpora.Dictionary(texts)
        dictionary.save("{}.dict".format(file_name))

        corpus = [dictionary.doc2bow(text) for text in texts]
        corpora.MmCorpus.serialize("{}.mm".format(file_name), corpus)

        lsi = LsiModel(corpus, id2word=dictionary, num_topics=1)
        index = similarities.MatrixSimilarity(lsi[corpus])
        index.save("{}.index".format(file_name))


def get_similarity(lsi, dictionary, index, input_doc):
    """
    Perform a similarity query against the corpus
    """
    vec_bow = dictionary.doc2bow(input_doc.lower().split())
    vec_lsi = lsi[vec_bow]  # convert the query to LSI space
    sims = index[vec_lsi]
    return list(enumerate(sims))[0][1]


def get_chunk(class_id, begin_post_id=0, limit=500):
    posts = (
        Post.select(Post.post_id, Post.content)
        .where(Post.post_id > begin_post_id, Post.class_id == class_id)
        .order_by(Post.post_id)
        .limit(limit)
    )
    return posts


def main():
    class_list = [c["class_id"] for c in Class.select().dicts()]

    begin_post_id = 0
    total_updated_records = 0
    for each in class_list:
        # Check if similarity index has been built for the syllabus
        if not os.path.isfile("data/syllabus/{}.index".format(each)):
            prepare_index("data/syllabus/{}.txt".format(each))

        # Load corpus and stuffs from disk
        dictionary = corpora.Dictionary.load("data/syllabus/{}.dict".format(each))
        corpus = corpora.MmCorpus("data/syllabus/{}.mm".format(each))
        index = similarities.MatrixSimilarity.load(
            "data/syllabus/{}.index".format(each)
        )

        # # init Laten Semantic Index model
        lsi = LsiModel(corpus, id2word=dictionary, num_topics=1)

        while True:
            current_chunk = get_chunk(each, begin_post_id, 100)

            if not current_chunk:
                begin_post_id = 0
                break

            print(
                "Fetching LSI similarity score from {} to {} within class {}".format(
                    current_chunk[0].post_id, current_chunk[-1].post_id, each
                )
            )

            result = {}
            for post in current_chunk:
                post_id = post.post_id
                content = post.content

                if not content:
                    continue

                try:
                    score = get_similarity(lsi, dictionary, index, content)
                except Exception as e:
                    print(e)
                    print("{} fail to get similarity score".format(post_id))

                result[post_id] = {"post_id": post_id, "similarity_score": score}

            with postgres_db.atomic():
                for key, value in result.items():
                    query = Post.update(
                        lsi_similarity_score=value["similarity_score"]
                    ).where(Post.post_id == key)
                    cnt = query.execute()
                    total_updated_records += cnt

            begin_post_id = current_chunk[-1].post_id

        begin_post_id = 0
        result = {}

    print("Total updated record: {}".format(total_updated_records))


if __name__ == "__main__":
    main()
