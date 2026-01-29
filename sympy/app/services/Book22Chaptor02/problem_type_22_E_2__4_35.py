import random
from typing import Any, Dict, List

import sympy as sp

from app.models.dataModels import LatexStringModel, ServiceResponce, LatexObject
from app.services.mcqRuleService import generateCustomeAnswerList, Rule
from app.utils.helpers import random_non_zero_real, randint_exclude_list, generate_general_constant_number, generate_general_constant_without_sqrt

class RandomFactoredExpressionGenerator:
    def __init__(self, variable):
        self.variable = variable

    def generate_factor(self):
        a = randint_exclude_list(-5, 5)  # Coefficient of x
        b = random.randint(-5, 5)  # Constant term
        return a * self.variable + b

    def generate_fully_factorizable_expression(self, variable, constant, degree, avoid_double_root_at=None):
        if degree == 1:
            return variable - constant
        else:
            expression = variable - constant
            for _ in range(degree - 1):
                factor = self.generate_factor()
                while avoid_double_root_at is not None and factor == (variable - avoid_double_root_at):
                    factor = self.generate_factor()  # Regenerate to avoid double root
                expression *= factor
            return expression

def generate_22_E_2__4_35_questions(difficulty: int,
                                    questions_count: int) -> List[ServiceResponce]:
    questions_and_answers = []
    x, k = sp.symbols('x k')

    for _ in range(questions_count):

        symbol = sp.Symbol(random.choice(['x', 'y', 't', 'u', 'v', 'z', 'r', 's']))
        limit_dir = random.choice(['+', '-'])
        # Choose question type based on the following randomly
        # Type:
        # 1 -> E_22_2.2_01
        # 2 -> E_22_2.3_21
        # 3 -> E_22_2.3_25
        question_type = random.randint(1, 3)
        piecewise_function = None

        def generate_limit_question_for_question_type_2__3_21(difficulty: int) -> Dict[str, Any]:
            other_solutions = None
            a = random_non_zero_real([4, 1, 1, 0])
            b = random_non_zero_real([4, 1, 1, 0])

            question_expr = None

            if difficulty == 1:
                # Randomly select the form of the limit question
                if random.choice([True, False]):
                    # Form: lim x -> 0 (sin(ax) / (bx))

                    expr = sp.sin(a * x) / (b * x)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                else:
                    # Form: lim x -> 0 (bx / sin(ax))
                    expr = (b * x) / sp.sin(a * x)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
            elif difficulty == 2:
                # Randomly select the form of the limit question
                a = random.randint(1, 20)
                b = random.randint(1, 20)
                c = random.randint(1, 4)
                if c == 4:
                    c = 3
                    d = 4
                else:
                    d = random.choice([c, c, random.randint(c, 4), random.randint(c, 4), random.randint(c, 4)])
                if random.choice([True, False]):
                    # Form: lim x -> 0 (sin^2(ax) / (bx^2))
                    expr = (sp.sin(a * x) ** d) / (b * x ** c)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                else:
                    # Form: lim x -> 0 (bx^2 / sin^2(ax))
                    expr = (b * x ** d) / (sp.sin(a * x) ** c)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
            elif difficulty == 3:
                a = random.randint(1, 10)
                b = random.randint(11, 20)
                # Randomly select the form of the limit question
                if random.choice([True, False]):
                    # Form: lim x -> 0 (sin(ax) / sin(bx))
                    expr = sp.sin(a * x) / sp.sin(b * x)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                else:

                    expr = sp.sin(b * x) / sp.sin(a * x)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
            elif difficulty == 4:

                choice = random.choice([1, 2, 3, 4])
                if choice == 1:
                    # Form: lim x -> 0 (1 - cos(ax) / bx^2)
                    c = random.choice([1, 2, 2, 2, 2])
                    expr = (1 - sp.cos(a * x)) / (b * x ** c)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                elif choice == 2:

                    c = random.choice([3, 4, 2, 2, 2, 2])
                    expr = (b * x ** c) / (1 - sp.cos(a * x))
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                elif choice == 3:
                    c = random.choice([1, 2, 2, 2, 2])
                    expr = (1 - sp.cos(a * x)) / (sp.sin(b * x) ** c)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                else:
                    c = random.choice([3, 4, 2, 2, 2, 2])
                    if b ** c >= 200:
                        c = 2
                        b = random.choice([3, 4, 5, 6, 7, 8])
                    expr = sp.sin(b * x) ** c / (1 - sp.cos(a * x))
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
            elif difficulty == 5:
                p = random.randint(1, 9)
                q = random.choice([i for i in range(-9, 10) if i != 0])
                a = b = 1
                transformed_x = p * x + q
                limit_value = sp.Rational(-q, p)
                sub_difficulty = random.choice([1, 2, 4])
                if sub_difficulty == 1:
                    if random.choice([True, False]):
                        expr = sp.sin(a * transformed_x) / (b * transformed_x)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                    else:
                        expr = (b * transformed_x) / sp.sin(a * transformed_x)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                elif sub_difficulty == 2:
                    c = random.randint(1, 4)
                    if c == 4:
                        c = 3
                        d = 4
                    else:
                        d = random.choice([c, c, random.randint(c, 4), random.randint(c, 4), random.randint(c, 4)])
                    if random.choice([True, False]):
                        expr = (sp.sin(a * transformed_x) ** d) / (b * transformed_x ** c)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                    else:
                        expr = (b * transformed_x ** d) / (sp.sin(a * transformed_x) ** c)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                elif sub_difficulty == 4:
                    choice = random.choice([1, 2, 3, 4])
                    if choice == 1:
                        c = random.choice([1, 2, 2, 2, 2])
                        expr = (1 - sp.cos(a * transformed_x)) / (b * transformed_x ** c)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                    elif choice == 2:
                        c = random.choice([3, 4, 2, 2, 2, 2])
                        expr = (b * transformed_x ** c) / (1 - sp.cos(a * transformed_x))
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                    elif choice == 3:
                        c = random.choice([1, 2, 2, 2, 2])
                        expr = (1 - sp.cos(a * transformed_x)) / (sp.sin(b * transformed_x) ** c)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                    else:
                        c = random.choice([3, 4, 2, 2, 2, 2])
                        if b ** c >= 200:
                            c = 2
                            b = random.choice([3, 4, 5, 6, 7, 8])
                        expr = sp.sin(b * transformed_x) ** c / (1 - sp.cos(a * transformed_x))
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
            elif difficulty == 6:
                c = random.randint(-20, 20)
                if random.choice([True, False]):
                    d = random.randint(-20, 20)
                    # Form: lim x -> -d/c (sin(ax + b) / (cx + d))
                    expr = sp.sin(a * x + b) / (c * x + d)
                    limit = sp.limit(expr, x, -d / c, dir=limit_dir)
                    question_expr = sp.Limit(expr, x, -d / c, dir=limit_dir)
                else:
                    d = random.randint(-20, 20)
                    # Form: lim x -> d/c (sin^2(ax - b) / (1 - cos(cx - d)))
                    expr = sp.sin(a * x - b) ** 2 / (1 - sp.cos(c * x - d))
                    limit = sp.limit(expr, x, d / c, dir=limit_dir)
                    question_expr = sp.Limit(expr, x, d / c, dir=limit_dir)

            return limit, question_expr

        if difficulty == 1:

            question_type = random.randint(1, 3)
            if question_type == 1:
                expression = generate_general_constant_number(-10, 10)
                constant = generate_general_constant_number(-10, 10)
                limit = sp.Limit(expression, symbol, constant, dir=limit_dir)
                solution = sp.limit(expression, symbol, constant, dir=limit_dir)
            elif question_type == 2:
                a = generate_general_constant_without_sqrt(-10, 10)
                b = generate_general_constant_without_sqrt(-10, 10)
                constant = generate_general_constant_without_sqrt(-10, 10)
                expression = a * symbol + b
                limit = sp.Limit(expression, symbol, constant, dir=limit_dir)
                solution = sp.limit(expression, symbol, constant, dir=limit_dir)
            else:
                degree = random.choice([2, 3, 4, 5, 6])
                polynomial = 0
                for i in range(degree):
                    if (degree == 2):
                        coefficient = generate_general_constant_without_sqrt(-10, 10)
                    else:
                        coefficient = random.choice([i for i in range(-10, 11) if i != 0])
                    polynomial += coefficient * symbol ** i
                constant = generate_general_constant_without_sqrt(-10, 10)
                limit = sp.Limit(polynomial, symbol, constant, dir=limit_dir)
                solution = sp.limit(polynomial, symbol, constant, dir=limit_dir)

            other_solutions = generateCustomeAnswerList(Rule.MULTIPLY.value, solution, 4)
            question = LatexStringModel(
                placeholders=[LatexObject(limit, False, True)],
                string_value="Evaluate the following one-sided limit. {}",
            ).convert_to_latex()
            other_solution_latex = [LatexStringModel(
                placeholders=[LatexObject(x, False, False)],
                string_value="{}"
            ).convert_to_latex() for x in other_solutions]

            questions_and_answers.append(ServiceResponce(
                question=question,
                correct_solution=LatexStringModel(
                    placeholders=[LatexObject(solution, False, False)],
                    string_value="{}").convert_to_latex(),
                other_solutions=other_solution_latex
            ))

        elif difficulty == 2:

            question_type = random.randint(1, 4)

            if question_type == 1:
                # Define possible limit numbers with higher probability for specific trigonometric values
                trig_values = [0, sp.pi / 6, sp.pi / 4, sp.pi / 3, sp.pi / 2, 5 * sp.pi / 6, 3 * sp.pi / 4,
                               2 * sp.pi / 3, sp.pi, 3 * sp.pi / 2, 2 * sp.pi]
                # Define possible functions
                functions = [
                    sp.Abs(symbol),
                    sp.sin(symbol),
                    sp.cos(symbol),
                    sp.tan(symbol),
                    sp.exp(symbol),
                    sp.log(symbol)
                ]

                # Randomly select a combination of functions
                selected_functions = random.sample(functions, k=random.randint(2, 3))

                if (sp.sin(symbol) in selected_functions or sp.cos(symbol) in selected_functions or sp.tan(
                        symbol) in selected_functions):
                    limit_number = random.choice(trig_values)
                else:
                    limit_number = generate_general_constant_number(-10, 10)

                if sp.log(symbol) in selected_functions:
                    limit_number = abs(limit_number)

                    # Create the expression by combining the selected functions
                expression = selected_functions[0]
                for func in selected_functions[1:]:
                    expression += func

                # Create the limit and solution
                question_exp = sp.Limit(expression, symbol, limit_number, dir=limit_dir)
                answer = sp.limit(expression, symbol, limit_number, dir=limit_dir)
                if (answer == sp.oo or answer == -sp.oo or answer == 0):
                    other_Solutions = generateCustomeAnswerList(Rule.MULTIPLY.value, random.randint(1, 10), 4)
                else:
                    other_Solutions = generateCustomeAnswerList(Rule.MULTIPLY.value, answer, 4)
            elif question_type == 2:
                answer, question_exp = generate_limit_question_for_question_type_2__3_21(2)
                other_Solutions = generateCustomeAnswerList(Rule.ADD.value, answer, 4)
            elif question_type == 3:
                # Form: lim x -> a (x^2 - a^2) / (x - a)
                a = random_non_zero_real([4, 1, 1, 0], 500, 2)
                expr = (symbol ** 2 - a ** 2) / (symbol - a)
                question_exp = sp.Limit(expr, symbol, a, dir=limit_dir)
                answer = sp.limit(expr, symbol, a, dir=limit_dir)
                other_Solutions = generateCustomeAnswerList(Rule.MULTIPLY.value, answer, 4)
            else:
                # Form: lim x -> a (x^d - a^d) / (x - a) where 3 <= d <= 5 and -500 < a^d < 500
                d = random.randint(3, 5)
                a = random_non_zero_real([4, 1, 1, 1], 500, d)

                while not (abs(a ** d) < 500):
                    d = random.randint(3, 4)
                    a = random_non_zero_real([4, 1, 1, 1], 500, d)

                expr = (symbol ** d - a ** d) / (symbol - a)
                question_exp = sp.Limit(expr, symbol, a, dir=limit_dir)
                answer = sp.limit(expr, symbol, a, dir=limit_dir)
                other_Solutions = generateCustomeAnswerList(Rule.MULTIPLY.value, answer, 4)

            questions_and_answers.append(ServiceResponce(
                question=LatexStringModel(
                    string_value="Evaluate the following one-sided limit. {} ",
                    placeholders=[LatexObject(question_exp, False, True)]
                ).convert_to_latex(),
                correct_solution=LatexStringModel(
                    string_value="{}",
                    placeholders=[LatexObject(answer)]
                ).convert_to_latex(),
                other_solutions=[LatexStringModel(
                    string_value="{}",
                    placeholders=[LatexObject(a)]
                ).convert_to_latex() for a in other_Solutions]
            ))

        elif difficulty == 3:
            question_type = random.randint(1, 4)

            if question_type == 1:
                answer, question_exp = generate_limit_question_for_question_type_2__3_21(2)
                other_Solutions = generateCustomeAnswerList(Rule.ADD.value, answer, 4)
            elif question_type == 2:
                answer, question_exp = generate_limit_question_for_question_type_2__3_21(3)
                other_Solutions = generateCustomeAnswerList(Rule.ADD.value, answer, 4)
            elif difficulty == 3:
                # Form: lim x -> a (x^d - a^d) / (x^c - a^c) where 2 <= c, d <= 5 and -500 < a^c, a^d < 500
                powers = [2, 3, 4, 5]
                c = random.choice(powers)
                powers.remove(c)
                d = random.choice(powers)
                a = random_non_zero_real([4, 1, 1, 1], 500, max(c, d))

                while not (abs(a ** c) < 500) or not (abs(a ** d) < 500):
                    powers = [2, 3, 4, 5]
                    c = random.choice(powers)
                    powers.remove(c)
                    d = random.choice(powers)
                    a = random_non_zero_real([4, 1, 1, 1], 500, max(c, d))
                expr = (symbol ** d - a ** d) / (symbol ** c - a ** c)
                question_exp = sp.Limit(expr, symbol, a, dir=limit_dir)
                answer = sp.limit(expr, symbol, a, dir=limit_dir)
                other_Solutions = generateCustomeAnswerList(Rule.MULTIPLY.value, answer, 4)
            else:
                # Form: lim x -> a (x^(1/d) - a^(1/d)) / (x^(1/c) - a^(1/c)) where d, c = 1, 2, 3 and d not equal c. If d or c even a > 0
                value_list = [1, 2, 3]
                c = random.choice(value_list)
                value_list.remove(c)
                d = random.choice(value_list)
                a = random_non_zero_real([4, 0, 0, 0])
                if c % 2 == 0 or d % 2 == 0:
                    a = abs(a)
                expr = (symbol ** (sp.Rational(1, d)) - a ** (sp.Rational(1, d))) / (
                        symbol ** (sp.Rational(1, c)) - a ** (sp.Rational(1, c)))
                question_exp = sp.Limit(expr, symbol, a, dir=limit_dir)
                answer = sp.limit(expr, symbol, a, dir=limit_dir)
                other_Solutions = generateCustomeAnswerList(Rule.MULTIPLY.value, answer, 4)

            questions_and_answers.append(ServiceResponce(
                question=LatexStringModel(
                    string_value="Evaluate the following one-sided limit. {} ",
                    placeholders=[LatexObject(question_exp, False, True)]
                ).convert_to_latex(),
                correct_solution=LatexStringModel(
                    string_value="{}",
                    placeholders=[LatexObject(answer)]
                ).convert_to_latex(),
                other_solutions=[LatexStringModel(
                    string_value="{}",
                    placeholders=[LatexObject(a)]
                ).convert_to_latex() for a in other_Solutions]
            ))

        elif difficulty == 4:
            question_type = random.randint(1, 3)

            if question_type == 1:
                answer, question_exp = generate_limit_question_for_question_type_2__3_21(4)
                other_Solutions = generateCustomeAnswerList(Rule.ADD.value, answer, 4)
            elif question_type == 2:
                answer, question_exp = generate_limit_question_for_question_type_2__3_21(5)
                other_Solutions = generateCustomeAnswerList(Rule.ADD.value, answer, 4)
            else:
                random_factored_expression_generator = RandomFactoredExpressionGenerator(symbol)
                # Form: lim x -> a (polynomial of degree 1, 2, 3 with a factor (x - a)) / (polynomial of degree 1, 2, 3 with a factor (x - a))
                # where all the polynomial easily factorisable and make sure that the denominator does not have a double root at x = a. a can be integers (slightly higher probability), fractions.
                a = random_non_zero_real([4, 1, 0, 0])
                numerator_degree = random.randint(1, 3)
                if numerator_degree == 1:
                    denominator_degree = random.randint(2, 3)
                else:
                    denominator_degree = random.randint(1, 3)
                numerator = random_factored_expression_generator.generate_fully_factorizable_expression(
                    symbol, a,
                    numerator_degree,
                    avoid_double_root_at=None).expand()
                denominator = random_factored_expression_generator.generate_fully_factorizable_expression(
                    symbol,
                    a,
                    denominator_degree,
                    avoid_double_root_at=a).expand()
                expr = numerator / denominator
                question_exp = sp.Limit(expr, symbol, a, dir=limit_dir)
                answer = sp.limit(expr, symbol, a, dir=limit_dir)
                other_Solutions = generateCustomeAnswerList(Rule.MULTIPLY.value, answer, 4)

            questions_and_answers.append(ServiceResponce(
                question=LatexStringModel(
                    string_value="Evaluate the following one-sided limit. {} ",
                    placeholders=[LatexObject(question_exp, False, True)]
                ).convert_to_latex(),
                correct_solution=LatexStringModel(
                    string_value="{}",
                    placeholders=[LatexObject(answer)]
                ).convert_to_latex(),
                other_solutions=[LatexStringModel(
                    string_value="{}",
                    placeholders=[LatexObject(a)]
                ).convert_to_latex() for a in other_Solutions]
            ))

        elif difficulty == 5:
            def generate_piece(degree):
                if degree == 0:  # Constant
                    return generate_general_constant_without_sqrt(-10, 10)
                elif degree == 1:  # Linear
                    a = generate_general_constant_without_sqrt(-10, 10)
                    b = generate_general_constant_without_sqrt(-10, 10)
                    return a * symbol + b
                elif degree == 2:  # Quadratic
                    a = generate_general_constant_without_sqrt(-10, 10)
                    b = generate_general_constant_without_sqrt(-10, 10)
                    c = generate_general_constant_without_sqrt(-10, 10)
                    return a * symbol ** 2 + b * symbol + c

            # Randomly choose breakpoints and corresponding pieces
            breakpoint = generate_general_constant_without_sqrt(-10, 10)
            left_piece = generate_piece(random.choice([0, 1, 2]))
            right_piece = generate_piece(random.choice([0, 1, 2]))

            # Define the limit at the breakpoint
            limit = sp.Limit(k, symbol, breakpoint, dir=limit_dir)
            piecewise_function = sp.Piecewise(
                (left_piece, symbol <= breakpoint),
                (right_piece, symbol > breakpoint), Evaluate=False
            )
            solution = sp.limit(piecewise_function, symbol, breakpoint, dir=limit_dir)

            other_solutions = generateCustomeAnswerList(Rule.MULTIPLY.value, random.randint(1, 10), 4)
            pf_str = LatexStringModel(
                string_value="{}",
                placeholders=[LatexObject(sp.Eq(sp.Function("f")(symbol), piecewise_function), False, True)],
            ).convert_to_latex()
            question = (LatexStringModel(
                string_value="Evaluate the following one-sided limit. {}",
                placeholders=[LatexObject(limit, False, True)],
            ).convert_to_latex().replace("k", f"f({symbol})") + f" where " + pf_str)

            other_solution_latex = [LatexStringModel(
                placeholders=[LatexObject(x, False, False)],
                string_value="{}"
            ).convert_to_latex() for x in other_solutions]
            other_solution_latex = other_solution_latex + ["Do not exist."]

            questions_and_answers.append(ServiceResponce(
                question=question,
                correct_solution=LatexStringModel(
                    placeholders=[LatexObject(solution, False, False)],
                    string_value="{}").convert_to_latex(),
                other_solutions=other_solution_latex
            ))

        else:
            raise ValueError('Unsupported difficulty level')

    return questions_and_answers