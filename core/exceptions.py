# 사용자 정의 예외
# 모든 예외가 CPUBaseError inherit

class CPUBaseError(Exception):
    def __init__(self, message: str, pc: int = -1):
        self.pc = pc
        location = f" [PC={pc}]" if pc >= 0 else ""
        super().__init__(f"{message}{location}")

# [ISA / Decode]

    # undefined opcode
class UnknownOpcodeError(CPUBaseError):
    def __init__(self, opcode: str, pc: int = -1):
        super().__init__(f"Unknown opcode: '{opcode}'", pc)
        self.opcode = opcode

    # 명령어 형식 위반
class InvalidInstructionErorr(CPUBaseError):
    def __init__(self, reason: str, raw: str = "", pc: int = -1):
        super().__init__(f"Invalid instruction ({reason}): '{raw}'", pc)
        self.raw = raw

# [Operand / Addressing]

    # operand prefix가 0x, R 아닐 때
class InvalidOperandError(CPUBaseError):
    def __init__(self, operand: str, pc: int = -1):
        super().__init__(f"Invalid operand format: '{operand}'", pc):
        self.operand = operand

    # register번호 our of range
class RegisterOutOfRangeError(CPUBaseError): 
    def __init__(self, index: int, pc: int = -1):
        super().__init__(f"Register index out of Range: R{index} (valid: R0~R9)", pc)
        self.index = index

# [Execute]

    # 나눗셈 연산에서 제수가 0일 때  
class DivisionByZeroError(CPUBaseError): 
    def __init__(self, pc: int = -1):
        super().__init__("Division by zero", pc)
 
    # PC가 0 ~ mem_size-1 벗어남
class PCOutOfBoundsError(CPUBaseError):
    def __init__(self, pc: int, mem_size: int):
        super().__init__(
            f"PC={pc} is out of bounds (memory size={mem_size})", pc
        )
        self.mem_size = mem_size

# [I/O]

    # input file problem 
class ProgramLoadError(CPUBaseError):
    def __init__(self, filename: str, reason: str):
        super().__init__(f"Cannot load program '{filename}': {reason}")
        self.filename = filename
