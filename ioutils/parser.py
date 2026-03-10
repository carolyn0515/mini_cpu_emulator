# 주석/빈줄 정리 등 전처리
def preprocess(lines: list[str]) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for file_lineno, raw in enumerate(lines, start=1):
        line = raw.rstrip('\n\r')

        if '#' in line:
            line = line[:line.index('#')]
        
        line = line.strip()

        if not line:
            continue

        result.append((file_lineno, line))

    return result