class Suspect():
    def __init__(self, name : str, starter_dialogue : str, location : tuple[int, int]) -> None:
        self.name = name
        self.location = location
        self.starter_dialogue = starter_dialogue
        self.questionsAndAnswers = []

    def checkVillainy(self) -> bool:
        return False

    def addQuestionAndAnswer(self, question, answer):
        self.questionsAndAnswers.append((question, answer))
        return self

class Villain(Suspect):
    def checkVillainy(self) -> bool:
        return True

