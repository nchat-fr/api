import socketio
import json

sio_server = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=[
        "http://localhost",
        "http://194.164.48.49",
        "http://85.215.133.119",
    ],
)

sio_app = socketio.ASGIApp(socketio_server=sio_server, socketio_path="/ws/socket.io")

clients = {}
identities = {}


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

    identities[sid] = identity
    await sio_server.emit("count", len(clients))


@sio_server.on("logout")
async def client_logout(sid, identity):
    if identity["username"] in clients:
        del clients[identity["username"]]
    await sio_server.emit("count", len(clients))


@sio_server.on("message")
async def message_received(sid, message):
    await sio_server.emit(
        "message",
        {"identity": identities[sid], "message": message.replace("\n", "<br />")},
    )


@sio_server.event
async def disconnect(sid):
    username = getUsernameForSid(sid)
    if username is not None:
        clients[username].remove(sid)
        if len(clients[username]) == 0:
            del clients[username]
    await sio_server.emit("count", len(clients))
