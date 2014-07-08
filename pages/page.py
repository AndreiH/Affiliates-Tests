#!/usr/bin/env python
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from unittestzero import Assert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException


class Page(object):
    '''
    Base class for all Pages
    '''

    def __init__(self, testsetup):
        '''
        Constructor
        '''
        self.testsetup = testsetup
        self.base_url = testsetup.base_url
        self.selenium = testsetup.selenium
        self.timeout = testsetup.timeout
        self._selenium_root = hasattr(self, '_root_element') and self._root_element or self.selenium

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def is_the_current_page(self):
        if self._page_title:
            WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)

        Assert.equal(self.selenium.title, self._page_title,
                     "Expected page title: %s. Actual page title: %s" % (self._page_title, self.selenium.title))
        return True

    @property
    def is_the_current_url(self):
        Assert.contains(self._page_url, self.selenium.current_url)
        return True

    def is_element_present(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            self.selenium.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def is_element_visible(self, *locator):
        try:
            return self.selenium.find_element(*locator).is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return False

    def wait_for_element_visible(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, 10).until(lambda s: self._selenium_root.find_element(*locator).is_displayed())
        except TimeoutException:
            Assert.fail(TimeoutException)
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def wait_for_element_not_visible(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, 10).until(lambda s: not self._selenium_root.find_element(*locator).is_displayed())
        except TimeoutException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def wait_for_element_present(self, *locator):
        """Wait for an element to become present."""
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, 10).until(lambda s: self._selenium_root.find_element(*locator))
        except TimeoutException:
            Assert.fail(TimeoutException)
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def wait_for_element_not_present(self, *locator):
        """Wait for an element to become not present."""
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, 10).until(lambda s: len(self._selenium_root.find_elements(*locator)) < 1)
            return True
        except TimeoutException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def open(self, url_fragment):
        self.selenium.get(self.base_url + url_fragment)

    @property
    def get_url_current_page(self):
        return self.selenium.current_url
