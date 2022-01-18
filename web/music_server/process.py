""" Handling background process """
from multiprocessing import Process, Queue
from typing import List, Tuple, Any


class ProcessHandler(object):

    """ Handling the background process """

    def __init__(self):
        """ Create the project """
        self.background: List[Tuple[Process, Queue, Any]] = []

    def start_process(self, target, args, job_info):
        """ Start a process running function target with arguments args. It
        would create a queue where the return value would be placed

        :target: The target function to run
        :args: The arguments for the target function
        :job_info: Information about the process
        :return: The process id of the background process

        """

        def process(args, q):
            ret = target(*args)
            q.put(ret)

        q: Queue = Queue()
        p: Process = Process(target=process, args=(args, q))

        self.background.append((p, q, job_info))
        p.start()

        return p.pid

    def status(self):
        """ Get the status of the processes
        :returns: For each background process with the current status either
        RUNNING, EXITED or FAILED.

        """
        status: List[str] = []
        for p, _, _ in self.background:
            s = p.is_alive()

            if s:
                status.append(f"{p.pid} RUNNING")
            else:
                if p.exitcode == 0:
                    status.append(f"{p.pid} EXITED")
                else:
                    status.append(f"{p.pid} FAILED")

        return status

    def get_info(self, pid):
        """ Get the information from the job with pid

        :pid: The process id
        :returns: The job information

        """

        for p, _, i in self.background:
            if p.pid == pid:
                return i

    def join(self, pid=-1):
        """ Attempt to join all or a given process, this would not block

        :pid: The process id, if -1, it would attempt to join all process
        :returns: The return value in the queue from the process

        """
        ret = []
        if pid == -1:
            status = self.status()

            for i in range(len(status)):
                if "EXITED" in status[i]:
                    ret.append(self.background[i][1].get())

        else:
            for p, q, _ in self.background:
                if p.pid == pid:
                    ret.append(q.get())
                    break

        return ret

    def cleanup(self, pid=-1):
        """ Remove finished or failed process

        :pid: cleanup process with process id
        :returns: TODO

        """
        status = self.status()

        if pid == -1:
            for i in range(len(status)):
                if "RUNNING" not in status[i]:
                    print("CLEANING", i)
                    self.background[i][0].join()
                    self.background.remove(self.background[i])
        else:
            for i in range(len(self.background)):
                p = self.background[i][0]
                if p.pid == pid:
                    p.join()
                    self.background.remove(self.background[i])
                    break

    def count(self) -> int:
        """ Return the number of process being managered
        :returns: The number of processes

        """
        return len(self.background)
