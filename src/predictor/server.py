# import socketio

# # create a Socket.IO server
# sio = socketio.Server()
# app = socketio.WSGIApp(sio)

# @sio.on('my custom event')
# def another_event(sid, data):
#     pass


# from aiohttp import web
# import socketio

# sio = socketio.AsyncServer()
# app = web.Application()
# sio.attach(app)
# @sio.event
# async def message(sid, message):
#     print("Socket ID: " , sid)
#     print(message)


# web.run_app(app,port=8000)

# import eventlet
# import socketio

# sio = socketio.Server()

# @sio.event
# def connect(sid, environ):
#     print('connect ', sid)

# @sio.event
# def my_message(sid, data):
#     print('message ', data)

# @sio.event
# def disconnect(sid):
#     print('disconnect ', sid)

# eventlet.wsgi.server(eventlet.listen(('', 8000)), app)

import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    #  Send reply back to client
    socket.send(b"World")