#!/usr/bin/python
#-*- coding:utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Long Changjin
# 
# Author:     Long Changjin <admin@longchangjin.cn>
# Maintainer: Long Changjin <admin@longchangjin.cn>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import ConfigParser
from xdg import BaseDirectory
from os.path import exists
from os import mkdir
from deepin_utils.file import get_parent_dir
sys.path.insert(0, get_parent_dir(__file__, 2))
from constant import PROGRAM_NAME

config_dir = BaseDirectory.xdg_config_home
WEIBO_CONFIG = "%s/%s/%s" % (config_dir, PROGRAM_NAME, 'weibo.ini')
OPERATE_CONFIG = "%s/%s/%s" % (config_dir, PROGRAM_NAME, 'config.ini')
COOKIE_FILE = "%s/%s/%s" % (config_dir, PROGRAM_NAME, 'cookie.txt')

if not exists("%s/%s" % (config_dir, PROGRAM_NAME)):
    mkdir("%s/%s" % (config_dir, PROGRAM_NAME))
if not exists(WEIBO_CONFIG):
    open(WEIBO_CONFIG, 'wb').close()
if not exists(OPERATE_CONFIG):
    open(OPERATE_CONFIG, 'wb').close()

class WeiboConfig(object):
    '''Weibo config'''
    def __init__(self, config_file=WEIBO_CONFIG):
        '''
        init config
        @param config_file: the file to save config
        '''
        self.config = ConfigParser.ConfigParser()
        self.config_file = config_file
        self.config.read(config_file)

    def sina_get(self):
        '''
        get sina info
        @return: all options value in Sina section
        '''
        return self.get('Sina')

    def tencent_get(self):
        '''
        get tencent info
        @return: all options value in Tecent section
        '''
        return self.get('Tencent')

    def twitter_get(self):
        '''
        get twitter info
        @return: all options value in Twitter section
        '''
        return self.get('Twitter')

    def get(self, weibo, opt=None):
        '''
        get weibo info
        @param weibo: the section name 
        @param opt: the options name
        @return: the opt value if the opt in the section, else None
        '''
        if not self.config.has_section(weibo):
            return None
        if opt:
            return self.config.get(weibo, opt) if self.config.has_option(weibo, opt) else None
        back = {}
        for option in self.config.options(weibo):
            back[option] = self.config.get(weibo, option)
        return back

    def tencent_set(self, **kw):
        '''set tencent info'''
        self.set('Tencent', **kw)

    def sina_set(self, **kw):
        '''set sina info'''
        self.set('Sina', **kw)

    def twitter_set(self, **kw):
        '''set twitter info'''
        self.set('Twitter', **kw)

    def set(self, weibo, **kw):
        '''
        set weibo info
        @param weibo: the section name 
        @param kw: some option and value
        '''
        if not self.config.has_section(weibo):
            self.config.add_section(weibo)
        for option in kw:
            self.config.set(weibo, option, kw[option])
        self.config.write(open(self.config_file, 'wb'))
    
    def __getattr__(self, kw):
        ''' __getattr__'''
        try:
            weibo, opt = kw.split('_')[0:2]
            return self.get(weibo, opt)
        except:
            return None
    

class OperateConfig(object):
    '''operate config'''
    def __init__(self, config_file=OPERATE_CONFIG):
        '''
        init config
        @param config_file: the file to save config
        '''
        self.config = ConfigParser.ConfigParser()
        self.config_file = config_file
        self.config.read(config_file)

    def get(self, section, opt=None):
        '''
        get section info
        @param section: the section name 
        @param opt: the options name
        @return: the opt value if the opt in the section, else None
        '''
        if not self.config.has_section(section):
            return None
        if opt:
            return self.config.get(section, opt) if self.config.has_option(section, opt) else None
        back = {}
        for option in self.config.options(section):
            back[option] = self.config.get(section, option)
        return back

    def set(self, section, **kw):
        '''
        set section info
        @param section: the section name 
        @param kw: some option and value
        '''
        if not self.config.has_section(section):
            self.config.add_section(section)
        for option in kw:
            self.config.set(section, option, kw[option])
        self.config.write(open(self.config_file, 'wb'))
        
    def __getattr__(self, kw):
        ''' __getattr__'''
        try:
            section, opt = kw.split('_')[0:2]
            return self.get(section, opt)
        except:
            return None
    
if __name__ == '__main__':
    c = WeiboConfig()
    print c.sina_get()
    print c.Sina_ab
