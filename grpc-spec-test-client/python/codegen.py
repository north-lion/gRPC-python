import glob
import os

from grpc_tools import protoc

python_dir = os.path.dirname(os.path.abspath(__file__))
protos_dir = os.path.join(os.path.dirname(python_dir), 'protos')
_proto_dir = os.path.join(os.path.dirname(protoc.__file__), '_proto') # grpc_toolsのprotoをインポートするための設定
proto_list = glob.glob(
    os.path.join(protos_dir, '**', '*.proto'), recursive=True)


for proto_file in proto_list:
    protoc.main((
        '',
        ''.join(['-I', protos_dir]),
        ''.join(['-I', _proto_dir]),
        ''.join(['--python_out=', python_dir]),
        ''.join(['--grpc_python_out=', python_dir]),
        proto_file
    ))