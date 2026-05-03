class SkillExtractor:

    def __init__(self):

        self.skill_list = [
            "python",
            "java",
            "sql",
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "flask",
            "django",
            "react",
            "javascript",
            "html",
            "css",
            "pandas",
            "numpy",
            "scikit-learn"
        ]


    def extract_skills(self, text):

        text = text.lower()

        extracted_skills = []

        for skill in self.skill_list:
            if skill in text:
                extracted_skills.append(skill)

        return extracted_skills