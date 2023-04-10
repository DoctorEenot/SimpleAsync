import Errors


class Future:
    pass


class Result(Future):
    value = None

    def __init__(self, value):
        self.value = value


class Task:
    def __init__(self, id: int, ctx, task, *args, **kwargs):
        self.task = iter(task(ctx, *args, *kwargs))
        self.id = id
        self._ctx = ctx

    def __iter__(self):
        return self

    def __next__(self) -> Future:
        try:
            return next(self.task)
        except StopIteration:
            return Result(None)


class Continue(Future):
    pass


class Await(Future):
    def __init__(self, child_task, *args, **kwargs):
        self.task = child_task
        self.args = args
        self.kwargs = kwargs


class AwaitReturn(Future):
    def __init__(self, child_task: Task):
        self.task = child_task


# if __name__ == "__main__":
#     task = Task(1, range, 1, 5)

#     for t in task:
#         print(t)
