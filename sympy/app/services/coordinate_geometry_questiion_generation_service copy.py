import random
import sympy as sp
import math

from app.services.base_quetion_generator_service import BaseQuestionGeneratorService


def generate_points(difficulty):
    if difficulty == 1:
        # Numeric points with integer coordinates
        x1, y1 = random.randint(-10, 10), random.randint(-10, 10)
        x2, y2 = random.randint(-10, 10), random.randint(-10, 10)
        return (x1, y1), (x2, y2)
    elif difficulty == 2:
        # Numeric points with square root coordinates
        x1, y1 = random.choice(
            [math.sqrt(random.randint(1, 10)), 
             random.randint(-10, 10)
             ]), 
        random.choice(
            [math.sqrt(random.randint(1, 10)), 
             random.randint(-10, 10)
             ])
        x2, y2 = random.choice(
            [math.sqrt(random.randint(1, 10)), 
             random.randint(-10, 10)]), 
        random.choice(
            [math.sqrt(random.randint(1, 10)), 
             random.randint(-10, 10)])
        return (x1, y1), (x2, y2)
    elif difficulty == 3:
        # Symbolic points with variables a, b
        a, b = sp.symbols('a b')
        return (a, b), (b, a)
    elif difficulty == 4:
        # Symbolic points with expressions involving variables
        a, b, c, d, e = sp.symbols('a b c d e')
        return (a + e, b + e), (c + e, d + e)
    else:
        return None, None


def calculate_distance(point1, point2, difficulty):
    if difficulty in [1, 2]:
        # Numeric distance calculation
        return round(math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2), 2)
    elif difficulty in [3, 4]:
        # Symbolic distance calculation
        return sp.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)


def generate_mcq_answers(correct_answer, difficulty):
    if difficulty in [1, 2]:
        # Numeric incorrect answers
        incorrect_answers = [round(correct_answer + random.uniform(-2, 2), 2) for _ in range(4)]
    else:
        # Symbolic incorrect answers
        a, b, c, d, e = sp.symbols('a b c d e')
        incorrect_answers = [
            correct_answer + sp.Rational(1, 2),
            correct_answer - sp.Rational(1, 2),
            correct_answer + a,
            correct_answer - b
        ]
    answers = incorrect_answers + [correct_answer]
    random.shuffle(answers)
    return answers


class CoordinateGeometryQuestionGeneratorService(BaseQuestionGeneratorService):

    def generate_answers(self) -> list:
        pass

    def format_questions(self):
        pass
    
    def generate_22_E_1__2_43_questions(self,section: str, difficulty: int, questions_count: int):

        def generate_line(difficulty):
            if difficulty == 1:
                # y = mx + c form
                m = random.randint(-5, 5)
                c = random.randint(-10, 10)
                x, y = sp.symbols('x y')
                line = sp.Eq(y, m*x + c)
            elif difficulty == 2:
                # x = a or y = b (parallel to y or x axis)
                if random.choice([True, False]):
                    a = random.randint(-10, 10)
                    line = sp.Eq(x, a)
                else:
                    b = random.randint(-10, 10)
                    line = sp.Eq(y, b)
            elif difficulty == 3:
                # General form ax + by + c = 0
                a = random.randint(-10, 10)
                b = random.randint(-10, 10)
                c = random.randint(-10, 10)
                x, y = sp.symbols('x y')
                line = sp.Eq(a*x + b*y + c, 0)
            else:
                return None

            return line

        def generate_point():
            # Generate a random point (x, y)
            x = random.randint(-10, 10)
            y = random.randint(-10, 10)
            return (x, y)

        def generate_perpendicular_question(difficulty):
            line = generate_line(difficulty)
            point = generate_point()
            x, y = sp.symbols('x y')
            question = {
                'line': line,
                'point': point,
                'question': f"Choose an equation of the line that is perpendicular to the given line {line} and passes through the given point P = {point}."
            }
            return question
# To test the functions

# question_generator = CoordinateGeometryQuestionGeneratorService()
# difficulty1 = question_generator.generate_type_1_questions("section1",1,10)
# for a in difficulty1.get("questions"):
#     print(a.get("question"))
#     print(a.get("answers"))
#     print(a.get("correct_answer"))

# difficulty2 = question_generator.generate_type_1_questions("section1",2,10)
# for a in difficulty2.get("questions"):
#     print(a.get("question"))
#     print(a.get("answers"))
#     print(a.get("correct_answer"))

# difficulty3 = question_generator.generate_type_1_questions("section1",3,10)
# for a in difficulty3.get("questions"):
#     print(a.get("question"))
#     print(a.get("answers"))
#     print(a.get("correct_answer"))

# difficulty4 = question_generator.generate_type_1_questions("section1",4,10)
# for a in difficulty4.get("questions"):
#     print(a.get("question"))
#     print(a.get("answers"))
#     print(a.get("correct_answer"))