import time

from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co.set_paths(local_port=9153)


def get_doubao(chat_text):
    page = ChromiumPage()
    tab = page.get_tab()
    tab.get("https://www.doubao.com/chat/")
    tab.wait(2)
    tab.ele('xpath=//*[@id="semi-modal-body"]//svg').click(by_js=True)
    input_text = tab.ele("xpath=//textarea[contains(@class, 'semi-input-textarea')]")
    input_text.click()
    input_text.input(chat_text)
    time.sleep(1)
    input_text.tab.actions.key_down('ENTER')
    tab.wait(20)
    value = tab.ele("xpath=//div[contains(@class, 'auto-hide-last-sibling-br')]").html
    tab.close()
    return value


# print(get_doubao('你好'))

