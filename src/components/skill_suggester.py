class SkillSuggester:

    def __init__(self):

        self.job_skills = {
            "machine learning engineer": [
                "python",
                "machine learning",
                "tensorflow",
                "pytorch",
                "sql"
            ],

            "data analyst": [
                "python",
                "sql",
                "pandas",
                "numpy",
                "data visualization"
            ],

            "backend developer": [
                "python",
                "flask",
                "django",
                "apis",
                "sql"
            ]
        }

    def suggest_skills(self, extracted_skills):

        suggestions = {}

        for job, skills in self.job_skills.items():

            missing = []

            for skill in skills:
                if skill not in extracted_skills:
                    missing.append(skill)

            suggestions[job] = missing

        return suggestions