import sys
import asyncio
import chardet

std_in = open(sys.stdin.fileno(), "r")
std_out = open(sys.stdout.fileno(), "w")


def __async_std_input():
    return (asyncio.get_event_loop()
            .run_in_executor(None, std_in.readline))


async def __async_std_output(output_s: str):
    await asyncio.sleep(2)
    std_out.write(output_s)


async def main():
    while True:
        inp = await __async_std_input()
        out = f"{inp}\n"
        await __async_std_output(out)


asyncio.run(main())
