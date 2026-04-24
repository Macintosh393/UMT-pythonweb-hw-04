import asyncio
import aioshutil
import argparse
from aiopath import AsyncPath
import logging

logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")


async def read_folder(src_p: AsyncPath, dst_p: AsyncPath, base_src: AsyncPath):
    tasks = []
    try:
        async for path in src_p.iterdir():
            if await path.is_file():
                ext_name = "".join(path.suffixes)[1:] if path.suffix else "no-extension"
                tasks.append(
                    copy_file(
                        path,
                        dst_p
                        / path.relative_to(base_src).parent
                        / ext_name
                        / path.name,
                    )
                )
            elif await path.is_dir():
                tasks.append(read_folder(path, dst_p, base_src))
    except OSError as e:
        logging.error(f"Failed to read directory {src_p}: {e}")

    if not tasks:
        return

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, Exception):
            logging.error(f"Task failed with error: {result}")


async def copy_file(file_p: AsyncPath, dst_p: AsyncPath):
    try:
        await dst_p.parent.mkdir(parents=True, exist_ok=True)
        await aioshutil.copy2(str(file_p), str(dst_p))
    except OSError as e:
        logging.error(f"Failed to copy {file_p} to {dst_p}: {e}")
        raise


async def main():
    parser = argparse.ArgumentParser(
        description="A program that allows to recursively sort directories",
        epilog="Usage: python main.py <source> <output>",
    )

    parser.add_argument("source", help="Directory to be sorted")

    parser.add_argument(
        "output", help="Output directory where sorted files will be stored"
    )

    try:
        args = parser.parse_args()
    except SystemExit:
        return

    try:
        src_p = AsyncPath(args.source)
        if not await src_p.exists():
            raise FileNotFoundError(f"Source directory '{args.source}' does not exist")

        if not await src_p.is_dir():
            raise NotADirectoryError(f"Source path '{args.source}' is not a directory")

        dst_p = AsyncPath(args.output)
        await read_folder(src_p, dst_p, base_src=src_p)

        print("All entries were successfully sorted")
    except (FileNotFoundError, NotADirectoryError) as e:
        logging.error(f"Configuration error: {e}")
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {type(e).__name__}: {e}")
    finally:
        print("Execution finished")


if __name__ == "__main__":
    asyncio.run(main())
