#!/usr/bin/env python
# --*-- encoding: iso-8859-1 --*--

import loggermanager
import os
import util
import urllib2
import traceback

from core.configmanager import Config

class GenericDownloader(object):
    def __init__(self, comic_section):
        self.config = Config([os.path.join(util.getProjectPath(), "config/config.desc")])
        self.comic_name = self.config.getComicName(comic_section)
        self.start_url = self.config.getComicStartUrl(comic_section)
        self.comic_path = os.path.join(util.getDataPath(), self.comic_name)
        self.quoteNumberForNextLink = self.config.getQuoteNumberForNextLink(comic_section)
        self.quoteNumberForImageLink = self.config.getQuoteNumberForImageLink(comic_section)
        self.localisationStringForNextLink = self.config.getLocalisationStringForNextLink(comic_section)
        self.localisationOffsetForNextLink = self.config.getOffsetForNextLink(comic_section)
        self.localisationStringForImageLink = self.config.getLocalisationStringForImageLink(comic_section)
        self.localisationOffsetForImageLink = self.config.getOffsetForImageLink(comic_section)
        self.logger = loggermanager.getLogger(__name__ + "." + comic_section)

    def locateInPage(self, text, pageAsList):
        """
        Locate some text in a page, return a list containing the number of each Line
        where the text was found
            -text : a unicode string encoded in utf8
            -page : file containing the html code of the page as a list of string
        """
        res = []
        for i, line in enumerate(pageAsList):
            if line.find(text) != -1:
                res.append(i)
        return res

    def downloadImage(self, url, filename):
        """Download an image from the url and rename it as filename,
        filename contains also the path of the image"""
        self.logger.info("downloading with urllib2 " + url)
        self.logger.info("to " + filename)
        f = urllib2.urlopen(url)
        data = f.read()
        with open(filename, "wb") as code:
            code.write(data)

    def getHtmlAsList(self, url):
        return urllib2.urlopen(url).read().decode('utf8').split(u'\n')

    def getImageUrl(self, htmlAsList):
        imgUrl = self.getUrl(
                             htmlAsList,
                             self.localisationStringForImageLink,
                             self.localisationOffsetForImageLink,
                             self.quoteNumberForImageLink
                             )

        if self.config.doImageLinkRequireBaseLink(self.comic_name):
            imgUrl = self.config.getImageBaseLink(self.comic_name) + imgUrl

        return imgUrl

    def getNextPageUrl(self, htmlAsList):
        next_link = self.getUrl(
                                htmlAsList,
                                self.localisationStringForNextLink,
                                self.localisationOffsetForNextLink,
                                self.quoteNumberForNextLink
                                )

        if self.config.doNextLinkRequireBaseLink(self.comic_name):
            next_link = self.config.getNextLinkBase(self.comic_name) + next_link

        self.logger.info("Going to " + next_link)
        return next_link

    def getUrl(self, htmlAsList, ls, offset, quoteNumber):
        quote = "\""
        lcs_pos = self.locateInPage(ls, htmlAsList)
        link_line = htmlAsList[lcs_pos[0]+offset]
        for _ in range(quoteNumber):
            link_line = link_line[link_line.find(quote)+1:]
        return link_line[:link_line.find(quote)]

    def saveLastViewedPage(self):
        pass

    def getLastViewedPage(self):
        pass

    def downloadComic(self):
        util.installProxyConnectionIfNecessary(self.config)
        util.ensureComicPath(self.comic_path)
        url = self.start_url
        count = 1
        try:
            while True:
                htmlAsList = self.getHtmlAsList(url)
                image_url =  self.getImageUrl(htmlAsList)
                _, img_ext = os.path.splitext(image_url)
                imageNewName = os.path.join(self.comic_path,
                                            self.comic_name + str(count).zfill(4) + img_ext)
                self.downloadImage(image_url, imageNewName)
                count = count + 1
                url = self.getNextPageUrl(htmlAsList)
        except Exception, err:
            self.logger.info("Done or error")
            self.logger.info(traceback.format_exc())
