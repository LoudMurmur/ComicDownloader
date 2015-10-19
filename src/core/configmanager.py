#!/usr/bin/env python
# --*-- encoding: iso-8859-1 --*--

import ConfigParser
import loggermanager

class ConfigManagerException(Exception):
    pass

class Config(object):

    def __init__(self, confpathes):
        """Constructeur
            -confpathes : liste de string contenant les chemins des fichiers de configuration
        """
        self.confpathes = confpathes
        self.configParser = ConfigParser.ConfigParser()
        self.configParser.read(self.confpathes)
        self.logger = loggermanager.getLogger("core.Config")

    def getValue(self, section, key, default=None):
        try:
            self.logger.debug("Trying to get section=%s key=%s." %(section, key))
            return self.configParser.get(section, key)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            if default is not None:
                self.logger.debug("Cannot get section=%s key=%s, returning default." %(section, key))
                return default
            raise ConfigManagerException("[%s], key %s is not defined in file %s"\
                                        %(section, key, self.confpathes))

    def isProxyRequired(self):
        return self.getValue("PROXY", "proxy.required", "true").upper() == "TRUE"

    def getProxyProtocol(self):
        return self.getValue('PROXY', 'proxy.protocol')

    def getProxyAdress(self):
        return self.getProxyHost() + ":" + self.getProxyPort()

    def getProxyHost(self):
        return self.getValue('PROXY', 'proxy.host')

    def getProxyPort(self):
        return self.getValue('PROXY', 'proxy.port')

    def getComicStartUrl(self, section):
        return self.getValue(section, 'start_url')

    def getComicName(self, section):
        return self.getValue(section, 'name')

    def getLocalisationStringForNextLink(self, section):
        return self.getValue(section, 'localisationStringForNextLink')

    def getOffsetForNextLink(self, section):
        return int(self.getValue(section, 'localisationOffsetForNextLink'))

    def getQuoteNumberForNextLink(self, section):
        return int(self.getValue(section, 'quoteNumberForNextLink'))

    def getLocalisationStringForImageLink(self, section):
        return self.getValue(section, 'localisationStringForImageLink')

    def getOffsetForImageLink(self, section):
        return int(self.getValue(section, 'localisationOffsetForImageLink'))

    def getQuoteNumberForImageLink(self, section):
        return int(self.getValue(section, 'quoteNumberForImageLink'))

    def doImageLinkRequireBaseLink(self, section):
        try:
            self.getValue(section, 'appendNextImageLinkTo')
            return True
        except:
            return False

    def doNextLinkRequireBaseLink(self, section):
        try:
            self.getValue(section, 'appenNextLinkTo')
            return True
        except:
            return False

    def getImageBaseLink(self, section):
        return self.getValue(section, 'appendNextImageLinkTo')

    def getNextLinkBase(self, section):
        return self.getValue(section, 'appenNextLinkTo')
