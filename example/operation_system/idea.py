"""
0. File system: In this software, you can use commands or click to create,copy,move,rename,delete,see,modify,rsync,compress,uncompress file or folder. 2MB size.

1. Email system: Basically, email system should based on http website system, but why you would trust a strange guy than your friend? Exchange information between friends first. In this system, you can send a pure text message to other people, and other people can send text message to you to contact you. It is similar to socket network, your friend ID is IP address, your message is bytes stream. If people ask privacy, let them encrypt the message from client to client. 0.5MB size.

2. HTTP webpage system: We use http1.1 protocol. And only support GET and POST request. We do not need https, we do not need to pay for domains, anyone can use our domains for free, but they do not do that because they are our friends. In one line router link, any computer can work as a DNS(domain to IP server), any computer can have infinity domains. And their computer can work as a http service server without limitations, for example, they can link whatever domain to IP:PORT of their computer, for one computer, it is said to have 60K port, which means they can serve 60k http service. And in that system, the computer can also work as a http client, as a broswer for pure text. Why we do not support browser script, such as javascript? Because we think if a server can't process a heavy computation, they should use a simpler algorithm for their website. 0.5MB client size + 1MB server size.

3. Chat or BBS system: This is a http based website for people to share information, to make friends and chat with friends. It is a pure text based website. 2MB size.

4. File upload and get share http link website: People can share file by using this website. 0.5MB size.

5. Python system: As I know, a system should have a programming language to power the user. A python3.2 statically linked i386 software is only 3MB, but can do many things. 3MB size.

6, Media system: Let people be able to view picture, watch movie, listen music. And take picture, record sound, record video. I have used python to represent image and video and sound, I found the core code is just hundreds of lines, less than 100KB. 1MB viwer size + 0.2MB recorder size.

7. Game system: Let people could play game on computer, 2D and 3D. 10MB size.

All in all, a system that takes only 20.7 MB.
"""
