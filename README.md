# P2P File-Sharing Application 
## About the project
This manual provides instructions on how to use the P2P file-sharing application, which consists of a server and a client component. The server manages connections and the discovery of files, while the client is used to publish, discover, and fetch files.
## Table of Contents
- [Installation](#installation)
- [Getting Started](#Getting-Started)
- [Usage](#usage)
- [License](#license)

## Installation
Within the activated environment, use the following command to install Flask:

`$ pip install Flask`

## Getting Started
1. Start the server by running the `server_real.py` script in a terminal or command prompt.
2. Open another terminal and start the client by running the `client_real.py` script.
3. Once both the server and the client are running, you can use the client command-line interface (CLI) to perform file-sharing operations.
### Notes
- Ensure that the server is running before starting the client.
- Files to be shared should be placed in a directory accessible by the server.
- The client must be connected to the server to publish or fetch files.
- To run the code, you only need to focus on two files: client_real and server_real. All other files are auxiliary files used during the assignment and do not need to be included in the report when submitting

## Usage
### Client Commands
Here is a list of commands that you can use within the client CLI:

#### Exit
- **Command**: `exit`
- **Syntax**: `exit`
- **Description**: Closes the client application.
- **Example**:
  
`(client) exit`

Exiting client...

#### Publish
- **Command**: `publish`
- **Syntax**: `publish <lname> <fname>`
- **Description**: Inform the server of a new file named 'fname' that you want to share. After sending the command to the server, you will be asked to provide a filepath. Please enter an authentic path. Afterward, your file will be known as 'fname' file by the server and other clients who want to fetch your file.
- **Parameters**:
- `<lname>`: The local path where the file is stored on your system.
- `<fname>`: The name you want to give the file in the network.
- **Example**:

`(client) publish myphoto.jpg myphoto`

Enter the path of the file: D:/shared/myphoto.jpg

#### Fetch
- **Command**: `fetch`
- **Syntax**: `fetch <filename>`
- **Description**: Requests information from the server about nodes that hold a specific file.
- **Parameters**:
- `<filename>`: The name of the file you want to download. Please don't forget to add the type of your file at the end.
- **Example**:
  
`(client) fetch myphoto`

Enter the directory for your new downloaded file: D:/downloads/

Enter the name of your new downloaded file(Don't forget to add the type of your file): newphoto.jpg

The file 'newphoto.jpg' has been downloaded to your device (path: 'D:/downloads/newphoto.jpg').


### Server Commands
The server operates in the background and does not require interactive commands for standard operation. However, for maintenance or administration, the following command is available in the server CLI:

#### Exit
- **Command**: `exit`
- **Syntax**: `exit`
- **Description**: Shuts down the server and terminates all client connections gracefully.
- **Example**:
  
`(server) exit`

Shutting down server...

## License

This project is licensed with the [MIT license](LICENSE).




