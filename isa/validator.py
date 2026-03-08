# instruction validation
from isa.spec import ISA_SPEC
from isa.opcodes import ALL_OPCODES
from core.exceptions import (
    UnknownOpcodeError,
    InvalidInstructionError,
    InvalidOperandError,
)

def _is_immediate(token: str) -> bool:
    return token.startswith('0x') or token.startswith('0X')

def _is_register(token: str) -> bool:
    return token.upper().startswith('R') and token[1:].isdigit()

def validate_tokens(opcode: str, op1: str | None, op2: str | None,
                    pc: int = -1) -> None:
    
    # opcode 존재 여부 
    if opcode not in ALL_OPCODES:
        raise UnknownOpcodeError(opcode, pc)
    
    spec = ISA_SPEC[opcode]
    operands = [o for o in (op1, op2) if o is not None]

    # operand 개수 검사
    if len(operands) < spec.min_operands:
        raise InvalidInstructionError(
            reason=f"needs at least {spec.min_operands} operand(s), got {len(operands)}",
            raw=f"{opcode} {op1} {op2}",
            pc=pc,
        )
    
    # op1 반드시 register여야 하는 경우 
    if spec.op1_must_be_reg and op1 is not None:
        if not _is_register(op1):
            raise InvalidInstructionError(
                reason=f"op1 must be a register (e.g. R2), got '{op1}'",
                raw=f"{opcode} {op1} {op2}",
                pc=pc,
            )
    
    # operand 형식 검사 
    for token in operands:
        if not (_is_immediate(token) or _is_register(token)):
            raise InvalidOperandError(token, pc)
        