import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from .requestAndBeautifulSoup import getBSText, beautifulJson
from .decorator import wait


__all__ = [
    "getMCFunc", "loginNoCaptcha", "loginNoCaptchaHeadLess", "getDriver",
    "getDriverHeadLess", "getSeleniumText", "getSeleniumJson", "getSeleniumSoup",
    "getSeleniumTextHeadLess", "getSeleniumJsonHeadLess", "getSeleniumSoupHeadLess",
]


def getMCFunc(driver, method_string):
    ''' 根据字符串返回对应的selenium定位函数 '''
    method_dict = {
        "id": driver.find_element_by_id,
        "name": driver.find_element_by_name,
        "tag_name": driver.find_element_by_tag_name,
        "css_selector": driver.find_element_by_css_selector,
        "link_text": driver.find_element_by_link_text,
        "partial_link_text": driver.find_element_by_partial_link_text,
        "xpath": driver.find_element_by_xpath,
        "class_name": driver.find_element_by_class_name,
    }

    methods_dict = {
        "id": driver.find_elements_by_id,
        "name": driver.find_elements_by_name,
        "tag_name": driver.find_elements_by_tag_name,
        "css_selector": driver.find_elements_by_css_selector,
        "link_text": driver.find_elements_by_link_text,
        "partial_link_text": driver.find_elements_by_partial_link_text,
        "xpath": driver.find_elements_by_xpath,
        "class_name": driver.find_elements_by_class_name,
    }

    for method in methods_dict:
        if method_string[-1] == "s" and method_string != "cs" and method_string != "css" and method_string != "ss":
            if method_string[:-1] in method:
                return methods_dict[method]
        elif method_string in method:
            return method_dict[method]


@wait
def loginNoCaptchaAction(mc_username, mc_password, mc_submit_button,
                         driver, username, password):
    """ 完成登录动作 """
    # 登录
    username_element = getMCFunc(driver, mc_username[0])(
        mc_username[1])
    password_element = getMCFunc(driver, mc_password[0])(
        mc_password[1])
    submit_button = getMCFunc(driver, mc_submit_button[0])(
        mc_submit_button[1])
    username_element.clear()
    password_element.clear()
    username_element.send_keys(username)
    password_element.send_keys(password)
    submit_button.click()
    time.sleep(2)


def loginNoCaptcha(url, method_params, username, password):
    ''' 登录无验证码的网站 '''
    mc_username = method_params[0]
    mc_password = method_params[1]
    mc_submit_button = method_params[2]
    # 进入首页
    driver = getDriver()
    driver.get(url)
    time.sleep(2)

    # 登录
    loginNoCaptchaAction(mc_username, mc_password,
                         mc_submit_button, driver, username, password)

    return driver


@wait
def loginNoCaptchaActionHeadless(mc_username, mc_password, mc_submit_button,
                                 driver, username, password):
    """ 无头模式完成登录动作 """
    # 登录
    username_element = getMCFunc(driver, mc_username[0])(
        mc_username[1])
    password_element = getMCFunc(driver, mc_password[0])(
        mc_password[1])
    submit_button = getMCFunc(driver, mc_submit_button[0])(
        mc_submit_button[1])
    username_element.clear()
    password_element.clear()
    username_element.send_keys(username)
    password_element.send_keys(password)
    submit_button.click()
    time.sleep(2)


def loginNoCaptchaHeadLess(url, method_params, username, password):
    ''' 无头模式登录无验证码的网站 '''
    mc_username = method_params[0]
    mc_password = method_params[1]
    mc_submit_button = method_params[2]
    # 进入首页
    driver = getDriverHeadLess()
    driver.get(url)
    time.sleep(2)

    # 登录
    loginNoCaptchaAction(mc_username, mc_password,
                         mc_submit_button, driver, username, password)

    return driver


def getDriver(options=None):
    ''' 返回Selenium Chrome Driver '''
    if options:
        driver = webdriver.Chrome(chrome_options=options)
    else:
        options = Options()
        driver = webdriver.Chrome(chrome_options=options)
    return driver


def getDriverHeadLess():
    ''' 返回Selenium HeadLess Chrome Driver '''
    options = Options()
    options.add_argument('--headless')
    driver = getDriver(options=options)
    return driver


def getSeleniumText(url, sleep_time=2):
    """ 获取driver.page_source """
    driver = getDriver()
    driver.get(url)
    time.sleep(sleep_time)

    return driver.page_source


def getSeleniumJson(url, sleep_time=2):
    """ 获取json.loads(driver.page_source) """
    driver = getDriver()
    driver.get(url)
    time.sleep(sleep_time)

    return beautifulJson(driver.page_source)


def getSeleniumSoup(url, parser="html.parser", sleep_time=2):
    """ 获取Beatifule(driver.page_source, "html.parser") """
    driver = getDriver()
    driver.get(url)
    time.sleep(sleep_time)

    return getBSText(driver.page_source, parser)


def getSeleniumTextHeadLess(url, sleep_time=2):
    """ 无头模式获取driver.page_source """
    driver = getDriverHeadLess()
    driver.get(url)
    time.sleep(sleep_time)

    return driver.page_source


def getSeleniumJsonHeadLess(url, sleep_time=2):
    """ 无头模式获取json.loads(driver.page_source) """
    driver = getDriverHeadLess()
    driver.get(url)
    time.sleep(sleep_time)

    return beautifulJson(driver.page_source)


def getSeleniumSoupHeadLess(url, parser="html.parser", sleep_time=2):
    """ 无头模式获取Beatifule(driver.page_source, "html.parser") """
    driver = getDriverHeadLess()
    driver.get(url)
    time.sleep(sleep_time)

    return getBSText(driver.page_source, parser)