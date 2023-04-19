import os
import json
import glob
import logging

import grpc
import check_type_spec_pb2
import check_type_spec_pb2_grpc

from google.protobuf import json_format


def run():
    print("Will try to check-type-spec request ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = check_type_spec_pb2_grpc.CheckTypeSpecStub(channel)

        _json_load_and_request(stub)


def _json_load_and_request(stub):
    default_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "json")
    file_paths = glob.glob(default_folder_path + "/**/" + "*", recursive=True)
    for fileName in file_paths:
        with open(fileName) as json_file:
            req_dict = json.load(json_file)

        request = json_format.ParseDict(req_dict, check_type_spec_pb2.CheckRequest())
        metadata = [('x-test-id', os.path.basename(fileName))]
        response = stub.UploadCheckResult(request, metadata=metadata)
        logging.info("response: " + response.message)



if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    run()