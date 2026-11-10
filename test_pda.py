import unittest
from pda_cfg_validator import (
    validate_parentheses_pda,
    validate_arithmetic_pda,
    validate_conditional_pda
)

class TestPDACFGCases(unittest.TestCase):

    def test_balanced_parentheses(self):
        self.assertTrue(validate_parentheses_pda("{[()()]}")[0])
        self.assertFalse(validate_parentheses_pda("([)]")[0])
        self.assertFalse(validate_parentheses_pda("((()")[0])

    def test_arithmetic_expressions(self):
        self.assertTrue(validate_arithmetic_pda("id + id * id")[0])
        self.assertTrue(validate_arithmetic_pda("id * (id + id)")[0])
        self.assertFalse(validate_arithmetic_pda("id + * id")[0])
        self.assertFalse(validate_arithmetic_pda("(id + id")[0])

    def test_conditional_syntax(self):
        self.assertTrue(validate_conditional_pda("if c then if c then a else a")[0])
        self.assertTrue(validate_conditional_pda("if c then a else a")[0])
        self.assertFalse(validate_conditional_pda("if c then a else a else a")[0])
        self.assertFalse(validate_conditional_pda("if c else a")[0])

if __name__ == "__main__":
    unittest.main(verbosity=2)