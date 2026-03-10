# CPU 본체: run loop, fetch/decode/execute orchestration
import sys
from core.memory import InstructionMemory
from core.registers import RegisterFile
from core.decoder import decode
from core.executor import Executor, HALT_SENTINEL
from core.state import CPUState
from core.exceptions import CPUBaseError, PCOutOfBoundsError
from ioutils.tracer import Tracer

class CPU:
    def __init__(self, tracer: Tracer | None = None) -> None:
        self.memory = InstructionMemory()
        self.registers = RegisterFile()
        self._pc: int = 0
        self._ir = None
        self._tracer = tracer or Tracer()
        self._executor = Executor(self.registers, self._tracer)
        self._cycle = 0

    def run(self) -> None:
        print("[Execution Start]")
        while True:
            try:
                # Fetch
                self._ir = self.memory.fetch(self._pc)
                
                # Execute
                self._cycle += 1
                next_pc = self._executor.execute(self._ir, self._pc)

                # PC update
                if next_pc == HALT_SENTINEL: break
                self._pc = next_pc

                # Snapshot
                state = CPUState.capture(
                    pc = self._pc,
                    reg_snapshot = self.registers.snapshot(),
                    instr = self._ir,
                    cycle = self._cycle,
                )
                self._tracer.record(state)

            # Error
            except PCOutOfBoundsError as e:
                self._tracer.log_error(str(e))
                break 
            except CPUBaseError as e: 
                self._tracer.log_error(f"[Exception] {e}")
                break

        self._tracer.print_final_state(self.registers.snapshot())
        self._tracer.print_summary()
    
    def reset(self) -> None:
        self.registers.reset()
        self._pc = 0
        self._ir = None
        self._cycle = 0