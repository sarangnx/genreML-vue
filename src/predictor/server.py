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