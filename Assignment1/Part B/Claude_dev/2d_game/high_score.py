import json
import os

class HighScore:
    def __init__(self):
        self.file_path = "high_scores.json"
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return []

    def save_high_scores(self):
        with open(self.file_path, "w") as file:
            json.dump(self.high_scores, file)

    def add_score(self, name, score):
        self.high_scores.append({"name": name, "score": score})
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep only top 10 scores
        self.save_high_scores()

    def get_high_scores(self):
        return self.high_scores