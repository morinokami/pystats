import io
import os
import zipfile

import requests

from . import api
from . import utils


class Project:

    def __init__(self, user, repo):
        self.user = user
        self.repo = repo

    def _download_project(self):
        res = {}

        project = io.BytesIO()
        project.write(api.get_archive(self.user, self.repo))
        project_zip = zipfile.ZipFile(project)

        for file_name in project_zip.namelist():
            res[file_name] = project_zip.read(file_name)
        
        return res
    
    def _init_repo_data(self):
        attrs = api.get_attrs(self.user, self.repo)
        languages = api.get_languages(self.user, self.repo)
        
        return {
            'name': attrs['name'],
            'description': attrs['description'],
            'url': attrs['url'],
            'size': attrs['size'],  # KB
            'stars': attrs['stars'],
            'forks': attrs['forks'],
            'watchers': attrs['watchers'],
            'file_count': 0,
            'languages': languages,
            'total_line_count': 0,
            'code_line_count': 0,
            'py_line_count': 0,
            'total_blank_lines': 0,
            'code_blank_lines': 0,
            'py_blank_lines': 0,
            'inline_comments': 0,
            'block_comments': 0,
            'function_count': 0,
            'function_length': 0,  # number of statements in a function
            'average_function_length': 0,
        }

    def _update_repo_data(self, repo_data, file_path, file_data):
        c = Code(file_path, file_data)
        languages = c.get_languages()
        line_count = c.count_lines()
        blank_lines = c.count_blank_lines()
        
        repo_data['file_count'] += 1
        repo_data['total_line_count'] += line_count
        repo_data['total_blank_lines'] += blank_lines
        
        if any(l in repo_data['languages'] for l in languages):
            repo_data['code_line_count'] += line_count
            repo_data['code_blank_lines'] += blank_lines
        
        if 'Python' in languages:
            repo_data['py_line_count'] += line_count
            repo_data['py_blank_lines'] += blank_lines
            repo_data['inline_comments'] += c.count_inline_comments()
            repo_data['block_comments'] += c.count_block_comments()
            function_count, function_length = \
                c.count_approximate_function_length()
            repo_data['function_count'] += function_count
            repo_data['function_length'] += function_length

    def analyze(self):
        repo_data = self._init_repo_data()

        project = self._download_project()
        for f in project:
            if f.endswith('/'):
                # ignore directories
                continue
            else:
                self._update_repo_data(repo_data, f, project[f])
        
        if repo_data['function_count'] != 0:
            repo_data['average_function_length'] = \
                repo_data['function_length'] / repo_data['function_count']

        return repo_data


class Code:

    def __init__(self, file_path, file_data):
        self.file_path = file_path
        if utils.is_text(file_data):
            self.data = file_data
        else:
            self.data = None
    
    def count_lines(self):
        lines = self.data.split(b'\n') if self.data else []
        return len(lines)

    def count_blank_lines(self):
        lines = self.data.split(b'\n') if self.data else []
        return len(list(l for l in lines if l.split() == []))

    def count_inline_comments(self):
        lines = self.data.split(b'\n') if self.data else []
        return len(list(l for l in lines if utils.is_inline_comment(l)))

    def count_block_comments(self):
        counter = 0
        comments = utils.extract_block_comments(self.data)
        for c in comments:
            counter += c.count(b'\n') + 1
        return counter
    
    def count_approximate_function_length(self):
        counter = 0
        functions = utils.extract_functions(self.data)
        for f in functions:
            counter += len(f.body)
        return len(functions), counter
    
    def get_languages(self):
        filename = os.path.basename(self.file_path)
        return utils.get_languages(filename)
