import uvloop
import asyncio
import os
import mimetypes
from request import *
from response import *
from datetime import datetime
from urllib.parse import unquote

SOCKET_BUFFER_SIZE = 1024

class Worker:

    def __init__(self, document_root, socket_connection):
        self.request_parser = RequestParser()
        self.document_root = document_root
        self.socket_connection = socket_connection
        self.loop = uvloop.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.cycle())

    async def cycle(self):
        while True:
            client, _ = await self.loop.sock_accept(self.socket_connection)
            self.loop.create_task(self.handleRequest(client))


    async def handleRequest(self, client):
        request = await self.read(client)
        self.response = Response()
        if not self.request_parser(request):
            response =  self.response.createResponse(400, [('Date', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')),('Server', 'HW1Highload'),('Connection', 'close')])
            await self.write(client, response)
            client.close()
            return

        if self.request_parser.method != 'HEAD' and self.request_parser.method != 'GET':
            response = self.response.createResponse(405,[('Date', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')),('Server', 'HW1Highload'),('Connection', 'close')])
            await self.write(client, response)
            client.close()
            return

        file_path = os.path.abspath(os.path.join(self.document_root, self.request_parser.path))
        file_path = unquote(file_path)


        if self.document_root not in file_path:
            response = self.response.createResponse(403, [('Date', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')),('Server', 'HW1Highload'),('Connection', 'close')])
            await self.write(client, response)
            client.close()
            return


        wrong_slash = (not file_path.endswith('/')) and self.request_parser.path.endswith('/')

        index_added = False

        if os.path.isdir(file_path):
            index_added = True
            file_path = os.path.join(file_path, 'index.html')

        if not os.path.exists(file_path):

            if index_added:
                await self.write(client, self.response.createResponse(403, [('Date', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')),('Server', 'HW1Highload'),('Connection', 'close')]))
            else:
                await self.write(client, self.response.createResponse(404, [('Date', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')),('Server', 'HW1Highload'),('Connection', 'close')]))

        else:
            if wrong_slash and not index_added:
                response = self.response.createResponse(404, [('Date', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')),('Server', 'HW1Highload'),('Connection', 'close')])
                await self.write(client, response)
            else:
                mime_type, _ = mimetypes.guess_type(file_path)
                headers = [('Date', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')),('Server', 'HW1Highload'),('Connection', 'close'), ('Content-Length', str(os.path.getsize(file_path))),('Content-Type', mime_type) ]

                response = self.response.createResponse(200, headers)

                if self.request_parser.method == 'HEAD':
                    await self.write(client, response)
                else:
                    with open(file_path, 'rb') as filepath:
                        await self.write(client, response, filepath)

        client.close()

    async def read(self, client):
        return (await self.loop.sock_recv(client, SOCKET_BUFFER_SIZE)).decode('utf-8')

    async def write(self, client, response, filepath = None):
        await self.loop.sock_sendall(client, str(response).encode('utf-8'))

        if filepath is not None:
            while True:
                line = filepath.read(1024)

                if not line:
                    return

                await self.loop.sock_sendall(client, line)