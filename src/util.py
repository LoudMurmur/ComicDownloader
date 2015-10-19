#!/usr/bin/env python
# --*-- encoding: iso-8859-1 --*--

import os
import urllib2
from os.path import split

def getProjectPath():
    """retourne le chemin absolu du projet quel que soit l'emplacement de départ"""
    util_path = os.path.realpath(__file__)
    src_path, _ = split(util_path)
    return src_path + "/../"

def getDataPath():
    return getProjectPath() + "data"

def installProxyConnectionIfNecessary(config):
    """instal a proxy handler if necessary"""
    if config.isProxyRequired():
        protocol = config.getProxyProtocol()
        adress = config.getProxyAdress()
        proxy = urllib2.ProxyHandler({protocol: adress})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)

def ensureComicPath(comic_path):
    if not os.path.exists(comic_path):
        os.makedirs(comic_path)
