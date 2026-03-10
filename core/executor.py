# opcode별 실제 실행 로직
from __future__ import annotations
from typing import TYPE_CHECKING, Callable

from core.instruction import Instruction
from core.exceptions import (
    DivisionByZeroError,
    UnknownOpcodeError,
)
from core.operands import resolve, get_register_index
from isa import opcodes as OP

if TYPE_CHECKING:
    from core.registers import RegisterFile
    from ioutils.tracer import Tracer

HALT_SENTINEL = -1

class Executor:

    def __init__(self, reg_file: "RegisterFile",
                 tracer: "Tracer | None" = None) -> None:
        self._reg = reg_file
        self._tracer = tracer

        self._handlers: dict[str, Callable[[Instruction, int], int]] = {
            OP.ADD:     self._add,
            OP.SUB:     self._sub,
            OP.MUL:     self._mul,
            OP.DIV:     self._div,
            OP.MOV:     self._mov,
            OP.JUMP:    self._jump,
            OP.COMPARE: self._compare,
            OP.BRANCH:  self._branch,
            OP.HALT:    self._halt,
        }

    def execute(self, instr: Instruction, pc: int) -> int:
        handler = self._handlers.get(instr.opcode)
        if handler is None:
            raise UnknownOpcodeError(instr.opcode, pc)
        return handler(instr, pc)
    
    def _val(self, token: str | None, pc: int) -> int:
        if token is None:
            raise ValueError(f"Missing operand at PC={pc}")
        return resolve(token, self._reg, pc)

    def _log(self, msg: str) -> None:
        if self._tracer:
            self._tracer.log(msg)
        else:
            print(msg)

    def _add(self, instr: Instruction, pc: int) -> int:
        a, b = self._val(instr.op1, pc), self._val(instr.op2, pc)
        result = a + b
        self._reg.write_result(result, pc)
        self._log(f"R0: {result} = {a}+{b}")
        return pc + 1
    
    def _sub(self, instr: Instruction, pc: int) -> int:
        a, b = self._val(instr.op1, pc), self._val(instr.op2, pc)
        result = a - b
        self._reg.write_result(result, pc)
        self._log(f"R0: {result} = {a}-{b}")
        return pc + 1

    def _mul(self, instr: Instruction, pc: int) -> int:
        a, b = self._val(instr.op1, pc), self._val(instr.op2, pc)
        result = a * b
        self._reg.write_result(result, pc)
        self._log(f"R0: {result} = {a}*{b}")
        return pc + 1

    def _div(self, instr: Instruction, pc: int) -> int:
        a, b = self._val(instr.op1, pc), self._val(instr.op2, pc)
        if b == 0:
            raise DivisionByZeroError(pc)
        result = a // b
        self._reg.write_result(result, pc)
        self._log(f"R0: {result} = {a}/{b}")
        return pc + 1

    def _mov(self, instr: Instruction, pc: int) -> int:
        dst = get_register_index(instr.op1, pc)  
        val = self._val(instr.op2, pc)
        self._reg.write(dst, val, pc)
        self._log(f"R{dst}: {val}")
        return pc + 1

    def _jump(self, instr: Instruction, pc: int) -> int:
        target = self._val(instr.op1, pc)
        self._log(f"Jump to {target}")
        return target  

    def _compare(self, instr: Instruction, pc: int) -> int:
        a, b = self._val(instr.op1, pc), self._val(instr.op2, pc)
        result = 1 if a < b else 0
        self._reg.write_result(result, pc)
        self._log(f"CMP {a} vs {b} → R0: {result}")
        return pc + 1

    def _branch(self, instr: Instruction, pc: int) -> int:
        if self._reg.read_result() == 1:
            target = self._val(instr.op1, pc)
            self._log(f"Branch taken → {target}")
            return target
        self._log("Branch not taken")
        return pc + 1

    def _halt(self, instr: Instruction, pc: int) -> int:
        self._log("HALT")
        return HALT_SENTINEL
