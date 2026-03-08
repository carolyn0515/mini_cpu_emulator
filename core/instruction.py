# Instruction 데이터 구조

# parsing 결과 담는 instruction data structure
# raw str -> instruction 객체로 change = Decode

from dataclasses import dataclass

@dataclass(frozen=True)
class Insruction:
    opcode: str
    op1: str | None
    op2: str | None
    raw: str
    line_no: int = -1

    def __str__(self) -> str: 
        parts = [self.opcode]
        if self.op1 is not None:
            parts.append(self.op1)
        if self.op2 is not None:
            parts.append(self.op2)
        return " ".join(parts)