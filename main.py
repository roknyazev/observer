from observer import *
import logging

scan = scanner('./test', 5)
print(scan())
print(diff(scan(), scan()))
print(diff(None, scan()))
print(diff([], scan()))

print('---------------------------------')

obs = Observer('./test', 4, 1)


@obs.listen
def test(payload):
    print('------', payload)


# obs.observe()
#
# async def test():
#     await asyncio.get_running_loop().create_future(print(123))


asyncio.run(obs.observe_async())
