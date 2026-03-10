# CPU state snapshot / dump 형식
from dataclasses import dataclass, field
from core.instruction import Instruction

@dataclass(frozen=True)
class CPUState: 
    pc: int
    registers: tuple
    instruction: Instruction
    cycle: int = 0

    # snapshot 받아 CPUState 생성
    @classmethod
    def capture(cls, pc: int, reg_snapshot: list[int],
                instr: Instruction, cycle: int) -> "CPUState":
        return cls(
            pc=pc,
            registers=tuple(reg_snapshot),
            instruction=instr,
            cycle=cycle,
        )
    # 레지스터 상태를 문자열로 포맷
    def format_registers(self, only_nonzero: bool = True) -> str:
        parts = []
        for i, v in enumerate(self.registers):
            if only_nonzero and v == 0:
                continue
            parts.append(f"R{i}={v}")
        return f"[{', '.join(parts)}]" if parts else "[all zero]"
    
    def __str__(self) -> str:
        return (
            f"cycle={self.cycle:>4}  "
            f"PC={self.pc:<4}  "
            f"instr='{self.instruction}'. "
            f"regs={self.format_registers()}"
        )