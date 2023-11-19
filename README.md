# BTL1_ComputerNetwork
- Dưới đây là các todolist phát sinh trong quá trình làm bài, mọi người cùng nhau giải quyết từng cái nhé <3

- Nếu có vấn đề gì trong quá trình hoàn thành assignment, mọi người hãy note lại ở dưới để dễ theo dõi và xử lí nha.

- Để chạy code chỉ cần quan tâm 2 file: client_real và server_real. Tất cả các file khác là các file phụ trợ trong quá trình làm bài và không cần include trong report lúc nộp bài


# Problems
- Hiện tại chỉ transfer được file .txt, cần phải nghĩ ra cách để transfer các file tầm trung như .jpg, hoặc các file video
  
# P2P File-Sharing Application User Manual

## Overview
This manual provides instructions on how to use the P2P file-sharing application, which consists of a server and a client component. The server manages connections and the discovery of files, while the client is used to publish, discover, and fetch files.

## Getting Started
1. Start the server by running the `server_hao.py` script in a terminal or command prompt.
2. Open another terminal and start the client by running the `client_git.py` script.
3. Once both the server and the client are running, you can use the client command-line interface (CLI) to perform file-sharing operations.

## Client Commands
Here is a list of commands that you can use within the client CLI:

### Exit
- **Command**: `exit`
- **Syntax**: `exit`
- **Description**: Closes the client application.
- **Example**:
  
(client) exit

Exiting client...

### Publish
- **Command**: `publish`
- **Syntax**: `publish <lname> <fname>`
- **Description**: Inform the server of a new file that you want to share.
- **Parameters**:
- `<lname>`: The local path where the file is stored on your system.
- `<fname>`: The name you want to give the file in the network.
- **Example**:

(client) publish D:/shared myphoto.jpg

Enter the path of the file: D:/shared/myphoto.jpg

### Fetch
- **Command**: `fetch`
- **Syntax**: `fetch <filename>`
- **Description**: Requests information from the server about nodes that hold a specific file.
- **Parameters**:
- `<filename>`: The name of the file you want to download.
- **Example**:
  
(client) fetch myphoto.jpg

Enter the directory for your new downloaded file: D:/downloads/

Enter the name of your new downloaded file: newphoto

The file 'newphoto' has been downloaded to your device (path: 'D:/downloads/newphoto.txt').


## Server Commands
The server operates in the background and does not require interactive commands for standard operation. However, for maintenance or administration, the following command is available in the server CLI:

### Exit
- **Command**: `exit`
- **Syntax**: `exit`
- **Description**: Shuts down the server and terminates all client connections gracefully.
- **Example**:
  
(server) exit

Shutting down server...


## Notes
- Ensure that the server is running before starting the client.
- Files to be shared should be placed in a directory accessible by the server.
- The client must be connected to the server to publish or fetch files.




