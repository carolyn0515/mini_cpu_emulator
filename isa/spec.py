# ISA 명세 / operand 개수 / 규칙

# Instruction Set Architecture Specification

# - 필요한 operand 최소 개수 
# - op1이 반드시 register이어야 하는지 여부 _ M 
# - op2를 무시하는지 여부


from isa.opcodes import (
    ADD, SUB, MUL, DIV, MOV,
    JUMP, COMPARE, BRANCH, HALT,
)

from dataclasses import dataclass

@dataclass(frozen = True)
class InstrSpec:
    opcode: str
    min_operands: int
    op1_must_be_reg: bool = False
    ignores_op2: bool = False
    description: str = ""

ISA_SPEC: dict[str, InstrSpec] = {
    ADD: InstrSpec(ADD, min_operands=2,
                   description="R0 <- val(op1) + val(op2)"),
    SUB: InstrSpec(SUB, min_operands=2,
                   description="R0 <- val(op1) - val(op2)"),
    MUL: InstrSpec(MUL, min_operands=2,
                   description="R0 <- val(op1) * val(op2)"),
    DIV: InstrSpec(DIV, min_operands=2,
                   description="R0 <- val(op1) / val(op2), op2!=0"),
    MOV: InstrSpec(MOV, min_operands=2, op1_must_be_reg=True,
                   description="reg[dst] ← val(op2)"),

    JUMP:    InstrSpec(JUMP,    min_operands=1, ignores_op2=True,
                       description="PC ← val(op1)"),
    COMPARE: InstrSpec(COMPARE, min_operands=2,
                       description="R0 ← 1 if op1 < op2 else 0"),
    BRANCH:  InstrSpec(BRANCH,  min_operands=1, ignores_op2=True,
                       description="if R0==1: PC ← val(op1)"),
    HALT:    InstrSpec(HALT,    min_operands=0, ignores_op2=True,
                       description="Halt execution"),}