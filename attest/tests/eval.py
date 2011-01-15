from attest import Tests, Assert
from attest.eval import evalexpr


suite = Tests()

@suite.test
def eval():
    value = 1 + 1

    samples = {
        'isinstance(value, int)': 'isinstance(2, int)',
        'value == int("2")': "(2 == int('2'))",
        'value == 5 - 3': '(2 == 2)',
        '{"value": value}': "{'value': 2}",
    }

    for expr, result in samples.iteritems():
        Assert(evalexpr(expr)) == result
