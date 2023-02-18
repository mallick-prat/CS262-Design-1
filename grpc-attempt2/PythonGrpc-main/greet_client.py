import greet_pb2_grpc
import greet_pb2
import time
import grpc

def talk_to_server():
    while True:
        print("If the prompt to type a message disappears, type your message and then press enter.")
        message = input("Please enter a message (or press enter to stop chatting):\n")

        if message == "":
            break

        hello_request = greet_pb2.Reply(message = message)
        yield hello_request
        time.sleep(1)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        responses = stub.Chatter(talk_to_server())
        for response in responses:
            print(response)
            talk_to_server()

if __name__ == "__main__":
    run()