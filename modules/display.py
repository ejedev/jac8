def generate(width, height) -> dict:
    display = {}
    for w in range(0, width):
        for h in range(0, height):
            # Scaled 10x for better visibility.
            display[(w * 10, h * 10)] = False
    return display
