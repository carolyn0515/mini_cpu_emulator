"""tests/test_decoder.py"""
import unittest
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.decoder import decode
from core.exceptions import UnknownOpcodeError, InvalidInstructionError, InvalidOperandError

class TestDecoder(unittest.TestCase):
    def test_decode_add(self):
        instr = decode("+ 0x3 0x2")
        self.assertEqual(instr.opcode, '+'); self.assertEqual(instr.op1, '0x3')
    def test_decode_mov_register(self):
        instr = decode("M R2 0x5")
        self.assertEqual(instr.opcode, 'M'); self.assertEqual(instr.op1, 'R2')
    def test_decode_halt(self):
        self.assertEqual(decode("H R0 R0").opcode, 'H')
    def test_strips_comment(self):
        instr = decode("+ 0x1 0x2  # comment")
        self.assertEqual(instr.op1, '0x1')
    def test_unknown_opcode(self):
        with self.assertRaises(UnknownOpcodeError): decode("X 0x1 0x2")
    def test_mov_op1_must_be_reg(self):
        with self.assertRaises(InvalidInstructionError): decode("M 0x3 0x2")
    def test_invalid_operand(self):
        with self.assertRaises(InvalidOperandError): decode("+ abc 0x2")

if __name__ == '__main__': unittest.main()
