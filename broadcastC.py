import socket
import json
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind(("", 37020))

while True:
    bander = True
    currentIndex = -1
    while True:
        data, addr = client.recvfrom(1024)
        isJson = False
        try:
            decodedData = data.decode()
        except:
            decodedData = data
            isJson = False
        try:
            cleanData = json.loads(decodedData)
            isJson = True
        except:
            cleanData = decodedData
        if isJson:
            fileData = {
                "fileName": cleanData['fileName'],
                "fileIndex": cleanData['fileIndex'],
                "chunkIndex": cleanData['chunkIndex'],
                "totalChunks": cleanData['totalChunks'],
                "totalFiles": cleanData["totalFiles"]
            }
        else:
            print('Chunk data: ', cleanData)
            if fileData['chunkIndex'] == fileData['totalChunks'] - 1:
                print("Acabamos---------------------------")
                in_file.close()
                if fileData["fileIndex"] == fileData["totalFiles"] - 1:
                    sys.exit(1)
                break
            
            if bander and fileData["fileIndex"] != currentIndex:
                in_file = open(f"received/{fileData['fileName']}", "wb")
                in_file.write(cleanData)
                bander = False
                currentIndex = fileData["fileIndex"]
            else:
                in_file.write(cleanData)


