#!/usr/bin/env python3
"""Config script for app"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Config class for Flask app"""
    SECRET_KEY = 'Just-a-random-basic-word'
    SQLALCHEMY_DATABASE_URI ='sqlite:///app.db'
      
    SQLALCHEMY_TRACK_MODIFICATIONS = False

