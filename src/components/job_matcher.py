from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class JobMatcher:

    def __init__(self):

        self.jobs = [
            "Python developer with Flask and SQL experience",
            "Machine learning engineer with Python and TensorFlow",
            "Data analyst with SQL, Pandas and data visualization",
            "Frontend developer with React and JavaScript",
            "Backend developer with Django and APIs"
        ]

    def match_jobs(self, resume_text):

        documents = self.jobs + [resume_text]

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

        scores = similarity.flatten()

        ranked_jobs = sorted(
            zip(self.jobs, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked_jobs