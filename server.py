import socket
import time
import json

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.settimeout(0.2)

def get_file_chunks(file_name, chunk_size):
    batch_contents = []
    with open(file_name, "rb") as in_file:
        while True:
            chunk = in_file.read(chunk_size)
            batch_contents.append(chunk)
            if chunk == b"":
                break  # end of file
    return batch_contents

fileNames = input("Ingrese el nombre de los archivos separados por espacio: ")
filesCollection = fileNames.split()

for i in range(len(filesCollection)):
    fileName = f'images/{filesCollection[i]}'
    fileChunks = get_file_chunks(fileName, 200)
    for index, chunk in enumerate(fileChunks):
        fileData = {
            "fileName": filesCollection[i],
            "fileIndex": i,
            "chunkIndex": index,
            "totalChunks": len(fileChunks),
        }
        encodedChunkData = bytes(json.dumps(fileData), 'utf-8')
        rawChunk = chunk
        server.sendto(encodedChunkData, ('<broadcast>', 37020))
        server.sendto(rawChunk, ('<broadcast>', 37020))
        print("message sent!")
        time.sleep(1)
    # server.sendto(b'Fin del archivo', ('<broadcast>', 37020))

