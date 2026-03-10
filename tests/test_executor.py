"""tests/test_executor.py"""
import unittest
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.executor import Executor, HALT_SENTINEL
from core.registers import RegisterFile
from core.decoder import decode
from core.exceptions import DivisionByZeroError
from ioutils.tracer import Tracer

def make(self):
    self.reg = RegisterFile()
    self.ex = Executor(self.reg, Tracer(silent=True))

class TestExecutor(unittest.TestCase):
    def setUp(self): make(self)
    def test_add(self):
        self.ex.execute(decode("+ 0x3 0x2"), 0); self.assertEqual(self.reg.read_result(), 5)
    def test_sub(self):
        self.ex.execute(decode("- 0xA 0x3"), 0); self.assertEqual(self.reg.read_result(), 7)
    def test_mul(self):
        self.ex.execute(decode("* 0x4 0x3"), 0); self.assertEqual(self.reg.read_result(), 12)
    def test_div(self):
        self.ex.execute(decode("/ 0xC 0x4"), 0); self.assertEqual(self.reg.read_result(), 3)
    def test_div_zero(self):
        with self.assertRaises(DivisionByZeroError): self.ex.execute(decode("/ 0x5 0x0"), 1)
    def test_mov(self):
        self.ex.execute(decode("M R3 0x7"), 0); self.assertEqual(self.reg.read(3), 7)
    def test_mov_from_reg(self):
        self.reg.write(2, 99); self.ex.execute(decode("M R5 R2"), 0)
        self.assertEqual(self.reg.read(5), 99)
    def test_jump(self):
        self.assertEqual(self.ex.execute(decode("J 0x5 R0"), 0), 5)
    def test_compare_lt(self):
        self.ex.execute(decode("C 0x3 0x5"), 0); self.assertEqual(self.reg.read_result(), 1)
    def test_compare_ge(self):
        self.ex.execute(decode("C 0x5 0x3"), 0); self.assertEqual(self.reg.read_result(), 0)
    def test_branch_taken(self):
        self.reg.write_result(1); self.assertEqual(self.ex.execute(decode("B 0x9 R0"), 3), 9)
    def test_branch_not_taken(self):
        self.reg.write_result(0); self.assertEqual(self.ex.execute(decode("B 0x9 R0"), 3), 4)
    def test_halt(self):
        self.assertEqual(self.ex.execute(decode("H R0 R0"), 0), HALT_SENTINEL)

if __name__ == '__main__': unittest.main()
