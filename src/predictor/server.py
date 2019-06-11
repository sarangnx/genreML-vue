# import socketio

# # create a Socket.IO server
# sio = socketio.Server()
# app = socketio.WSGIApp(sio)

# @sio.on('my custom event')
# def another_event(sid, data):
#     pass


from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
@sio.on('message')
async def print_message(sid, message):
    print("Socket ID: " , sid)
    print(message)


web.run_app(app,port=8000)