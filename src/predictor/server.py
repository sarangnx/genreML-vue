import zmq
import json
import predict

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    query = socket.recv()
    
    queryObject = json.loads(query)

    if(queryObject["mode"] == "single"):
        songPath = queryObject["data"]
        # predicted_class, prediction_percentage = predict.singleMode(songPath)

        predicted_class = predict.singleMode(songPath)
        socket.send_string(predicted_class)
        # socket.send_string(songPath)
    else:
        socket.send_string("BATCH")

    # print(json.dumps(query))
    #  Send reply back to client
    # socket.send_string(json.dumps(query))
