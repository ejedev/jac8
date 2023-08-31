# jac8

Just another Chip-8 Interpreter written in Python.

## Warning

This project is in active development. It is currently failing several [Corax+](https://github.com/Timendus/chip8-test-suite) tests (`8xyE`, `Fx65`, `Fx55`, `Fx33`, `Fx1E`, and `Registers`)

## Features

- Rudimentary Chip-8 emulation. Can run the IBM logo and most tests although some fail.
- Rudimentary step by step debugger that allows you to dump the memory, registers, and stack. Shows the current `pc`, `i`, `instruction`, etc.

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
