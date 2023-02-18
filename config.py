from my_kayboards import Keyboards
from vkbottle import CtxStorage


qiwi_api_key = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjlweXRvNS0wMCIsInVzZXJfaWQiOiI3OTk5ODU5NzQwMiIsInNlY3JldCI6ImEzMzUxMDUxN2ZkMWY3N2U4MTBiMDY1MDcwYzQxMDA4MGIyMmJlYmVhOGQ4OGE4NjA5YzhhYWYyM2ExNTAwMmMifX0="
vk_bot_api_key = "vk1.a.r3noLcROF-h3hMPhWEB3a7NE4AakexlLaWmJR6puFS9DA7Y6L4ewqUHLN-joI8yNBBIHiMChmmHYrtsYauE4Jf4cUhDZL_0nqZVcoWULNTk7FkPZvj47ZoJzvltaGwLx_7o4xYHm1UluBsMcc4-BVA_vmHsmqSoOtcpH3beIkdJ6T8x2RcdSwqJE-SYHHxuwyPuuLuMBf5HR60HabzfovA"
lolz_url = "https://lzt.market/"
qiwi_number = "9998597402"
qiwi_password = "Bodya4832"
sikret_word = "Программист"
lolz_login = "bp1512"
lolz_password = "15122006diana"

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