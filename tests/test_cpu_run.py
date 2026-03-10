"""tests/test_cpu_run.py"""
import unittest, tempfile, os
import sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.cpu import CPU
from ioutils.loader import load
from ioutils.tracer import Tracer

def make_cpu():
    return CPU(tracer=Tracer(silent=True))

def run_text(text):
    cpu = make_cpu()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(text); fname = f.name
    load(fname, cpu.memory); cpu.run(); os.unlink(fname)
    return cpu

class TestCPURun(unittest.TestCase):
    def test_basic_add(self):
        cpu = run_text("+ 0x3 0x2\nH R0 R0\n")
        self.assertEqual(cpu.registers.read_result(), 5)
    def test_jump_skips(self):
        cpu = run_text("M R1 0x1\nJ 0x3 R0\nM R1 0xFF\nH R0 R0\n")
        self.assertEqual(cpu.registers.read(1), 1)
    def test_branch_taken(self):
        cpu = run_text("C 0x3 0x5\nB 0x3 R0\nM R1 0xFF\nM R2 0x1\nH R0 R0\n")
        self.assertNotEqual(cpu.registers.read(1), 0xFF)
        self.assertEqual(cpu.registers.read(2), 1)
    def test_div_zero_graceful(self):
        run_text("/ 0x5 0x0\nH R0 R0\n")   
        
if __name__ == '__main__': unittest.main()
