# 실행 로그 출력 / trace 저장

from __future__ import annotations
import sys
from core.state import CPUState

class Tracer:
    def __init__(
        self,
        verbose: bool = False, # 매 사이클 후 register 전체 상태 출력
        trace_file: str | None = None, # 파일에도 로그 기록
        silent: bool = False, # 콘솔 출력 완전 억제
    ) -> None:
        self._verbose = verbose
        self._silent = silent
        self._history: list[CPUState] = []
        self._buf: list[str] = []

        self._file_out = None
        if trace_file:
            try:
                self._file_out = open(trace_file, 'w', encoding='utf-8')
            except OSError as e:
                print(f"[WARN] Cannot open trace file: {e}", file=sys.stderr)

# 기본 로그 출력

    def log(self, msg: str) -> None:
        if not self._silent:
            print(msg)
        if self._file_out:
            self._file_out.write(msg + '\n')
    
    def log_error(self, msg: str) -> None:
        print(msg, file=sys.stderr)
        if self._file_out:
            self._file_out.write(f"[ERROR] {msg}\n")
    
# State 기록

    def record(self, state: CPUState) -> None:
        self._history.append(state)
        if self._verbose and not self._silent:
            print(f" {state.format_registers()}")
        if self._file_out:
            self._file_out.write(f" TRACE: {state}\n")

# 최종 출력

    def print_final_state(self, reg_snapshot: list[int]) -> None:
        if self._silent:
             return 
        print("[Final Register State]")
        has_nonzero = False
        for i, v in enumerate(reg_snapshot):
            if v != 0: 
                print(f" R{i} = {v}")
                has_nonzero = True
        if not has_nonzero: print(" all registers are 0")

    def print_summary(self) -> None:
        if not self._silent:
            print(f"[SUMMARY] Total cycles executed: {len(self._history)}")

# history 조회 

    @property
    def history(self) -> list[CPUState]:
        return list(self._history)
    
    def close(self) -> None:
        if self._file_out:
            self._file_out.close()
            self._file_out = None
    
    def __del__(self) -> None:
        self.close()
        