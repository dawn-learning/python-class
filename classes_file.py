
class Suspect():
    def __init__(self, name, init_dialogue) -> None:
        self.name = name
        self.init_dialogue = init_dialogue
        self.questions = []
        self.answers = []

    def addQuestionAndAnswer(self, question, answer):
        self.questions.append(question)
        self.answers.append(answer)
        return self

class Villain(Suspect):
    def isVillian(self):
        return True
