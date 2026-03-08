# Mini CPU Emulator

A lightweight CPU emulator implemented in Python that simulates the execution of a simple instruction set architecture (ISA).  
The project models core components of a CPU such as registers, instruction memory, decoding, validation, and execution logic, allowing programs written in a simplified assembly-like format to be parsed and executed step-by-step.

The emulator is designed with a modular architecture that separates ISA specification, instruction decoding, execution logic, and I/O processing.  
This structure makes the system easier to extend, test, and analyze while demonstrating the fundamental workflow of a CPU execution pipeline.

---

## Project Structure
```
mini_cpu_emulator/
├── main.py
├── config.py
├── README.md
├── requirements.txt                
│
├── core/
│   ├── __init__.py
│   ├── cpu.py                      # CPU 본체: run loop, fetch/decode/execute orchestration
│   ├── memory.py                   # Instruction memory
│   ├── registers.py                # Register file
│   ├── instruction.py              # Instruction 데이터 구조
│   ├── decoder.py                  # 문자열 명령어 -> Instruction 객체
│   ├── executor.py                 # opcode별 실제 실행 로직
│   ├── operands.py                 # immediate/register operand 해석
│   ├── state.py                    # CPU state snapshot / dump 형식
│   └── exceptions.py               # 사용자 정의 예외
│
├── io/
│   ├── __init__.py
│   ├── loader.py                   # input.txt -> instruction memory 적재
│   ├── parser.py                   # 주석/빈줄 정리 등 전처리
│   └── tracer.py                   # 실행 로그 출력 / trace 저장
│
├── isa/
│   ├── __init__.py
│   ├── opcodes.py                  # opcode 상수
│   ├── spec.py                     # ISA 명세 / operand 개수 / 규칙
│   └── validator.py                # instruction validation
│
├── programs/
│   ├── input_basic.txt
│   ├── input_move.txt
│   ├── input_arithmetic.txt
│   ├── input_jump.txt
│   ├── input_compare_branch.txt
│   ├── input_gcd.txt
│   └── input_invalid_div_zero.txt
│
├── tests/
│   ├── test_decoder.py
│   ├── test_operands.py
│   ├── test_executor.py
│   ├── test_cpu_run.py
│   └── test_gcd.py
│
├── docs/
│   ├── report.md
│   ├── isa_spec.md
│   ├── architecture.md
│   ├── execution_flow.md
│   └── screenshots/
│
└── examples/
    ├── sample_output_basic.txt
    ├── sample_output_gcd.txt
    └── sample_trace.txt
```

---

## Execution Flow

```
exceptions → opcodes → spec → instruction
→ operands → decoder → validator
→ registers → memory → state
→ executor → cpu
→ loader → parser → tracer
→ main
```

### Component Roles

| Component | Layer | Description |
|-----------|------|-------------|
| **exceptions** | Core | Defines custom exception classes used across the emulator (e.g., invalid opcode, illegal register access, divide-by-zero). |
| **opcodes** | ISA | Contains opcode constants that represent supported CPU instructions (ADD, SUB, MOV, JMP, HALT, etc.). |
| **spec** | ISA | Defines the instruction set architecture specification: operand count, operand types, and constraints for each opcode. |
| **instruction** | Core | Data structure representing a decoded instruction, including opcode, operands, and metadata such as line number. |
| **operands** | Core | Provides parsing and interpretation of operand types such as registers, immediates, or memory references. |
| **decoder** | Core | Converts textual assembly instructions into structured `Instruction` objects. |
| **validator** | ISA | Verifies that decoded instructions follow the ISA specification (correct operand count, types, and rules). |
| **registers** | Core | Implements the register file used by the CPU to store temporary computation values. |
| **memory** | Core | Stores instructions and optionally data used during execution. Provides read/write access. |
| **state** | Core | Represents the current CPU state snapshot (PC, registers, flags, execution status). |
| **executor** | Core | Executes instructions by applying opcode logic and modifying registers or memory accordingly. |
| **cpu** | Core | Orchestrates the execution loop (`fetch → decode → execute`) and manages the program counter. |
| **loader** | IO | Loads program files and prepares instruction sequences for the emulator. |
| **parser** | IO | Preprocesses program text by removing comments, trimming whitespace, and organizing instructions. |
| **tracer** | IO | Produces execution logs and traces to visualize instruction-by-instruction behavior. |
| **main** | Entry | Entry point of the application. Initializes components, loads programs, and starts CPU execution. |

---