""" """
from audio_control import ProcessHandler
from time import sleep


def test_process(i):
    sleep(5*i)
    return i


handler = ProcessHandler()

handler.start_process(target=test_process, args=0)
handler.start_process(target=test_process, args=1)
handler.start_process(target=test_process, args=2)

j = 0
while j < 3:
    status = handler.status()
    print("Status:")
    for s in status:
        print("\t" + s)

    if True in ["EXITED" in s for s in status]:
        print("A process is done")
        ret = handler.join()
        print("The return value was", ret)
        j += 1
        handler.cleanup()

    print("WAITING")
    sleep(1)

print("DONE")
