from multiprocessing import Process

from jobs.sms import sms_job


def start_sms_job():
    worker = Process(target=sms_job)
    worker.start()
    return [worker]


def close_workers(workers):
    for worker in workers:
        worker.terminate()
        worker.join()
        worker.close()
