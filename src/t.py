import sys
import asyncio

print(sys.stdin.encoding)
print(sys.stdout.encoding)

def __async_std_input():
    return (asyncio.get_event_loop()
            .run_in_executor(None, sys.stdin.readline))


def __async_std_output(output_s: str):
    return (asyncio.get_event_loop()
            .run_in_executor(None, lambda s=output_s: sys.stdout.write(s)))


async def main():
    while True:
        inp = await __async_std_input()
        out = f"{inp}\n"
        await __async_std_output(out)


asyncio.run(main())
