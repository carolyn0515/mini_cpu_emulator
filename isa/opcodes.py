# opcode 상수

# [Arithmetic]
ADD = '+'
SUB = '-'
MUL = '*'
DIV = '/'

# [Data Transfer]
MOV = 'M'

# [Control Flow]
JUMP = 'J'
COMPARE = 'C' # Compare:  R0 ← 1 if op1 < op2 else 0
BRANCH = 'B' # R0 == 1이 분기 조건
HALT = 'H'

ALL_OPCODES:frozenset[str] = frozenset({
    ADD, SUB, MUL, DIV,
    MOV,
    JUMP, COMPARE, BRANCH,
    HALT,
})

WRITES_R0: frozenset[str] = frozenset({ADD, SUB, MUL, DIV, COMPARE})

IGNORES_OP2: frozenset[str] = frozenset({JUMP, BRANCH, HALT})