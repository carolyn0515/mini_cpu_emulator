# 문자열 명령어 -> Instruction 객체
# IR -> split() _ tokenize -> ISA validator -> Instruction 객체 return

from core.instruction import Instruction
from core.exceptions import InvalidInstructionError
from isa.validator import validate_tokens

def decode(raw: str, line_no: int = -1) -> Instruction:
    if '#' in raw:
        raw = raw[:raw.index('#')]
    tokens = raw.strip().split()

    if not tokens:
        raise InvalidInstructionError("empty line", raw=raw, pc=line_no)
    
    opcode = tokens[0]
    op1 = tokens[1] if len(tokens) > 1 else None
    op2 = tokens[2] if len(tokens) > 2 else None

    validate_tokens(opcode, op1, op2, pc=line_no)

    return Instruction(
        opcode = opcode, 
        op1 = op1,
        op2 = op2, 
        raw = raw.strip(),
        line_no = line_no,
    )