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
        index, percentages = predict.singleMode(songPath)
        
        # Assign Genre Name
        predicted_class = predict.classes[index]
        
        prediction_percentage = {}
        for i in range(len(percentages)):
            prediction_percentage[predict.classes[i]] = percentages[i]

        data = {
            "predicted_class" : predicted_class, 
            "prediction_percentage" : prediction_percentage
        }

        socket.send_string(json.dumps(data))

    else:
        socket.send_string("BATCH")
