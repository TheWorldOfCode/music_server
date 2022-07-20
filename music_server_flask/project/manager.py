""" Manage celery task """
from threading import Lock
from typing import List, Tuple
from celery.result import AsyncResult


class Manager():

    """ Managements of celery task """
    def __init__(self):
        """ Create the object """
        self.lock = Lock()
        self.task_ids = {}

    def init_app(self, celery) -> None:
        """ Initialize the Manager

        @param celery The celery object

        """

        self._celery = celery

    def add_task(self, task_id: str, name: str) -> None:
        """ Add task to manager.

            @param task_id The id of the task
            @param name The name of the task
        """
        self.lock.acquire()
        self.task_ids[str(task_id)] = name
        self.lock.release()

    def remove_task(self, task_id: str) -> None:
        """ Remove a task from manager

        @param task_id The id of the task 

        """
        self.lock.acquire()
        self.task_ids.pop(task_id)
        self.lock.release()

    def get_status(self) -> List[Tuple[str, str]]:
        """ Get the status of the tasks """
        self.lock.acquire()

        celery = self._celery

        results = []

        for id in self.task_ids.keys():
            task = celery.AsyncResult(id)
            results.append((self.task_ids[id], task.status))

        self.lock.release()

        return results

    def get_task_status(self, task_id: str) -> str:
        """ Get the status of a specify task

        @param task_id The id of the task
        @return The status of the task

        """
        self.lock.acquire()

        status = self._celery.AsyncResult(task_id).status

        self.lock.release()

        return status

    def get_result(self, task_id: str) -> AsyncResult:
        """ Get the result of a specify task

        @param task_id The id of the task
        @return The AsyncResult from celery

        """
        self.lock.acquire()

        result = self._celery.AsyncResult(task_id)

        self.lock.release()

        return result

    def get_results(self, status="success") -> List[AsyncResult]:
        """ Return the results from tasks

            @param status The status of the result, either success or failed
            @return A list of the results 
        
        """
        if status not in ["success", "failed"]:
            raise Exception("Known status, only success or failed is allowed")

        self.lock.acquire()
        
        celery = self._celery

        results = []

        for id in self.task_ids.keys():
            task = celery.AsyncResult(id)
            if task.status.lower() == status:
        
                results.append({
                    "name": self.task_ids[id], 
                    "id": id, 
                    "data": task.result})

        self.lock.release()

        return results



    def retry(self, task_id: str) -> None:
        """ Retry task 

            @param task_id The id of the task to retry 

        """
        self.lock.acquire()

        meta = self._celery.backend.get_task_meta(task_id)
        print(self._celery.tasks.keys())
        print(meta)
        task = self._celery.tasks[meta['name']]
        task.apply_async(args=meta['args'], kwargs=meta['kwargs']) 

        self.lock.release()