# vim: set ts=4 sw=4 et fileencoding=utf-8:

from __future__ import print_function

import sublime
import sublime_plugin
import os
import re


def plugin_loaded():
    print('Loaded Pablo!!!')


def plugin_unloaded():
    print('No more Pablo :(')


def recursive_find(window_paths, starting_path, file_name):
    path = os.path.abspath(starting_path)

    while any(path.startswith(os.path.abspath(window_path))
              for window_path in window_paths):

        search_target = os.path.join(path, file_name)
        if (os.path.exists(search_target)):
            return search_target

        # go up one level and try again
        path = os.path.abspath(os.path.join(path, '..'))
    pass


class OpenCmakelistsCommand(sublime_plugin.WindowCommand):
    def description(self):
        return 'Opens CMakeLists.txt recursively or in the file''s directory'

    def is_enabled(self):
        return True

    def run(self, extensions=[]):
        if not self.window.active_view():
            return

        file_name = self.window.active_view().file_name()
        if not file_name:
            return

        path = os.path.dirname(file_name)
        _, extension = os.path.splitext(file_name)

        if extensions and extension.lstrip('.') not in extensions:
            return

        target = recursive_find(self.window.folders(), path, 'CMakeLists.txt')
        if target is None:
            target = os.path.join(path, 'CMakeLists.txt')

        self.window.open_file(target)


# TODO: make generic for all languages and do proper parsing
class ToPythonSingleQuotesCommand(sublime_plugin.TextCommand):
    def description(self):
        return 'Convert double quotes to single quotes'

    def is_enabled(self):
        return True

    def run(self, edit):
        def convert(s):
            return s.replace("'", "''").replace('"', "'")

        for region in self.view.sel():
            if region.empty():
                region = self.view.line(region)

            self.view.replace(edit, region, convert(self.view.substr(region)))


class RgbToHex(sublime_plugin.TextCommand):
    RX = re.compile(r'^(\d{1,3})\D+(\d{1,3})\D+(\d{1,3})\D*(\d{1,3})?$')

    def description(self):
        return 'Convert three or four decimal numbers to hex'

    def run(self, edit):
        def convert(s):
            '''Convert to hex or return the original string'''
            match = self.RX.match(s)
            if match:
                numbers = map(int, filter(None, match.groups()))
                return '#' + ''.join('{:02x}'.format(i) for i in numbers)
            else:
                return s

        for region in self.view.sel():
            if region.empty():
                region = self.view.line(region)

            self.view.replace(edit, region, convert(self.view.substr(region)))
