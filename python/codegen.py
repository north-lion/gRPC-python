from grpc_tools import protoc

protoc.main(
    (
        '',
        '-I.',
        '--python_out=./python',
        '--grpc_python_out=./python',
        './protos/helloworld.proto',
    )
)