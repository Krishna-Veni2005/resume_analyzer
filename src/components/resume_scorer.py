class ResumeScorer:

    def __init__(self):

        self.expected_skills = [
            "python",
            "sql",
            "machine learning",
            "deep learning",
            "pandas",
            "numpy",
            "scikit-learn",
            "tensorflow",
            "pytorch",
            "flask"
        ]


    def calculate_score(self, extracted_skills):

        matched_skills = []

        for skill in extracted_skills:
            if skill in self.expected_skills:
                matched_skills.append(skill)

        score = (len(matched_skills) / len(self.expected_skills)) * 100

        return score, matched_skills