#!/usr/bin/env python
# encoding: utf-8
"""
ErrorIgnore.py

Created by Peter Meckiffe on 2013-03-13.
Copyright (c) 2013 UWE. All rights reserved.
"""

import sys
import os
import unittest

# Decorator to ignore Exceptions
class ErrorIgnore(object):
   def __init__(self, errors, errorreturn = None, errorcall = None):
      self.errors = errors
      self.errorreturn = errorreturn
      self.errorcall = errorcall

   def __call__(self, function):
      def returnfunction(*args, **kwargs):
         try:
            return function(*args, **kwargs)
         except Exception as E:
            if type(E) not in self.errors:
               raise E
            if self.errorcall is not None:
               self.errorcall(E, *args, **kwargs)
            return self.errorreturn
      return returnfunction