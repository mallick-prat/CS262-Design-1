from concurrent import futures
import time

import grpc
import greet_pb2
import greet_pb2_grpc

class GreeterServicer(greet_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print("SayHello Request Made:")
        print(request)
        hello_reply = greet_pb2.HelloReply()
        hello_reply.message = f"{request.greeting} {request.name}"

        return hello_reply
    
    def BloodyMary(self, request, context):
        print("A message has arrived for Bloody Mary...\n")
        print(request)

        for i in range(3):
            hello_reply = greet_pb2.HelloReply()
            hello_reply.message = f"{request.greeting} {request.name} {i + 1}"
            yield hello_reply
            time.sleep(3)

    def Attendance(self, request_iterator, context):
        delayed_reply = greet_pb2.DelayedReply()
        for request in request_iterator:
            print("Attendance form is filled out:")
            print(request)
            delayed_reply.request.append(request)

        delayed_reply.message = f"You have sent {len(delayed_reply.request)} messages. Please expect a delayed response."
        return delayed_reply

    def Chatter(self, request_iterator, context):
        for request in request_iterator:
            print("If the prompt to type a message disappears, type your message and then press enter.")
            print(request)

            hello_reply = greet_pb2.Reply()
            hello_reply.message = input("Please type reply message: ")

            yield hello_reply

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("10.250.11.170:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()