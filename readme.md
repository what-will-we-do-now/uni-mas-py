## unimas.py

This repository is a port of [what-will-we-do-now/uni-mas](https://github.com/what-will-we-do-now/uni-mas) for Python.

## Usage

The usage of uni-mas.py is relatively simple.

To create a client use the following code

```python
import unimaspy

# you can change the name of the client here
client = unimaspy.Client('client')

# next you need to connect to the router.
client.connect(ip='127.0.0.1', port=42069)
# you can also forgo the ip and port parameters
# to connect to the defaults used in the parameters above

# now we can send a message
message = unimaspy.Message('client', 'recipient', unimaspy.MessageType.USER_MSG, 'Hello')

client.send(message)

# next we can receive a message
response = client.recv()
print(response.getSender() + ": " response.getMessage())

# and now we can close the connection
client.disconnect()
```

for more help you can always check 
```python
help(unimaspy)
```