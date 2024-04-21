<center><font size=6><b>SAL Problem Set Task 1</b></font></center>

## I. Design and Implementation of Communication Protocol

The protocol adopted this time is the HTTP protocol. The layers of the TCP/IP protocol stack from bottom to top are: 
1. Network Interface Layer
2. Internet Layer
3. Transport Layer
4. Application Layer

HTTP protocol is included in the application layer of TCP/IP.

The main reasons for choosing HTTP as the protocol are as follows:

1. Simple and flexible, HTTP uses a simple text format, which is easy to understand and implement.
2. The HTTP protocol is stateless, allowing servers to handle many requests and easily maintain independence between them.
3. Its compatibility and standardisation allow it to operate on various platforms and systems and seamlessly integrate with other technologies and protocols.
4. It supports multiple data formats, and HTTP supports transmitting various data formats.
5. Connectionless HTTP is a connectionless protocol; each request and response are independent.
6. It supports security, and although HTTP itself is not a security protocol, it can ensure data transmission security and privacy when used in conjunction with other security protocols.

## II. Description of System Architecture

**Both server and client code are written in Python**

> sensor/
> ├── service.Dockerfile 
> ├── client.Dockerfile 
> ├── client.py
> ├── matrix.html 
> └── service.py 

Project structure file description:

1. client.Dockerfile - Build the client-side docker image
2. service.Dockerfile - Build the server-side docker image
3. service.py - Server side
4. client.py - Simulate client
5. matrix.html - Display sensor occupancy data

​The server side uses the Flask open-source framework, which is a web framework that implements communication of web applications over HTTP protocol. Choosing this framework for the server side because Flask is a lightweight framework with a relatively small codebase that is easy to learn and use. Developers can flexibly customise it to meet their own needs. Another important reason is that it has a Jinja2 template engine, which allows developers to build pages with rich interactivity easily, and through these pages, we can more intuitively feel the occupancy status of server-side sensor data.

​The client uses the requests library, a popular library for sending HTTP requests. It is simple and easy to use; requests offer a concise and intuitive API, making sending HTTP requests very straightforward. In the sensor client, its post method sends data packets to the server, and the get method is for receiving sensor data packet occupancy data from the server.

## III. GitHub Code Repository

The purpose of storing project code in a GitHub remote repository is for code preservation.

GitHub repository access URL: https://github.com/DKsoup/Problem_SET
Docker Hub URL: https://hub.docker.com/r/zongyueliu/problem_set_task_1_client


## III. Instructions for Starting Client and Server Containers

​Since the server serves multiple clients, the server should always be online, while the client can disconnect after sending/receiving data without affecting the server. Thus, I containerised the server and created a docker image to start the service. I use a local trigger for the sensor client to simulate sending and receiving data packets.

Server build steps:

​1. Build the image

​    `docker build -f service.Dockerfile -t sensor:1.0.0 .`

​2. Run the server container to start the service

​    `docker run -itd -p 8000:8000 --name sensor_service sensor:1.0.0`

Sensor client:

​1. Build the image

​   `docker build -f client.Dockerfile -t client:1.0.0 . `

​2. The client sends and receives data

If the server and client are not on the same local network, modify the 12th line of the client's code, i.e., replace the right of "host=" with the current content.

host = 'http://127.0.0.1:8000/' If your server IP address is 192.168.65.1, replace it with: host = 'http://192.168.65.1:8000/' accordingly.

1. Send data packets to the server
   Example: 
```shell
    docker run client:1.0.0 python client.py 1 send '{[1, 2], 0}'  # Client 1 sends data packets
```
   If it's Client 2, change 1 to 2 accordingly: docker run client:1.0.0 python client.py 2 send '{[3, 2], 1}'

2. Receive data packets
   Example: 
```shell
    docker run client:1.0.0
    python client.py 1 receive    # Client 1 receives data packets
 ```
 If it's Client 2, change 1 to 2 accordingly: 
```shell
    docker run client:1.0.0 python client.py 2 receive
```
