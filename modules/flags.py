def setup(parser):
    parser.add_argument(
        "path",
        help="path to game",
        type=str,
    )
    parser.add_argument("-c", "--cycles", help="cycles per frame. default 15", type=int, default=15)
    parser.add_argument("--debug", help="start step by step debugger", required=False, action="store_true")
    return parser
