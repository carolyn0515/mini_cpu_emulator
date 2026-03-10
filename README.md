
# Mini CPU Emulator — Execution Trace

이 문서는 **Mini CPU Emulator가 실제로 어떻게 실행되는지**를
**함수 호출 단위까지 추적하여 설명**한다.

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


실행 과정은 크게 두 단계로 나뉜다.

1. **Phase 1 — Load (프로그램 적재)**
2. **Phase 2 — Run (CPU 실행 사이클)**

---

# Phase 1 — Load (프로그램 적재)

프로그램 파일을 읽어서 **Instruction Memory에 적재하는 과정**

```
main()
│
│  argv[1] = "programs/input_gcd.txt"
│
├─► load(filename, memory)                         ioutils/loader.py
│     IN  : filename: str, memory: InstructionMemory
│     OUT : int (적재된 명령어 수)
│
│   ├─► open(filename)
│   │     IN  : "programs/input_gcd.txt"
│   │     OUT : raw_lines: list[str]
│   │           ["M R1 0xC       # line 0\n",
│   │            "M R2 0x8       # line 1\n", ...]
│   │
│   ├─► preprocess(raw_lines)                      ioutils/parser.py
│   │     IN  : list[str]  ← 개행·주석 포함 raw 줄들
│   │     OUT : list[tuple[int, str]]
│   │           [(7, "M R1 0xC"),
│   │            (8, "M R2 0x8"),
│   │            (11, "C R2 0x1"), ...]
│   │           └─ (파일 줄번호, 정제된 명령어 문자열)
│   │
│   └─► for each (file_lineno, line) in cleaned:
│         │
│         ├─► decode(line, line_no=mem_idx)        core/decoder.py
│         │     IN  : raw="M R1 0xC", line_no=0
│         │     OUT : Instruction(
│         │             opcode="M",
│         │             op1="R1",
│         │             op2="0xC",
│         │             raw="M R1 0xC",
│         │             line_no=0
│         │           )
│         │
│         │   ├─► raw.split()
│         │   │     IN  : "M R1 0xC"
│         │   │     OUT : ["M", "R1", "0xC"]
│         │   │
│         │   └─► validate_tokens(opcode, op1, op2, pc) isa/validator.py
│         │         IN  : opcode="M", op1="R1", op2="0xC", pc=0
│         │         OUT : None (정상) / raise Exception (위반)
│         │
│         │       ├─► opcode in ALL_OPCODES         isa/opcodes.py
│         │       │     IN  : "M"
│         │       │     OUT : True
│         │       │
│         │       ├─► ISA_SPEC["M"]                 isa/spec.py
│         │       │     OUT : InstrSpec(
│         │       │             opcode="M",
│         │       │             min_operands=2,
│         │       │             op1_must_be_reg=True
│         │       │           )
│         │       │
│         │       └─► _is_register("R1")
│         │             IN  : "R1"
│         │             OUT : True
│         │
│         └─► instructions.append(Instruction(...))
│
└─► memory.load(instructions)                      core/memory.py
      IN  : list[Instruction]
      OUT : None
      내부: self._instructions = [Instruction, Instruction, ...]
```

이 단계가 끝나면

```
InstructionMemory
```

안에 모든 프로그램 명령어가 적재된다.

---

# Phase 2 — Run (CPU 실행 사이클)

CPU는 **Fetch → Execute → PC Update** 사이클을 반복한다.

예시: `pc = 7`에서 `- R3 R2` 실행

```
cpu.run()                                          core/cpu.py
│
│  while True:
│
├─► memory.fetch(pc=7)                             core/memory.py
│     IN  : pc: int = 7
│     OUT : Instruction(
│             opcode="-",
│             op1="R3",
│             op2="R2",
│             raw="- R3 R2",
│             line_no=7
│           )
│
│   self._ir = Instruction("-", "R3", "R2", ...)
│
├─► executor.execute(instr, pc=7)                  core/executor.py
│     IN  : instr: Instruction, pc: int
│     OUT : next_pc: int = 8
│
│   ├─► self._handlers["-"] → self._sub
│   │
│   └─► _sub(instr, pc=7)
│         IN  : instr: Instruction
│         OUT : int = 8
│
│       ├─► self._val("R3", pc=7)
│       │
│       │   └─► resolve("R3", reg_file, pc=7)      core/operands.py
│       │
│       │       └─► reg_file.read(idx=3, pc=7)     core/registers.py
│       │             OUT : int = 12
│       │
│       ├─► self._val("R2", pc=7)
│       │     OUT : int = 8
│       │
│       ├─► result = 12 - 8 = 4
│       │
│       ├─► reg_file.write_result(4, pc=7)
│       │     내부: self._regs[0] = 4
│       │
│       ├─► tracer.log("R0: 4 = 12-8")             ioutils/tracer.py
│       │
│       └─► return 8
│
├─► self._pc = 8
│
├─► CPUState.capture(                              core/state.py
│     pc=8,
│     reg_snapshot=[4, 12, 8, 4, 0, ...],
│     instr=Instruction("-", "R3", "R2"),
│     cycle=8
│   )
│
└─► tracer.record(state)                           ioutils/tracer.py
```

---

# Branch Example

예: `pc=6`, `"B 0xA R0"`

```
executor.execute(Instruction("B","0xA","R0"), pc=6)
│
└─► _branch(instr, pc=6)
      IN  : instr, pc=6
      OUT : int  ← 10 or 7
│
      ├─► reg_file.read_result()
      │     OUT : int = 1
      │
      ├─► R0 == 1 → branch taken
      │
      ├─► resolve("0xA") → 10
      │
      ├─► tracer.log("Branch taken → 10")
      │
      └─► return 10
```

CPU는 다음 instruction을

```
pc = 10
```

에서 실행한다.

---

# Exception Example

예: `"/ R1 0x0"`

```
executor._div(instr, pc=1)
│
├─► self._val("R1") → 5
├─► self._val("0x0") → 0
├─► b == 0
│
└─► raise DivisionByZeroError(pc=1)
```

예외 처리

```
cpu.run()
  └─ except CPUBaseError

tracer.log_error("[EXCEPTION] Division by zero [PC=1]")
break
print_final_state()
print_summary()
```

---

# 전체 데이터 흐름

CPU 에뮬레이터의 전체 데이터 흐름은 다음과 같다.

```
str (파일)
  → list[str] (raw lines)           parser.preprocess()
  → list[(line_no, str)]            cleaned instructions
  → list[Instruction]               decoder.decode()
  → InstructionMemory               memory.load()
  → Instruction                     memory.fetch(pc)
  → next_pc + side effects          executor.execute()
  → CPUState snapshot               CPUState.capture()
  → list[CPUState] history          tracer.record()
```

---

# CPU Pipeline 관점

이 에뮬레이터는 실제 CPU 구조의 **기본 실행 파이프라인**을 그대로 모사한다.

```
Program Load
      ↓
Fetch
      ↓
Decode
      ↓
Execute
      ↓
Writeback
      ↓
Next PC
```

---