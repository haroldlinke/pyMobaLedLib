This is just a basic chat client/server app. It uses the Queue module so the server thread can post messages to the main GUI event loop. One notable feature of this sample is that messages can be broadcast to more than one machine, so a group of people all using the chat sample can carry on a type of conference.

This is just a sample though. I'm hoping that it will inspire other people to do a real chat client using the Jabber protocol or perhaps a simple IRC client.

Enter the Nick Name (e.g. Kevin) that you would like to appear on the machines you're sending to into the "Nick Name:" field.

Enter the IP addresses you want to send your messages to separated by commas in the "Send to IP addresses:" field. By default, the chat sample is set to send messages to 127.0.0.1 which is your local machine, so you can test the sample by sending messages to yourself.

Enter the message you want to send in the bottom field and then click the Send button.

Each message you send and receive from other people running the chat sample will be displayed in the top field.

For example, after changing the "Nick Name:" field to "Kevin", typing "Hello chat" in the bottom field and clicking "Send" the top field might show:

Kevin (10.0.0.2): Hello chat
Kevin (10.0.0.2): Hello chat


I made up the IP address above. Your machine's IP address will automatically be sent by the chat client as a way of helping identify where each message comes from. When the chat sample starts up it tries to determine your IP address and puts it in the "Your IP Address:" field.

If you are using Network Address Translation (NAT) at home, it is quite likely that the IP address that other users need to send to is different. The IP address you enter for "Your IP Address:" will need to be the address of your router or modem assigned by your ISP.

If your machine is behind a firewall, the chat sample will not be able to communicate unless port 50007 is open for both sending and receiving.
