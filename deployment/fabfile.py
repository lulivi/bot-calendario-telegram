#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deployment of the app.

Copyright 2017, Luis Liñán (luislivilla@gmail.com)

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>
"""
from fabric.api import cd, run, sudo


def RemoveApp():
    # Delete the repository
    run('sudo rm -rf ./bot-calendario-telegram')


def InstallApp():
    RemoveApp()
    # Download the repository
    run('git clone https://github.com/lulivi/bot-calendario-telegram.git')

    # Install the app requirements
    run('cd bot-calendario-telegram/ && pip install -r requirements.txt')


def StartApp():
    # Start web service
    with cd('bot-calendario-telegram'):
        with cd('bot_calendario_telegram'):
            sudo('hug -p 80 -f reminder_rest_api.py')
