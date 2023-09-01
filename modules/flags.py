import argparse


def setup(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument(
        "path",
        help="path to game",
        type=str,
    )
    parser.add_argument("-c", "--cycles", help="cycles per frame. default 15", type=int, default=15)
    parser.add_argument(
        "-m", "--mode", help="mode to use. default is schip", type=str, default="schip", choices=["chip8", "schip", "xochip"]
    )
    parser.add_argument("--debug", help="start step by step debugger", required=False, action="store_true")
    return parser
