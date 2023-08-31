from modules import data


def init(ram: list) -> list:
    # Fonts are loaded into 0x50-0x9F.
    fc = 79
    for font in data.font:
        ram[fc] = font
        fc += 1
    return ram
