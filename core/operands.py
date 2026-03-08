# immediate/register operand 해석

# Addressing Mode 구현
# - Immediate Addressing: 0x{hex} -> int
#       (Immediate Operand)
# - Register Addressing: R{n} -> registers[n]
#       (Register Direct Addressing)

from __future__ import annotations
from typing import TYPE_CHECKING

from core.exceptions import InvalidOperandError, RegisterOutOfRangeError

if TYPE_CHECKING:
    from core.registers import RegisterFile

# [operand evaluation]
# operand -> 실제 값

def resolve(token: str, reg_file: "RegisterFile", pc: int = -1) -> int:
    # token: operand str
    # reg_file: 현재 register file
    # pc: 현재 pc _ for error message
    
    # InvalidOperandError: prefix != 0x OR R
    if token.startswith('0x') or token.startswith('0X'):
        try:
            return int(token, 16)
        except ValueError:
            raise InvalidOperandError(token, pc)
        
    # RegisterOutOfRangeError: register out of range
    if token.upper().startswith('R') and len(token) > 1:
        try:
            idx = int(token[1:])
        except ValueError:
            raise InvalidOperandError(token, pc)
        return reg_file.read(idx, pc)

    raise InvalidOperandError(token, pc)

# [register 형식 아닌 operand]
# operand -> register num

def get_register_index(token: str, pc: int=-1) -> int:
    # InvalidOperandError: R prefix 없음
    if not (token.upper().startswith('R') and len(token) > 1):
        raise InvalidOperandError(token, pc)
    try:
        idx = int(token[1:])
    except ValueError:
        raise InvalidOperandError(token, pc)
    
    if not (0 <= idx <= 9):
        raise RegisterOutOfRangeError(idx, pc)
    return idx
