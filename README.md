# jac8

Just another Chip-8 Interpreter written in Python.

## Warning

This project is in active development. It is currently failing several [Corax+](https://github.com/Timendus/chip8-test-suite) tests (`8xyE` and `Registers`)

## Features

- Rudimentary Chip-8 emulation. Can run the IBM logo and most tests although some fail.
- Rudimentary step by step debugger that allows you to dump the memory, registers, and stack. Shows the current `pc`, `i`, `instruction`, etc.
- Keypad input, it marks a key as being pressed until it is released. The keypad bindings are as follows:

```
  1 2 3 C            1 2 3 4
  4 5 6 D            Q W E R
  7 8 9 E            A S D F
  A 0 B F            Z X C V

Chip-8 Keypad    QWERTY equivilant
```

## Usage

Install the required modules with `pip3 install -r requirements.txt`

You can run a game with `python3 main.py path/to/file.ch8`.

Run it with the `--debug` flag to enter step by step debugging.

Debugging example:

```
$ python3 main.py 3-corax+.ch8 --debug
pygame 2.3.0 (SDL 2.24.2, Python 3.11.4)
Hello from the pygame community. https://www.pygame.org/contribute.html
Debugger Active
- Press enter to execute instruction
- Enter 'ram' to dump memory
- Enter 'registers' to view registers
- Enter 'stack' to view stack
- Enter 'exit' to quit
[*] i: 0x0, pc: 0x202, instruction: 1208, x: 2, y: 0, nnn: 520, nn: 8, timer: 0, stimer: 0

jac8$ registers
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[*] i: 0x0, pc: 0x202, instruction: 1208, x: 2, y: 0, nnn: 520, nn: 8, timer: 0, stimer: 0

jac8$
```

## References

- https://tobiasvl.github.io/blog/write-a-chip-8-emulator
- https://github.com/IslayLaphroaig/CHIP-8
