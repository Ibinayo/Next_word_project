#!/usr/bin/env python3
"""Config script for app"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Config class for Flask app"""
    SECRET_KEY = 'Just-a-random-basic-word'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
        # 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = 'postgres://next_db_62g4_user:jgaxnYDnk85xS1IOJXV7sOBpHvDxsTXP@dpg-ckv6p73amefc73dath10-a.oregon-postgres.render.com/next_db_62g4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

