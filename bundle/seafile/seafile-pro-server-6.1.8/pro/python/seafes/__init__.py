#coding: UTF-8

from .indexes import RepoFilesIndex
from .connection import es_get_conn

def es_search(repo_ids, keyword, suffixes, start, size):
    conn = es_get_conn()
    files_index = RepoFilesIndex(conn)
    return files_index.search_files(repo_ids, keyword, suffixes, start, size)
