Initial CLI call:
python3 -m grpc_tools.protoc -I youtubetutorial --python_out=. --grpc_python_out=. youtubetutorial/greet.proto
python3 -m grpc_tools.protoc -I CS262-Design-1 --python_out=. --grpc_python_out=. CS262-Design-1/new-chat.proto
python3 -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/greet.proto

greet_pb2.py has autogenerated code at the top and the function definitions at the bottom
greet_pb2_grpc.py is all autogenerated code