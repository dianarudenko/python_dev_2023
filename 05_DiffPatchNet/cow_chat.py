import asyncio
import shlex
import cowsay

clients = {}
cows = set(cowsay.list_cows())

async def chat(reader, writer):
    me = None
    while True:
        request = await reader.readline()
        request = shlex.split(request.decode())
        if len(request) == 1:
            if request[0] == 'who':
                response = 'Current users of the chat:\n'
                for client in clients:
                    response += client + '\n'
                writer.write((response +'\n').encode())
                await writer.drain()
            elif request[0] == 'cows':
                response = 'Available cownames to register with:\n'
                for cowname in cows:
                    response += cowname + '\n'
                writer.write((response + '\n').encode())
                await writer.drain()
            elif request[0] == 'quit':
                writer.write('Goodbye!\n'.encode())
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                return
            else:
                writer.write('Bad request\n'.encode())
                await writer.drain()
        elif len(request) == 2 and request[0] == 'login':
            cowname = request[1]
            if cowname in cows:
                clients[cowname] = asyncio.Queue()
                me = cowname
                cows.discard(cowname)
                writer.write('You have successfully logged in, you can start chatting now!\n'.encode())
                await writer.drain()
                break
            else:
                writer.write('Bad cowname\n'.encode())
                await writer.drain()
        else:
            writer.write('Bad request (maybe try to log in first)\n'.encode())
            await writer.drain()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                request = shlex.split(q.result().decode())
                length = len(request)
                if length == 1:
                    if request[0] == 'who':
                        response = 'Current users of the chat:\n'
                        for client in clients:
                            response += client + '\n'
                        writer.write((response +'\n').encode())
                        await writer.drain()
                    elif request[0] == 'cows':
                        response = 'Available cownames to register with:\n'
                        for cowname in cows:
                            response += cowname + '\n'
                        writer.write((response + '\n').encode())
                        await writer.drain()
                    elif request[0] == 'quit':
                        send.cancel()
                        receive.cancel()
                        writer.write('Goodbye!\n'.encode())
                        await writer.drain()
                        del clients[me]
                        cows.add(me)
                        writer.close()
                        await writer.wait_closed()
                        return
                    else:
                        writer.write('Bad request\n'.encode())
                        await writer.drain()
                elif length == 2 and request[0] == 'yield':
                    for out in clients.values():
                        if out is not clients[me]:
                            await out.put(
                                f'{me}:\n{cowsay.cowsay(request[1], cow=me)}\n'
                            )
                elif length == 3 and request[0] == 'say':
                    await clients[request[1]].put(
                        f'{me}:\n{cowsay.cowsay(request[2], cow=me)}\n'
                    )
                else:
                    writer.write('Bad request\n'.encode())
                    await writer.drain()
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())