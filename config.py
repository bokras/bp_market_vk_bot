from my_kayboards import Keyboards
from vkbottle import CtxStorage


qiwi_api_key = "="
vk_bot_api_key = "----"
lolz_url = "https://lzt.market/"
keys_url = "https://keys-ground.com/"
qiwi_number = ""
qiwi_password = ""
sikret_word = ""
lolz_login = ""
lolz_password = ""

class Bot_Data():
    def __init__(self):
        self.count_order = CtxStorage()
        self.kayboards = Keyboards()
        self.item_list = {}
        self.current_driver = None
        self.answer_text = ""
        self.selected_item = None
        self.wait_pay = False
        self.bill = None
        self.p2p = None
        self.DEBUG_IDS = ["207012171"]
        self.log_pass = []
        self.attamp = 0
