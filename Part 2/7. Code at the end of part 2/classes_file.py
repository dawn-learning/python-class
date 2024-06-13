class Suspect():
    def __init__(self, name : str, starter_dialogue : str, location : tuple[int, int]) -> None:
        self.name = name
        self.location = location
        self.starter_dialogue = starter_dialogue
        self.questionsAndAnswers = []

    def checkVilliany(self) -> bool:
        return False

    def addQuestionAndAnswer(self, question, answer):
        self.questionsAndAnswers.append((question, answer))
        return self

class Villian(Suspect):
    def checkVilliany(self) -> bool:
        return True
