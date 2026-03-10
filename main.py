import sys
from core.cpu import CPU
from core.exceptions import ProgramLoadError, CPUBaseError
from ioutils.loader import load
from ioutils.tracer import Tracer 
import config

def main() -> None:
# 입력 파일
    filename = sys.argv[1] if len(sys.argv) > 1 else config.DEFAULT_PROGRAM

# tracer
    tracer = Tracer(
        verbose = config.VERBOSE,
        trace_file = config.TRACE_FILE,
    )

# cpu 
    cpu = CPU(tracer=tracer)

# program load
    try: 
        load(filename, cpu.memory)
    except ProgramLoadError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    
# 실행
    try:
        cpu.run()
    except CPUBaseError as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        tracer.close()

if __name__ == "__main__":
    main()