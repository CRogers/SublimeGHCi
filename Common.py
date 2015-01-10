import sublime, re

def all_views():
    for window in sublime.windows():
        for view in window.views():
            yield view

def find_open_file(file_name):
    for view in all_views():
        if view.file_name() == file_name:
            return view

def find_in_open_files(pattern):
    for view in all_views():
        region = view.find(pattern, 0)
        if region.begin() != -1 and region.end() != -1:
            return {"view": view, "region": region}