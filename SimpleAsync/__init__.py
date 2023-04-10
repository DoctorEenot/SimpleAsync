import Task
import Cycle
import Errors
from async_implementations import *
import File


if __name__ == "__main__":

    def return_task(ctx, num: int):
        num += 1
        yield Task.Continue()
        num += 1

        # return result from a task
        yield Task.Result(num)

    def another_task(ctx):
        for s in ["first", "second", "third"]:
            print(s)

            # telling cycle, that this function will run again later
            # used only for demonstration purposes
            yield Task.Continue()

    def some_task(ctx, start, end):
        '''
            Generic task, calls 2 other tasks in loop
        '''
        for i in range(start, end):
            print(i)

            # just calling another async function
            yield Task.Await(another_task)

            # returning value from awaited function
            awaited_task = Task.Task(ctx.last_task_id, ctx, return_task, i)
            yield Task.AwaitReturn(awaited_task)
            print(ctx.get_result(awaited_task.id))

        yield None

    def background_task(ctx):
        '''
            Some long task, that needs to be ran for a while
        '''

        for i in range(1, 50):
            print(i)
            yield Task.Continue()

    # creating main executor cycle
    main_cycle = Cycle.Cycle()

    # registering tasks to run
    main_cycle.register_task(some_task, 1, 5)
    main_cycle.register_task(some_task, 1, 5)
    main_cycle.register_task(background_task)
    main_cycle.register_task(File.read_async, "testfile.txt")
    main_cycle.register_task(File.read_async, "testfile.txt")
    main_cycle.register_task(File.read_async, "testfile.txt")
    main_cycle.register_task(File.read_async, "testfile.txt")
    main_cycle.register_task(File.read_async, "testfile.txt")
    main_cycle.register_task(File.read_async, "testfile.txt")
    main_cycle.register_task(File.read_async, "testfile.txt")
    main_cycle.register_task(File.read_async, "testfile.txt")

    # running cycle
    main_cycle.run_cycle()
