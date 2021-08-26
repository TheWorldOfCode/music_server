import os
from time import sleep

def remove_empty_folders(path_abs):
    walk = list(os.walk(path_abs))
    for path, _, _ in walk[::-1]:
        if len(os.listdir(path)) == 0 and path != path_abs:
            os.rmdir(path)

def db_update(client, wait=2):
    client.update()

    def still_updating():
        status = client.status()
        if 'updating_db' in status:
            return True
        return False

    sleep(wait)

    while not still_updating():
        pass

    print("Update complete")
