import random
import sympy as sp
from fractions import Fraction
from app.models.dataModels import LatexStringModel, LatexObject
from app.utils.helpers import  generate_integer_or_fraction

# Define the variables
x, y = sp.symbols('x y')

def generate_parallel():
    # Generate a random slope for the first equation
    slope = generate_integer_or_fraction(-10, 10)
    intercept = generate_integer_or_fraction(-10, 10)
    eq1 = sp.Eq(y, slope * x + intercept)

    # The second equation will have the same slope
    intercept2 = generate_integer_or_fraction(-10, 10)
    eq2 = sp.Eq(y, slope * x + intercept2)

    return eq1, eq2

def generate_perpendicular():
    # Generate a random slope for the first equation
    slope = generate_integer_or_fraction(-10, 10)
    intercept = generate_integer_or_fraction(-10, 10)
    eq1 = sp.Eq(y, slope * x + intercept)

    # The second equation will have the negative reciprocal of the first slope
    if slope != 0:  # Avoid division by zero
        slope_perpendicular = Fraction(-1 , slope)
    else:
        slope_perpendicular = random.randint(-5, 5) + 1
    intercept2 = generate_integer_or_fraction(-10, 10)
    eq2 = sp.Eq(y, slope_perpendicular * x + intercept2)
    
    return eq1, eq2

def generate_neither():
    # Generate two random slopes and intercepts
    slope1 = generate_integer_or_fraction(-10, 10)
    intercept1 = generate_integer_or_fraction(-10, 10)
    eq1 = sp.Eq(y, slope1 * x + intercept1)

    slope2 = generate_integer_or_fraction(-10, 10)
    intercept2 = generate_integer_or_fraction(-10, 10)

    # Ensure the slopes are not equal (not parallel) and not negative reciprocals (not perpendicular)
    while slope1 == slope2 or slope1 == -1 / slope2:
        slope2 = random.randint(-5, 5) + random.random()

    eq2 = sp.Eq(y, slope2 * x + intercept2)

    return eq1, eq2

def generate_difficulty_level_1_equations():
    # Choose randomly between parallel, perpendicular, and neither
    choice = random.choice(['parallel', 'perpendicular', 'neither'])
    eq1, eq2 = None, None
    if choice == 'parallel':
        eq1, eq2 = generate_parallel()
    elif choice == 'perpendicular':
        eq1, eq2 = generate_perpendicular()
    else:
        eq1, eq2 = generate_neither()
    other_choices = [selection for selection in ['parallel', 'perpendicular', 'neither'] if selection != choice]
    return eq1, eq2, choice, other_choices

def generate_vertical_lines():
    """Generate a pair of vertical lines (x = k)."""
    x1 = random.randint(-10, 10)  # Random integer for x
    x2 = random.randint(-10, 10)
    while x2 == x1:  # Ensure they are not the same line
        x2 = random.randint(-10, 10)
    return sp.Eq(x,x1), sp.Eq(x,x2)

def generate_horizontal_lines():
    """Generate a pair of horizontal lines (y = k)."""
    y1 = random.randint(-10, 10)  # Random integer for y
    y2 = random.randint(-10, 10)
    while y2 == y1:  # Ensure they are not the same line
        y2 = random.randint(-10, 10)
    return sp.Eq(y,y1), sp.Eq(y,y2)

def generate_mixed_lines():
    """Generate one vertical line and one horizontal line."""
    x1 = random.randint(-10, 10)
    y1 = random.randint(-10, 10)
    return sp.Eq(x,x1), sp.Eq(y,y1)

def generate_difficulty_level_2_equations():
    # Choose randomly between vertical, horizontal, and mixed
    choice = random.choice(['vertical', 'horizontal', 'mixed'])
    eq1, eq2 = None, None
    if choice == 'vertical':
        eq1, eq2 = generate_vertical_lines()
    elif choice == 'horizontal':
        eq1, eq2 = generate_horizontal_lines()
    else:
        eq1, eq2 = generate_mixed_lines()
    # choice = 'parallel' if (choice == 'vertical' or 'horizontal') else 'perpendicular'
    if(choice == 'vertical' or choice == 'horizontal'):
        choice = 'parallel'
    else:
        choice = 'perpendicular'
    other_choices = [selection for selection in ['parallel', 'perpendicular', 'neither'] if selection != choice]
    return eq1, eq2, choice, other_choices

def generate_difficulty_level_3_equations():
    choice = random.choice(['parallel', 'perpendicular', 'neither'])
    intercept1 = generate_integer_or_fraction(-10, 10)

    # Generate the first equation in the form ax + by = c
    a1 = generate_integer_or_fraction(-10, 10)
    b1 = generate_integer_or_fraction(-10, 10)
    eq1 = sp.Eq(a1 * x + b1 * y, intercept1)

    if choice == 'parallel':
        # For parallel, ensure the same ratio for a and b
        intercept2 = generate_integer_or_fraction(-10, 10)
        eq2 = sp.Eq(a1 * x + b1 * y, intercept2)
    elif choice == 'perpendicular':
        # For perpendicular, ensure slopes are negative reciprocals
        intercept2 = generate_integer_or_fraction(-10, 10)
        a2 = -b1
        b2 = a1
        eq2 = sp.Eq(a2 * x + b2 * y, intercept2)
    else:
        # For neither, ensure coefficients are not equal or negative reciprocals
        intercept2 = generate_integer_or_fraction(-10, 10)
        a2 = generate_integer_or_fraction(-10, 10)
        b2 = generate_integer_or_fraction(-10, 10)

        while a1 * b2 == b1 * a2 or (a1 * a2 + b1 * b2 == 0):
            a2 = generate_integer_or_fraction(-10, 10)
            b2 = generate_integer_or_fraction(-10, 10)

        eq2 = sp.Eq(a2 * x + b2 * y, intercept2)
    other_choices = [selection for selection in ['parallel', 'perpendicular', 'neither'] if selection != choice]

    return eq1, eq2, choice, other_choices

def generate_equestion(difficulty: int):
    if difficulty == 1:
        return generate_difficulty_level_1_equations()
    elif difficulty == 2:
        return generate_difficulty_level_2_equations()
    else:
        return generate_difficulty_level_3_equations()

def generate_problem_22_E_1__2_27_questions(difficulty: int,
                                    questions_count: int):
    equations_and_solutions = []

    for _ in range(questions_count):
        eq1, eq2, choice, other_choices = generate_equestion(difficulty)
        
        equations_and_solutions.append({
            "question": LatexStringModel(
                placeholders=[LatexObject(eq1, False, False),
                              LatexObject(eq2, False, False)],
                string_value="Choose whether {} and {} lines are parallel, perpendicular, or neither."
            ).convert_to_latex(),
            "solution": choice,
            "other_solutions": other_choices
        })
    return equations_and_solutions