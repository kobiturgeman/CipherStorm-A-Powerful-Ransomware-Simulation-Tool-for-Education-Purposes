# CipherStorm-A-Powerful-Ransomware-Simulation-Tool-for-Education-Purposes


### WARNING: This project is for educational purposes only and should not be used for malicious purposes.

This project is written in Python and simulates a ransomware attack. A server is implemented using the threading module to manage a limitless number of clients. When the client runs, it selects a random key, passes it through a hash, and encrypts all files with extensions such as .docs, .txt, .mp3, etc. The client then sends the encrypted key and its hostname to the server for identification purposes. The client immediately deletes all information about the key. All communication between the server and client is encrypted using shared keys between them.

### Installation
##### To install the required packages, run the following command in the terminal:

- Copy code
- pip install -r requirements.txt

### Usage
##### To run the server, use the following command:

- Copy code
- python server.py
To run the client, use the following command:

- Copy code
- python client.py
### Contributing
We welcome contributions to this project. If you have any ideas or bug fixes, please submit a pull request.
