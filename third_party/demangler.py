#!/usr/bin/python

'''
Simple tool to run the demangler.

(C) 2010 Alon Zakai, MIT licensed

Usage: demangler.py FILENAME SPLITTER

Make sure you define ~/.emscripten, and fill it with something like

JS_ENGINE=[os.path.expanduser('~/Dev/v8/d8')]
JS_ENGINE_PARAMS=['--']

or

JS_ENGINE=[os.path.expanduser('~/Dev/tracemonkey/js/src/js')]
JS_ENGINE_PARAMS=[]

'''

import os, sys, subprocess

CONFIG_FILE = os.path.expanduser('~/.emscripten')
exec(open(CONFIG_FILE, 'r').read())

data = open(sys.argv[1], 'r').readlines()
splitter = sys.argv[2]

SEEN = {}
for line in data:
  if len(line) < 4: continue
  if line[:2] != '  ': continue
  if line[2] != '_': continue
  func = line.lstrip().split(splitter)[0]
  if func in SEEN: continue
  SEEN[func] = True
  args = JS_ENGINE + [os.path.join(os.path.dirname(__file__), 'gcc_demangler.js')] + JS_ENGINE_PARAMS + [func[1:]]
  cleaned = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
  if cleaned is None: continue
  if 'Fatal exception' in cleaned: continue
  cleaned = cleaned[1:-2]
  if cleaned == '(null)': continue
  if ' throw ' in cleaned: continue
  print func, '=', cleaned
