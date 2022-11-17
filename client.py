import socket
import json

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind(("", 37020))
bander = True
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
            "totalChunks": cleanData['totalChunks']
        }
    else:
        print('Chunk data: ', cleanData)
        if fileData['chunkIndex'] == fileData['totalChunks'] - 1:
            in_file.close()
            break
        
        if bander:
            in_file = open(f"received/{fileData['fileName']}", "wb")
            in_file.write(cleanData)
            bander = False
        else:
            in_file.write(cleanData)
        # if cleanData != "Fin del archivo":
        # else:
        #     print("Llegamos al fin del archivo, hay que guardarlo")
