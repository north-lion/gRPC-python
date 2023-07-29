import logging

import grpc
import protos.helloworld_pb2
import protos.helloworld_pb2_grpc

def run():
    print("Will try to greet world ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = protos.helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(protos.helloworld_pb2.HelloRequest(str_val='hoge'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()