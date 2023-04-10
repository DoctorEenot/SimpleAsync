import errno
import os
import Task


def read_async(ctx, filename: str, read_batch=2048):
    to_return = ""

    try:
        pipe = os.open(filename,
                       os.O_RDONLY | os.O_NONBLOCK
                       )
        while True:
            try:
                buf = os.read(pipe, read_batch)
                if not buf:
                    break
                else:
                    content = buf.decode("utf-8")
                    to_return += content
                    # yield Task.Continue()
            except OSError as e:
                if e.errno == 11:
                    yield Task.Continue()
                else:
                    raise e

    except OSError as e:
        if e.errno == errno.ENOENT:
            pipe = None
        else:
            raise e

    print(len(to_return))

    yield Task.Result(to_return)
