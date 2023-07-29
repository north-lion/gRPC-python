import os
import json
import glob
import logging

import grpc
import check_type_spec_pb2
import check_type_spec_pb2_grpc

from google.protobuf import json_format


FILE_ABS_PARH = os.path.abspath(__file__)
FILE_DIR_PATH = os.path.dirname(FILE_ABS_PARH)
OUTPUT_DIR_PATH = os.path.join(os.getcwd(), "_output_json")


def run():
    print("Will try to check-type-spec request ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = check_type_spec_pb2_grpc.CheckTypeSpecStub(channel)

        _json_load_and_request(stub)


def _json_load_and_request(stub):
    # jsonフォルダ内に配置したjsonデータを全て読み込み、RPCメッセージにパースしてRPCメソッド呼び出し
    default_folder_path = os.path.join(FILE_DIR_PATH, "..", "_input_json")
    file_paths = glob.glob(default_folder_path + "/**/" + "*", recursive=True)
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        with open(file_path) as json_file:
            input_dict = json.load(json_file)

        request = json_format.ParseDict(input_dict, check_type_spec_pb2.CheckRequest())
        metadata = [('x-test-id', file_name)]
        response = stub.UploadCheckResult(request, metadata=metadata)

        # 結果をJSONファイルで出力
        os.makedirs(OUTPUT_DIR_PATH, exist_ok=True)
        with open(os.path.join(OUTPUT_DIR_PATH, file_name), 'w') as f:
            json.dump(json.loads(response.message), f, indent=2, ensure_ascii=False)



if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    run()