#coding: UTF-8

import logging

try:
    from urllib3.exceptions import ConnectionError as NoServerAvailable
except ImportError:
    try:
        from urllib3.exceptions import ProtocolError as NoServerAvailable
    except ImportError:
        from urllib3.exceptions import HTTPError as NoServerAvailable

from .commit_differ import CommitDiffer
from .indexes import RepoStatusIndex, RepoFilesIndex

from seafobj import commit_mgr
from seaserv import seafile_api

logger = logging.getLogger('seafes')

MAX_ERRORS_ALLOWED = 1000

class FileIndexUpdater(object):
    '''Update the repo file info index'''

    def __init__(self, es_conn):
        self.es_conn = es_conn

        self.status_index = RepoStatusIndex(es_conn)
        self.files_index = RepoFilesIndex(es_conn)
        self.error_counter = 0

    def abort_if_too_many_errors(self):
        self.error_counter += 1
        if self.error_counter > MAX_ERRORS_ALLOWED:
            msg = 'ABORT this update process because of too much errors'
            logger.warning('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            logger.warning(msg)
            logger.warning('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            raise Exception(msg)

    def run(self):
        repo_commits = seafile_api.get_all_repo_id_commit_id()

        self.clear_deleted_repo(repo_commits)

        logger.debug('%s repos in total' % len(repo_commits))
        for e in repo_commits:
            try:
                self.update_repo(e.repo_id, e.commit_id)
            except NoServerAvailable:
                logger.warning('elasticsearch server not available')
                return
            except:
                logger.exception('Error when index repo %s', e.repo_id)
                self.abort_if_too_many_errors()

    def clear_deleted_repo(self, repo_commits):
        repo_all = [e.get('id') for e in self.status_index.get_all_repos_from_index()]

        repo_exist = []
        if repo_commits:
            repo_exist = [e.repo_id for e in repo_commits]

        repo_deleted = set(repo_all) - set(repo_exist)
        logger.info("""Index repos count: %d, total repos count: %d, 
                    start to delete %d stale repos from index."""
                    %(len(repo_all), len(repo_exist), len(repo_deleted)))
        for repo in repo_deleted:
            self.delete_repo(repo)
            logger.info('Repo %s has been deleted from index.' % repo)

    def update_files_index(self, repo_id, old_commit_id, new_commit_id):
        if old_commit_id == new_commit_id:
            return

        old_root = None
        if old_commit_id:
            old_commit = commit_mgr.load_commit(repo_id, 0, old_commit_id)
            old_root = old_commit.root_id

        new_commit = commit_mgr.load_commit(repo_id, 0, new_commit_id)
        new_root = new_commit.root_id
        version = new_commit.get_version()

        if old_root == new_root:
            return

        differ = CommitDiffer(repo_id, version, old_root, new_root)
        added_files, deleted_files, added_dirs, deleted_dirs, modified_files = differ.diff()

        # if inrecovery:
        #     added_files = filter(lambda x:not es_check_exist(es, repo_id, x), added_files)

        # total_changed = sum(map(len, [added_files, deleted_files, deleted_dirs, modified_files]))
        # if total_changed > 10000:
        #     logger.warning('skip large changeset: %s files(%s)', total_changed, repo_id)
        #     return

        self.files_index.add_files(repo_id, version, added_files)
        self.files_index.delete_files(repo_id, deleted_files)
        self.files_index.add_dirs(repo_id, version, added_dirs)
        self.files_index.delete_dirs(repo_id, deleted_dirs)
        self.files_index.update_files(repo_id, version, modified_files)

    def check_recovery(self, repo_id):
        status = self.status_index.get_repo_status(repo_id)
        if status.need_recovery():
            logger.warning('%s: inrecovery', repo_id)
            old = status.from_commit
            new = status.to_commit
            self.update_files_index(repo_id, old, new)
            self.status_index.finish_update_repo(repo_id, new)

    def update_repo(self, repo_id, latest_commit_id):
        self.check_recovery(repo_id)

        status = self.status_index.get_repo_status(repo_id)
        if latest_commit_id != status.from_commit:
            logger.info('Updating repo %s' % repo_id)
            logger.debug('latest_commit_id: %s, status.from_commit: %s' %
                         (latest_commit_id, status.from_commit))
            old = status.from_commit
            new = latest_commit_id
            self.status_index.begin_update_repo(repo_id, old, new)
            self.update_files_index(repo_id, old, new)
            self.status_index.finish_update_repo(repo_id, new)
        else:
            logger.debug('Repo %s already uptodate', repo_id)

    def delete_repo(self, repo_id):
        if len(repo_id) != 36:
            return
        self.status_index.delete_repo(repo_id)
        self.files_index.delete_repo(repo_id)
