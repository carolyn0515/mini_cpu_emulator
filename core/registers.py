# Register file

from core.exceptions import RegisterOutOfRangeError

NUM_REGISTERS = 10
RESULT_REG = 0 # R0: 연산 결과

class RegisterFile:
    # R0~9
    def __init__(self) -> None: 
        self._regs: list[int] = [0] * NUM_REGISTERS

# [기본]
    # get register value
    def read(self, index: int, pc: int = -1) -> int:
        self._check_range(index, pc)
        return self._regs[index]
    
    # write on register
    def write(self, index: int, value: int, pc: int = -1) -> None:
        self._check_range(index, pc)
        self._regs[index] = value

    def write_result(self, value: int, pc: int = -1) -> None:
        self.write(RESULT_REG, value, pc)

    def read_result(self) -> int:
        return self._regs[RESULT_REG]

# [R0 전용]
    # 연산 결과 R0에 저장
    def write_result(self, value: int, pc: int = -1) -> None:
        self.write(RESULT_REG, value, pc)
    # R0 값 읽음
    def read_result(self) -> int:
        return self._regs[RESULT_REG]
    
# [utility]
    # reset
    def reset(self) -> None:
        self._regs = [0] * NUM_REGISTERS
    
    # copy return 
    def snapshot(self) -> list[int]:
        return list(self._regs)
    
    def _check_range(self, index: int, pc: int) -> None:
        if not (0 <= index < NUM_REGISTERS):
            raise RegisterOutOfRangeError(index, pc)
    
    def __repr__(self) -> str:
        parts = [f"R{i}={v}" for i, v in enumerate(self._regs) if v != 0]
        return f"RegisterFile({'. '.join(parts) or 'all zero'})"

    
