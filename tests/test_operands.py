"""tests/test_operands.py"""
import unittest
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.operands import resolve, get_register_index
from core.registers import RegisterFile
from core.exceptions import InvalidOperandError, RegisterOutOfRangeError

class TestOperands(unittest.TestCase):
    def setUp(self):
        self.reg = RegisterFile()
        self.reg.write(3, 42)

    def test_immediate_hex(self):       self.assertEqual(resolve("0xA", self.reg), 10)
    def test_immediate_ff(self):        self.assertEqual(resolve("0xFF", self.reg), 255)
    def test_register_addressing(self): self.assertEqual(resolve("R3", self.reg), 42)
    def test_register_zero(self):       self.assertEqual(resolve("R0", self.reg), 0)
    def test_invalid_format(self):
        with self.assertRaises(InvalidOperandError): resolve("abc", self.reg)
    def test_reg_out_of_range(self):
        with self.assertRaises(RegisterOutOfRangeError): resolve("R10", self.reg)
    def test_get_reg_index(self):       self.assertEqual(get_register_index("R5"), 5)
    def test_get_reg_index_invalid(self):
        with self.assertRaises(InvalidOperandError): get_register_index("0x3")

if __name__ == '__main__': unittest.main()
