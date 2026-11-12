
import unittest
from unittest.mock import patch

from parser import parser
from semantic import semantic_analysis
from intermediate import generate_tac
from interpreter import execute_tac


class TestCompiler(unittest.TestCase):

    def test_valid_declaration_and_print(self):
        code = "int a = 10; print(a);"
        ast = parser.parse(code)

        self.assertIsNotNone(ast)
        self.assertEqual(ast[0], ('declare', 'a', 10))

        with patch("builtins.print") as mock_print:
            semantic_analysis(ast)

        mock_print.assert_called_once_with("Output: 10")

    def test_arithmetic_operations(self):
        code = "int a = 10 + 5 - 3; print(a);"
        ast = parser.parse(code)

        with patch("builtins.print") as mock_print:
            semantic_analysis(ast)

        mock_print.assert_called_once_with("Output: 12")

    def test_operator_precedence(self):
        code = "int a = 5 + 10 * 2; print(a);"
        ast = parser.parse(code)

        with patch("builtins.print") as mock_print:
            semantic_analysis(ast)

        mock_print.assert_called_once_with("Output: 25")

    def test_syntax_error(self):
        code = "int a = 10 print(a);"

        with self.assertRaises(Exception):
            parser.parse(code)

    def test_undeclared_variable(self):
        code = "print(x);"
        ast = parser.parse(code)

        with self.assertRaisesRegex(
            Exception, "Variable 'x' not declared"
        ):
            semantic_analysis(ast)

    def test_division_by_zero(self):
        code = "int a = 10 / 0;"
        ast = parser.parse(code)

        with self.assertRaisesRegex(
            Exception, "Division by zero"
        ):
            semantic_analysis(ast)

    def test_tac_generation(self):
        code = "int a = 5 + 10; print(a);"
        ast = parser.parse(code)
        tac = generate_tac(ast)

        self.assertEqual(
            tac,
            ["t1 = 5 + 10", "a = t1", "print a"]
        )

    def test_interpreter_output(self):
        tac = [
            "a = 10",
            "b = 20",
            "t1 = a + b",
            "print t1"
        ]

        with patch("builtins.print") as mock_print:
            execute_tac(tac)

        mock_print.assert_called_once_with("FINAL OUTPUT: 30")

    def test_runtime_undeclared_variable(self):
        tac = ["print x"]

        with self.assertRaisesRegex(
            Exception, "Variable 'x' not declared"
        ):
            execute_tac(tac)

    def test_interpreter_division_by_zero(self):
        tac = [
            "a = 10",
            "b = 0",
            "t1 = a / b",
            "print t1"
        ]

        with self.assertRaisesRegex(
            Exception, "Division by zero"
        ):
            execute_tac(tac)


if __name__ == "__main__":
    unittest.main()
