import random
from enum import Enum

class Rule(Enum):
    MULTIPLY = "multiply"
    ADD = "add"
    SUBTRACT = "subtract"
    DIVIDE = "divide"

def generateCustomAnswer(rule, correct_answer):
    rules={
        Rule.ADD.value: random.randint(1,10)+correct_answer,
        Rule.SUBTRACT.value: random.randint(1,10)-correct_answer,
        Rule.MULTIPLY.value: random.randint(1,10)*correct_answer,
        Rule.DIVIDE.value: random.randint(1,10)/correct_answer
    }
    return rules[rule]

def generateCustomeAnswerList(rule, correct_answer, count):
    answers = []
    while len(answers) < count:
        answer = generateCustomAnswer(rule, correct_answer)
        if answer not in answers and answer != correct_answer:
            answers.append(answer)
            
    return answers

