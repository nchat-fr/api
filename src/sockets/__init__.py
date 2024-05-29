import socketio

sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=['http://localhost']
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='/ws/socket.io'
)

clients = {}


@sio_server.event
async def connect(sid, environ, auth):
    clients[sid] = auth
    await sio_server.emit('count', len(clients))


@sio_server.event
async def disconnect(sid):
    del clients[sid]
    await sio_server.emit('count', len(clients))
