def load(file: str, ram: list) -> list:
    # First 512 bytes are reserved. ROM bytes are loaded in starting at 0x200.
    loc = 512
    with open(file, "rb") as f:
        while byte := f.read(1):
            ram[loc] = int.from_bytes(byte)
            loc += 1
    return ram


def trim(instruction: str) -> str:
    trimmed = instruction.split("0x")[1]
    if len(trimmed) == 1:
        trimmed = "0" + trimmed
    return trimmed
