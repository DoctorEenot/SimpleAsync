from Task import Task, Result, Continue, Await, AwaitReturn
from typing import List, Dict
import Errors


class Cycle:
    __running_queue: List[Task] = []
    "FIFO"

    __awaiting: Dict[int, Task] = {}
    "child_id: parent_task"

    __futures_results: Dict[int, Result] = {}
    "task_id: Result"

    __last_task_id: int

    def __init__(self):
        self.__last_task_id = 0

    def register_raw_task(self, task: Task):
        self.__running_queue.append(task)
        self.__last_task_id += 1

    def register_task(self, task, *args, **kwargs) -> int:
        task = Task(self.last_task_id, self, task, *args, **kwargs)
        self.__running_queue.append(task)
        self.__last_task_id += 1
        return task.id

    @property
    def last_task_id(self):
        return self.__last_task_id

    def get_result(self, child_id: int):
        res = self.__futures_results.pop(child_id, None)
        if res is None:
            raise Errors.NotFinished

        return res.value

    def run_cycle(self):
        while len(self.__running_queue) != 0:
            task = self.__running_queue.pop(0)  # get first task in queue

            task_res = next(task)  # run one tasks iteration

            if isinstance(task_res, Continue):
                # task will continue execution later
                self.__running_queue.append(task)
            elif isinstance(task_res, Await):
                # task awaits another task

                # register awaited task
                task_id = self.register_task(
                    task_res.task, *task_res.args, **task_res.kwargs)

                # move current tast to await queue
                self.__awaiting[task_id] = task
            elif isinstance(task_res, AwaitReturn):
                new_task = task_res.task

                # register awaited task
                self.register_raw_task(new_task)

                # move current tast to await queue
                self.__awaiting[new_task.id] = task
            elif isinstance(task_res, Result):
                # task stopped

                # get awaiting task, if it exists
                parent_task = self.__awaiting.pop(task.id, None)
                if parent_task is not None:
                    # put awaiting task into running queue
                    self.__running_queue.append(parent_task)

                # remember result from current task
                self.__futures_results[task.id] = task_res
