import queue
import threading

# create a queue to handle background tasks
q = queue.Queue()

def worker():
  while True:
    message = q.get()
    print(f'Working on {message}')
    with open('log.txt', mode='a') as f:
      f.write(message + '\n')
    print(f'Finished {message}')
    q.task_done()

# turns-on the worker thread
threading.Thread(target=worker, daemon=True).start()

def append_log_bg(message: str):
  q.put(message)

# blocks until all items in the queue have been processed
q.join()
