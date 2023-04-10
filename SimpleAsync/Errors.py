class NotFinished(Exception):
    "Exception is raised when the task is not yet finished"
    pass


class BlockingSocket(Exception):
    "Raised when the socket is blocking"
    pass
