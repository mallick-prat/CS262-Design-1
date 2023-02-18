from concurrent import futures

import grpc
import greet_pb2
import greet_pb2_grpc

class GreeterServicer(greet_pb2_grpc.GreeterServicer):

    def Chatter(self, request_iterator, context):
        for request in request_iterator:
            print("If the prompt to type a message disappears, press any letter key and then press enter.")
            print(request)

            hello_reply = greet_pb2.Reply()
            hello_reply.message = input("Please type reply message: ")

            yield hello_reply
            

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()