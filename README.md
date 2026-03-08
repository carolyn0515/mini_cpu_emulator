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
├── ioutils/
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



| 파일 | 한 줄 요약 |
|------|-----------|
| `core/exceptions.py` | 에뮬레이터 전용 예외 클래스 계층 — `CPUBaseError`를 루트로 모든 예외가 여기서 정의됨 |
| `isa/opcodes.py` | opcode 문자열 상수 (`'+'`, `'M'`, `'J'` 등) 를 이름으로 관리 — 코드 전체에서 리터럴 직접 쓰지 않게 해줌 |
| `isa/spec.py` | 각 opcode가 operand 몇 개 필요한지, op1이 레지스터여야 하는지 등 ISA 규칙을 데이터로 선언 |
| `core/instruction.py` | 파싱 완료된 명령어 하나를 담는 불변 데이터 구조 (`opcode`, `op1`, `op2`, `raw`) |
| `core/operands.py` | operand 토큰(`0xA`, `R3`)을 실제 정수값으로 변환 — Addressing Mode 구현체 |
| `core/decoder.py` | raw 문자열 한 줄을 받아 `Instruction` 객체로 만드는 Decode 단계 |
| `isa/validator.py` | `decode()` 내부에서 호출 — 토큰이 ISA spec을 위반하는지 검사하고 위반 시 예외 raise |
| `core/registers.py` | R0~R9 레지스터 파일 — `read()` / `write()` / `snapshot()` 제공 |
| `core/memory.py` | `Instruction` 리스트를 보관하는 Instruction Memory — `fetch(pc)`로 접근 |
| `core/state.py` | 한 사이클 후의 PC + 레지스터 전체를 찍은 불변 스냅샷 — tracer가 기록에 씀 |
| `core/executor.py` | opcode별 핸들러 딕셔너리 — 실제 연산 수행하고 `next_pc` 반환 |
| `core/cpu.py` | Fetch → Decode(완료) → Execute → PC update 루프를 돌리는 CPU 본체 |
| `ioutils/loader.py` | 파일 열기 → parser 전처리 → decoder 파싱 → memory 적재 순서 총괄 |
| `ioutils/parser.py` | 파일에서 읽은 raw 줄에서 빈 줄·주석 제거해서 파싱 가능한 줄만 추려냄 |
| `ioutils/tracer.py` | 실행 로그 콘솔 출력 + `CPUState` 히스토리 기록 + trace 파일 저장 |
| `main.py` | CLI 인자 파싱 → Tracer·CPU 생성 → load → run 순서로 묶는 진입점 |