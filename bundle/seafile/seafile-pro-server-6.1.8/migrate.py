#!/usr/bin/env python
#coding: utf-8

import os
import sys
import logging
import Queue
import rados
import boto
import urllib2
import httplib
import requests
import threading
from threading import Thread
from boto.s3.key import Key

from seafobj.objstore_factory import SeafObjStoreFactory

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

class Worker(Thread):
    def __init__(self, do_work, task_queue):
        Thread.__init__(self)
        self.do_work = do_work
        self.task_queue = task_queue

    def run(self):
        while True:
            try:
                task = self.task_queue.get()
                if task is None:
                    break
                self.do_work(task)
            except Exception as e:
                logging.warning('Failed to execute task: %s' % e)
            finally:
                self.task_queue.task_done()

class ThreadPool(object):
    def __init__(self, do_work, nworker=20):
        self.do_work = do_work
        self.nworker = nworker
        self.task_queue = Queue.Queue(maxsize = 2000)

    def start(self):
        for i in xrange(self.nworker):
            Worker(self.do_work, self.task_queue).start()

    def put_task(self, task):
        self.task_queue.put(task)

    def join(self):
        self.task_queue.join()
        # notify all thread to stop
        for i in xrange(self.nworker):
            self.task_queue.put(None)

class Task(object):
    def __init__(self, repo_id, repo_version, obj_id):
        self.repo_id = repo_id
        self.repo_version = repo_version
        self.obj_id = obj_id

class ObjMigrateWorker(Thread):
    def __init__(self, orig_obj_factory, dest_obj_factory, dtype):
        Thread.__init__(self)
        self.lock = threading.Lock()
        self.dtype = dtype
        self.orig_store = orig_obj_factory.get_obj_store(dtype)
        self.dest_store = dest_obj_factory.get_obj_store(dtype)
        self.thread_pool = ThreadPool(self.do_work)

    def run(self):
        logging.info('Start to migrate [%s] object' % self.dtype)
        self.thread_pool.start()
        self.migrate()
        self.thread_pool.join()
        logging.info('Complete migrate [%s] object' % self.dtype)

    def do_work(self, task):
        try: 
            exists = self.dest_store.obj_exists(task.repo_id, task.obj_id)
        except Exception as e:
            logging.warning('[%s] Failed to check object %s existence from repo %s: %s' % (self.dtype, task.obj_id, task.repo_id, e))
            raise

        if not exists:
            try:
                data = self.orig_store.read_obj_raw(task.repo_id, task.repo_version, task.obj_id)
            except Exception as e:
                logging.warning('[%s] Failed to read object %s from repo %s: %s' % (self.dtype, task.obj_id, task.repo_id, e)) 
                raise

            try: 
                self.dest_store.write_obj(data, task.repo_id, task.obj_id)
            except Exception as e:
                logging.warning('[%s] Failed to write object %s from repo %s: %s' % (self.dtype, task.obj_id, task.repo_id, e))
                raise

    def migrate(self):
        try:
            obj_list = self.orig_store.list_objs()
        except Exception as e:
            logging.warning('[%s] Failed to list all objects: %s' % (self.dtype, e))
            raise

        for obj in obj_list:
            repo_id = obj[0]
            obj_id = obj[1]
            task = Task(repo_id, 1, obj_id)
            self.thread_pool.put_task(task)

def main():
    try:
        orig_obj_factory = SeafObjStoreFactory()
        os.environ['SEAFILE_CENTRAL_CONF_DIR'] = os.environ['DEST_SEAFILE_CENTRAL_CONF_DIR']
    except KeyError:
        logging.warning('DEST_SEAFILE_CENTRAL_CONF_DIR environment variable is not set.\n')
        sys.exit()

    dest_obj_factory = SeafObjStoreFactory()

    dtypes = ['commits', 'fs', 'blocks']
    for dtype in dtypes:
        ObjMigrateWorker(orig_obj_factory, dest_obj_factory, dtype).start()

if __name__ == '__main__':
    main()
