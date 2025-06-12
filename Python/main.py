import tetris


async def tetris_main():
    print("Starting Tetris...")
    tetris.start_tetris()


async def main():
    tetris_main()
    print("let's a go!")


if __name__ == "__main__":
    main()
