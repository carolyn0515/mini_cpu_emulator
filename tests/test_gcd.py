"""tests/test_gcd.py"""
import unittest, os, tempfile
import sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.cpu import CPU
from ioutils.loader import load
from ioutils.tracer import Tracer

GCD_PROGRAM = os.path.join(os.path.dirname(__file__), '..', 'programs', 'input_gcd.txt')

def run_gcd(a, b):
    prog = (
        f"M R1 {hex(a)}\nM R2 {hex(b)}\n"
        "C R2 0x1\nB 0xD R0\n"
        "M R3 R1\nC R3 R2\nB 0xA R0\n"
        "- R3 R2\nM R3 R0\nJ 0x5 R0\n"
        "M R1 R2\nM R2 R3\nJ 0x2 R0\n"
        "H R0 R0\n"
    )
    cpu = CPU(tracer=Tracer(silent=True))
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(prog); fname = f.name
    load(fname, cpu.memory); cpu.run(); os.unlink(fname)
    return cpu.registers.read(1)

class TestGCD(unittest.TestCase):
    def test_gcd_file(self):
        cpu = CPU(tracer=Tracer(silent=True))
        load(GCD_PROGRAM, cpu.memory); cpu.run()
        self.assertEqual(cpu.registers.read(1), 4)
    def test_gcd_12_8(self):   self.assertEqual(run_gcd(12, 8), 4)
    def test_gcd_48_18(self):  self.assertEqual(run_gcd(48, 18), 6)
    def test_gcd_100_75(self): self.assertEqual(run_gcd(100, 75), 25)
    def test_gcd_coprime(self):self.assertEqual(run_gcd(7, 13), 1)

if __name__ == '__main__': unittest.main()
