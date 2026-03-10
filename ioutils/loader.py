# input.txt -> instruction memory 적재

import sys
from core.instruction import Instruction
from core.memory import InstructionMemory
from core.decoder import decode
from core.exceptions import ProgramLoadError, CPUBaseError
from ioutils.parser import preprocess

def load(filename: str, memory: InstructionMemory) -> int:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            raw_lines = f.readlines()
    except OSError as e:
        raise ProgramLoadError(filename, str(e))
    
    cleaned = preprocess(raw_lines)
    
    instructions: list[Instruction] = []
    for mem_idx, (file_lineno, line) in enumerate(cleaned):
        try:
            instr = decode(line, line_no=mem_idx)
            instructions.append(instr)
        except CPUBaseError as e:
            print(f"[WARN] line {file_lineno}: {e}", file=sys.stderr)
    
    memory.load(instructions)

    print(f"[LOAD] '{filename}' -> {memory.size} instruction(s) loaded\n")
    return memory.size