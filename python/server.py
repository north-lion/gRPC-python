# 並列実行するために必要なモジュール
from concurrent import futures

import logging

import grpc
import protos.helloworld_pb2
import protos.helloworld_pb2_grpc

# GreeterServicerクラスを継承
class Greeter(protos.helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        checkField(request)
        return protos.helloworld_pb2.HelloReply(message='Hello')

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protos.helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


'''
[Reference] 
Official: https://protobuf.dev/reference/python/python-generated/
UserGithub(高レベルすぎて解読不可): https://github.com/v1c77/py_grpc_validator/blob/master/grpc_proto_validator/validator.

各項目に対し、単純な存在チェックを行いたかったが、
HasField()はオプションがついているかどうかのチェックしか不可能
-> オプションを付与していない項目で使用すると例外が発生する
'''

def checkField(request):
    fields = ["str_val","optional_str_val"]
    for field in fields:
        try:
            if request.HasField(field):
                logging.debug(field + ' is defined')
        except Exception as e:
            logging.debug(field + ' is not defined')



if __name__ == '__main__':
    # Default: level = logging.WARNING
    logging.basicConfig(level = logging.DEBUG)
    serve()
