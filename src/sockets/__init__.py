import socketio

sio_server = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins=["http://localhost"]
)

sio_app = socketio.ASGIApp(socketio_server=sio_server, socketio_path="/ws/socket.io")

clients = {}


def getUsernameForSid(sid: str):
    for username, sids in clients.items():
        if sid in sids:
            return username
    return None


@sio_server.on("auth")
async def client_auth(sid, identity):
    if identity["username"] in clients:
        clients[identity["username"]].append(sid)
    else:
        clients[identity["username"]] = [sid]
    await sio_server.emit("count", len(clients))


@sio_server.on("logout")
async def client_logout(sid, identity):
    if identity["username"] in clients:
        del clients[identity["username"]]
    await sio_server.emit("count", len(clients))


@sio_server.event
async def disconnect(sid):
    username = getUsernameForSid(sid)
    if username is not None:
        clients[username].remove(sid)
        if len(clients[username]) == 0:
            del clients[username]
    await sio_server.emit("count", len(clients))
