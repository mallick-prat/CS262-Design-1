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
        print("GRPC MessageBase -- CS 262\n")
        print("---------")
        print()

        print("Welcome to our GRPC MessageBase!")
        print("To alter the original assignment, we created a bidirectional chat feature as well as unary, server-side, and client-side streaming options.")

        print("1. Unary Demo")
        print("2. Server-Side Demo")
        print("3. Client-Side Demo")
        print("4. Bidirectional Chat")
        rpc_call = input("Please select an option to explore: ")

        if rpc_call == "1":
            hello_request = greet_pb2.HelloRequest(greeting = "Bonjour,", name = "CS262 Student")
            hello_reply = stub.SayHello(hello_request)
            print("SayHello Response Received:")
            print(hello_reply)
        
        elif rpc_call == "2":
            hello_request = greet_pb2.HelloRequest(greeting = "Arise,", name = "Bloody Mary")
            hello_replies = stub.BloodyMary(hello_request)

            for hello_reply in hello_replies:
                print("You have summoned the Bloody Mary...\n")
                print(hello_reply)
        
        elif rpc_call == "3":
            print("Attendance time: please type each person's name to be recorded.\n")
            delayed_reply = stub.Attendance(talk_to_server())

            print("Attendance Received: ")
            print(delayed_reply)
        
        elif rpc_call == "4":
            responses = stub.Chatter(talk_to_server())

            for response in responses:
                print(response)
                talk_to_server()

if __name__ == "__main__":
    run()