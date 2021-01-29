import socket

RECIPIENT_GLOBAL = 'GLOBAL'

MESSAGE_MAX_SIZE = 65536


class MessageType:
    """
    This class contains list of allowed messages types
    """
    USER_MSG = 'USER_MSG'
    ADD_METAAGENT = 'ADD_METAAGENT'
    REMOVE_METAAGENT = 'REMOVE_METAAGENT'
    ERROR = 'ERROR'
    ADD_PORTAL = 'ADD_PORTAL'
    REMOVE_PORTAL = 'REMOVE_PORTAL'
    LOAD_TABLE = 'LOAD_TABLE'
    ADD_ROUTER = 'ADD_ROUTER'
    LOAD_ADDRESSES = 'LOAD_ADDRESSES'
    REQUEST_ROUTER_ADDRESSES = 'REQUEST_ROUTER_ADDRESSES'


class Message:
    """
    This class is used to represent a message object from uni-mas
    """
    def __init__(self, sender: str, recipient: str, type: MessageType, message: str):
        """
        Parameters
        ----------
        sender : str
            The name of the sender
        recipient : str
            The name of the recipient

        """
        self.__sender__ = sender
        self.__recipient__ = recipient
        self.__type__ = type
        self.__message__ = message

    def __str__(self):
        return self.__sender__ + "/" + self.__recipient__ + "/" + self.__type__ + "/" + self.__message__

    def setSender(self, sender: str):
        self.__sender__ = sender

    def setRecipient(self, recipient: str):
        self.__recipient__ = recipient

    def setType(self, type: MessageType):
        self.__type__ = type

    def setMessage(self, message: str):
        self.__message__ = message

    def getSender(self):
        return self.__sender__

    def getRecipient(self):
        return self.__recipient__

    def getType(self):
        return self.__type__

    def getMessage(self):
        return self.__message__


class Client:
    """
    This class represents a Uni-Mas Client.
    The client will be connecting directly to router using a direct socket connection.
    To connect the client use `connect()` method.
    To send message use the `send(msg)` method.
    To receive message use `recv()` method.
    To end connection use `disconnect()` method
    """
    def __init__(self, name: str):
        """
        Parameters
        ----------
        name : str
            The name of the client that should be used.
            The name can not contain '/' or be equal (case insensitive) to RECIPIENT_GLOBAL.

        Raises
        ------
        ValueError
            If name contains illegal signs or reserved name.
        """
        if '/' in name or name.lower() == RECIPIENT_GLOBAL.lower():
            raise ValueError("Attempting to use illegal client name")

        self.__name__ = name
        self.__opened__ = False

    def connect(self, **kwargs):
        """
        This function will connect Client to Router.

        Parameters
        ----------
        ip : str, optional
            The ip address where router is listening (default is 'localhost').
        port : int, optional
            The port number where router is listening (default is '42069').
        """

        self.__socket__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ip = kwargs.get('ip') or 'localhost'
        port = kwargs.get('port') or 42069

        self.__socket__.connect((ip, port))

        # register with router
        message = Message(self.__name__, RECIPIENT_GLOBAL,
                          MessageType.ADD_METAAGENT, '')
        self.__socket__.send(str.encode(str(message)))
        
        self.__opened__ = True

    def send(self, message: Message):
        """
        This function will send message to Router

        Parameters
        ----------
        message: Message
            The message to be sent to the Router
            Note: This function will set the sender to the name of the client before sending the message.

        Raises
        ------
        ConnectionError
            When connection to the server is currently not opened.
        """
        if(self.__opened__):
            message.setSender(self.__name__)
            self.__socket__.send(str.encode(str(message)))
        else:
            raise ConnectionError("The connection is not opened")

    def recv(self):
        """
        This function will receive message from the router.
        It will block until a message is available.
        If a message has been submitted before we listen for it,
        this function will return with that message.

        Returns
        -------
        Message
            The message received from the portal

        Raises
        ------
        ConnectionError
            When connection to the server is currently not opened.
        """
        if(self.__opened__):
            data = self.__socket__.recv(MESSAGE_MAX_SIZE).decode('utf-8').split('/', 3)
            return Message(data[0], data[1], data[2], data[3])
        else:
            raise ConnectionError("The connection is not opened")

    def setRecvTimeout(self, timeout):
        """
        This function will send receiving timeout for all recv after this function call.

        Parameters
        ----------
        timeout: float
            The time in seconds before recv should be terminated with exception. Use None to disable timeouts
        """
        self.__socket__.settimeout(timeout)

    def disconnect(self):
        """
        This function will disconnect the client from the router.
        Raises
        ------
        ConnectionError
            When connection to the server is currently not opened.
        """
        if(self.__opened__):
            message = Message(self.__name__, RECIPIENT_GLOBAL, MessageType.REMOVE_METAAGENT, '')
            self.__socket__.send(str.encode(str(message)))
            self.__socket__.close()
        else:
            raise ConnectionError("The connection is not opened")
