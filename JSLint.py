#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import re
import os

EXEC_LINT = 'js_lint_exec'
SETTINGS_FILE = 'JSLint.sublime-settings'

class JsLintExecCommand(sublime_plugin.WindowCommand):

	def run(self, files=[]):
		if len(files) != 1:
			raise "oops"

		settings = sublime.load_settings(SETTINGS_FILE)
		if re.search(settings.get('filename_filter')['js'], files[0]):
			self.window.run_command('exec', {
				'cmd':
					map(os.path.expanduser, settings.get('jslint', ['node', sublime.packages_path() + '/JSLint/linter.js']))  +
					settings.get('options')['js'] +
					files,
				'line_regex': settings.get('line_regex', '.*// Line ([0-9]*), Pos ([0-9]*)$'),
				'file_regex': settings.get('file_regex', '(^[^# ]+.*$)')
			})
		elif re.search(settings.get('filename_filter')['coffee'], files[0]):
			self.window.run_command('exec', {
				'cmd': settings.get('coffeelint', ['coffeelint']) + files,
				'line_regex': settings.get('line_regex', ''),
				'file_regex': settings.get('file_regex', '(^[^# ]+.*$)')
			})


class JsLintOnSave(sublime_plugin.EventListener):

	def on_post_save(self, view):
		settings = sublime.load_settings(SETTINGS_FILE)
		if settings.get('run_on_save', False) == False:
			return
		filename = view.file_name()

		if (re.search(settings.get('filename_filter')['js'], filename) or
			re.search(settings.get('filename_filter')['coffee'], filename)):
			view.window().run_command(EXEC_LINT, {
				'files': [filename]
			})


# Support calls to the old API of the JSLint package.

class JslintCommand(sublime_plugin.WindowCommand):

	def run(self):
		self.window.run_command(EXEC_LINT, {
			'files': [self.window.active_view().file_name()]
		})
