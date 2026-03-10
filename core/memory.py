# Instruction memory
from core.instruction import Instruction
from core.exceptions import PCOutOfBoundsError

class InstructionMemory:
    # Von Neumann Instruction Memory
    # loader가 parsing한 instruction 객체 순서대로 저장 
    def __init__(self) -> None:
        self._instructions: list[Instruction] = []
    
    def load(self, instructions: list[Instruction]) -> None:
        self._instructions = list(instructions)
    
    # PC 위치의 명령어 반환
    def fetch(self, pc: int) -> Instruction:
        if not (0<=pc<len(self._instructions)):
            raise PCOutOfBoundsError(pc, len(self._instructions))
        return self._instructions[pc]
    
    @property
    def size(self) -> int:
        return len(self._instructions)
    
    def is_valid_pc(self, pc: int) -> bool:
        return 0 <= pc < len(self._instructions)
    
    def _repr_(self) -> str:
        return f"InstructionMemory(size={self.size})"