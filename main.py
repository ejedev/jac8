import random
import pygame

import argparse

from modules import data, memory, display, parse, flags

display_normal = [64, 32]


def main():
    parser = argparse.ArgumentParser(
        prog="jac8",
    )
    parser = flags.setup(parser)
    results = parser.parse_args()

    # Input frame.
    ipf = False
    ckey = 0
    timer = 0
    stimer = 0
    # First 512 bytes are reserved. Execution starts at 0x200.
    pc = 512
    i = 0
    stack = [0] * 16
    cells = display.generate(display_normal[0], display_normal[1])
    ram = memory.init([0] * 4096)
    registers = [0] * 16
    ram = parse.load(results.path, ram)

    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode([display_normal[0] * 10, display_normal[1] * 10])
    running = True
    if results.debug:
        print(data.debug)
    while running:
        draw = False
        if timer != 0:
            timer -= 1
        if stimer != 0:
            stimer -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                else:
                    if int(event.key) in data.keypad:
                        ipf = True
                        ckey = int(event.key)
            elif event.type == pygame.KEYUP:
                ipf = False

        screen.fill(pygame.Color(0, 0, 0, 0))
        for c in range(0, results.cycles):
            # Instruction is two bytes. We load both and trim values into a string so we can parse it in a human-readable way.
            instruction = parse.trim(hex(ram[pc])) + parse.trim(hex(ram[pc + 1]))
            pc += 2
            nnn = int(instruction[1:], 16)
            nnstr = instruction[2:]
            nn = int(nnstr, 16)
            nstr = instruction[-1]
            n = int(nstr, 16)
            x = instruction[1:2]
            y = instruction[2:3]
            vx = int(x, 16)
            vy = int(y, 16)

            if results.debug:
                while True:
                    print(
                        f"[*] i: {hex(i)}, pc: {hex(pc)}, instruction: {instruction}, x: {x}, y: {y}, nnn: {nnn}, nn: {nn}, timer: {timer}, stimer: {stimer}"
                    )
                    match input("\njac8$ "):
                        case "":
                            break
                        case "ram":
                            print(ram)
                        case "registers":
                            print(registers)
                        case "stack":
                            print(stack)
                        case "exit":
                            exit()

            match instruction:
                # Clear instruction. We just regenerate a blank cell map rather then set the values back to 0.
                case "00e0":
                    cells = display.generate(display_normal[0], display_normal[1])

                case "00ee":
                    pc = stack.pop()

                case instruction if instruction.startswith("a"):
                    i = nnn

                case instruction if instruction.startswith("b"):
                    if results.mode == "schip":
                        pc = nnn + registers[vx]
                    else:
                        pc = nnn + registers[0]

                case instruction if instruction.startswith("c"):
                    registers[vx] = random.randint(0, nn) & nn

                case instruction if instruction.startswith("d"):
                    # Display wait logic. Don't allow a draw to execute if it isn't the first cycle of a frame.
                    if c != 0 and results.mode == "chip8":
                        pc -= 2
                        break
                    # New variables x1, y1 created as they need to be modified during the draw loop.
                    draw = True
                    x1 = registers[vx] & 63
                    y1 = registers[vy] & 31
                    registers[15] = 0
                    for s in range(0, n):
                        sprite = ram[i + s]
                        for w in range(0, 8):
                            validSpritePixel = (sprite & (1 << 7 - w)) != 0
                            if validSpritePixel and cells[(x1 * 10, y1 * 10)] is False:
                                cells[(x1 * 10, y1 * 10)] = True
                            elif validSpritePixel and cells[(x1 * 10, y1 * 10)] is True:
                                cells[(x1 * 10, y1 * 10)] = False
                                registers[15] = 1
                            # X clipping quirk
                            if results.mode == "xochip":
                                x1 = x1 % 63
                            if x1 >= 63:
                                break
                            x1 += 1
                        # Y clipping quirk
                        if results.mode == "xochip":
                            y1 = y1 % 31
                        if y1 >= 31:
                            break
                        y1 += 1
                        x1 = registers[vx] & 63

                case instruction if instruction.startswith("e"):
                    match nnstr:
                        case "9e":
                            if ipf and data.keypad[ckey] == registers[vx]:
                                pc += 2
                        case "a1":
                            if not ipf or data.keypad[ckey] != registers[vx]:
                                pc += 2

                case instruction if instruction.startswith("f"):
                    match nnstr:
                        case "07":
                            registers[vx] = timer
                        case "15":
                            timer = registers[vx]
                        case "18":
                            # TODO make it beep if stimer > 0
                            stimer = registers[vx]
                        case "1e":
                            i += registers[vx]
                        case "0a":
                            if ipf:
                                registers[vx] = data.keypad[ckey]
                            else:
                                pc -= 2
                        case "29":
                            i = 79 + (registers[vx] * 5)
                        case "33":
                            ram[i] = registers[vx] // 100
                            ram[i + 1] = (registers[vx] // 10) % 10
                            ram[i + 2] = registers[vx] % 10
                        case "55":
                            vpos = 0
                            while vpos <= int(x, 16):
                                ram[i + vpos] = registers[vpos]
                                vpos += 1
                            if results.mode in ["chip8", "xochip"]:
                                i += vpos
                        case "65":
                            vpos = 0
                            while vpos <= int(x, 16):
                                registers[vpos] = ram[i + vpos]
                                vpos += 1
                            if results.mode in ["chip8", "xochip"]:
                                i += vpos

                case instruction if instruction.startswith("1"):
                    pc = nnn

                case instruction if instruction.startswith("2"):
                    stack.append(pc)
                    pc = nnn

                case instruction if instruction.startswith("3"):
                    if registers[vx] == nn:
                        pc += 2

                case instruction if instruction.startswith("4"):
                    if registers[vx] != nn:
                        pc += 2

                case instruction if instruction.startswith("5"):
                    if registers[vx] == registers[vy]:
                        pc += 2

                case instruction if instruction.startswith("6"):
                    registers[vx] = nn

                case instruction if instruction.startswith("7"):
                    registers[vx] += nn
                    registers[vx] %= 256

                case instruction if instruction.startswith("8"):
                    match nstr:
                        case "0":
                            registers[vx] = registers[vy]
                        case "1":
                            registers[vx] = registers[vx] | registers[vy]
                            if results.mode == "chip8":
                                registers[15] = 0
                        case "2":
                            registers[vx] = registers[vx] & registers[vy]
                            if results.mode == "chip8":
                                registers[15] = 0
                        case "3":
                            registers[vx] = registers[vx] ^ registers[vy]
                            if results.mode == "chip8":
                                registers[15] = 0
                        case "4":
                            registers[vx] += registers[vy]
                            if registers[vx] > 255:
                                registers[vx] -= 256
                                registers[15] = 1
                            else:
                                registers[15] = 0
                        case "5":
                            registers[vx] = registers[vx] - registers[vy]
                            if registers[vx] < 0:
                                registers[vx] += 256
                                registers[15] = 0
                            else:
                                registers[15] = 1
                        case "6":
                            if results.mode == "schip":
                                vf = registers[vx] & 1
                                registers[vx] = (registers[vx] >> 1) % 256
                            else:
                                vf = registers[vy] & 1
                                registers[vx] = (registers[vy] >> 1) % 256
                            registers[15] = vf
                        case "7":
                            registers[vx] = registers[vy] - registers[vx]
                            if registers[vx] < 0:
                                registers[vx] += 256
                                registers[15] = 0
                            else:
                                registers[15] = 1
                        case "e":
                            if results.mode == "schip":
                                vf = (registers[vx] >> 7) & 1
                                registers[vx] = (registers[vx] << 1) % 256
                            else:
                                vf = (registers[vy] >> 7) & 1
                                registers[vx] = (registers[vy] << 1) % 256
                            registers[15] = vf

                case instruction if instruction.startswith("9"):
                    if registers[vx] != registers[vy]:
                        pc += 2

                case _:
                    print("Unknown instructions:", instruction)

        if draw:
            for cell in cells:
                if cells[cell] is True:
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(cell[0], cell[1], 10, 10))
            pygame.display.flip()
        # FPS set at 60 for timers.
        clock.tick(60)


if __name__ == "__main__":
    main()
