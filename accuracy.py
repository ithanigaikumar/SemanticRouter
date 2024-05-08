import json
from semantic_router import Route
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.layer import RouteLayer


# New filename for the combined data
filename = "combined_data.json"
# Sort out data


def load_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


test_data_math = load_from_json(filename)
# unpack the test data
X, y = zip(*test_data_math)
# Rputes initialisation


# Initialise routes:
math_route = Route(
    name="maths",
    utterances=[
        "Solve for x in the equation 3x - 7 = 2x + 8",
        "Calculate the integral of x^2 from 0 to 1",
        "Determine the derivative of f(x) = 3x^3 - 5x + 6",
        "Provide a proof for the Pythagorean theorem",
        "How do you find the percentage of 50 in 200?",
        "Calculate the determinant of the 2x2 matrix [[1, 2], [3, 4]]",
        "What is the sum of 2 + 2?",
        "Expand the polynomial (x+1)^3",
        "Calculate the area of a circle with a radius of 5 units",
        "Explain the Pythagorean theorem and its applications",
        "Find the volume of a cone with a radius of 3 units and a height of 5 units",
        "Simplify the square root of 144",
        "Solve the system of equations 2x + 3y = 5 and 4x - y = 2",
        "Calculate the slope of the line passing through the points (2, 3) and (5, 7)",
        "Factorize the quadratic x^2 - 5x + 6",
        "Explain Euler's formula and its significance in complex analysis",
        "Calculate the cosine of a 45-degree angle",
        "List all prime numbers up to 100",
        "Solve the quadratic equation x^2 - 4x + 4 = 0",
        "Explain the concept of logarithms and their real-world applications",
        "Calculate the sum of the arithmetic series 3 + 7 + 11 + ... up to n terms",
        "Find the limit as x approaches 2 of the function (x^2 - 4)/(x - 2)",
        "Describe the binomial theorem and its use in algebra",
        "Compute the compound interest for an initial investment of 1000 dollars at 5% per year for 10 years",
        "Derive the formula for the circumference of a circle",
        "If set A = {1, 2, 3, 4} and set B = {3, 4, 5, 6}, what is the intersection of A and B?",
        "How many different ways can you rearrange the letters in the word 'MATH'?"
    ]

)

coding_route = Route(
    name="code",
    utterances=[
        "How to reverse a string in Python?",
        "What is the difference between == and === in JavaScript?",
        "How to sort an array of integers in C++?",
        "Write a function in Java to check if a number is prime",
        "How to merge two dictionaries in Python?",
        "Explain the use of arrow functions in JavaScript.",
        "How to handle exceptions in Java?",
        "Write a program in C to find the Fibonacci sequence up to n terms",
        "How to read and write files in Python?",
        "Explain polymorphism in object-oriented programming with a C++ example",
        "What is recursion and provide a C# example?",
        "How to find the maximum value in a JavaScript array?",
        "How to implement a queue using arrays in C?",
        "What is a decorator in Python and how can you create one?",
        "How to check if two strings are anagrams in Java?",
        "Write a SQL query to find the second highest salary from the Employees table",
        "How to convert a JavaScript array of strings to integers?",
        "What is the difference between deep copy and shallow copy in Python?",
        "How to find the intersection of two arrays in JavaScript without using set operations?",
        "What is a lambda function in Python and how is it used?",
        "How to implement a simple linear search algorithm in C++?",
        "Write a JavaScript function to count the occurrences of a character in a string",
        "How to implement a binary search algorithm in Java?",
        "What are the different ways to iterate over a dictionary in Python?",
        "How to calculate the sum of elements in an array using a loop in C?"
    ]

)

# List of all routes
routes = [math_route, coding_route]

encoder = HuggingFaceEncoder()
rl = RouteLayer(encoder=encoder, routes=routes)
# evaluate using the default thresholds
accuracy = rl.evaluate(X=X, y=y)
print(f"Accuracy: {accuracy*100:.2f}%")
route_thresholds = rl.get_thresholds()
print("Default route thresholds:", route_thresholds)
rl.fit(X=X, y=y)
route_thresholds = rl.get_thresholds()
print("Updated route thresholds:", route_thresholds)
accuracy = rl.evaluate(X=X, y=y)
print(f"Accuracy after fitting: {accuracy*100:.2f}%")
