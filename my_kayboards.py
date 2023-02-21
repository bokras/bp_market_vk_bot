from vkbottle import Keyboard,Text,EMPTY_KEYBOARD, OpenLink, template_gen, TemplateElement

class Keyboards():
    def __init__(self):

        self.empty = EMPTY_KEYBOARD

        self.main_menu_keyboard = (
            Keyboard(inline=True)
            .add(Text("Купить"))
        )

        self.select_type_keyboard = (
            Keyboard(inline=True)
            .add(Text("Аккаунты",))
            .add(Text("Ключи"))
            .row()
            .add(Text("Кино"))
            .add(Text("Vpn"))
        )

        self.select_market_keyboard = (
            Keyboard(inline=True)
            .add(Text("Steam"))
            .add(Text("Social Club"))
            .add(Text("Epic Games"))
            .add(Text("Origin"))
            .row()
            .add(Text("Uplay"))
        )



        self.select_game_keyboard = (
            Keyboard(inline=True)
            .add(Text("GTA V"))
            .add(Text("Red Dead Redemption 2"))
            .row()
            .add(Text("Ввести название вручную"))
            .row()
            .add(Text("Назад"))
        )


        self.buy_selected_account_keyboard = (
            Keyboard(inline=True)
            .add(Text("купить"))
            .add(Text("посмотреть ещё"))
        )

        self.change_user_keyboard = (
            Keyboard(inline=True)
            .add(Text("Перепривязать аккаунт на меня"))
            .add(Text("Нет, я сделаю это позже самостоятельно"))
        )

        self.origin_activity_keyboard = (
            Keyboard(inline=True)
            .add(Text("EA Play"))
            .add(Text("EA Play Pro"))
            .add(Text("Не важно"))
        )

        self.select_cinema_keyboard = (
            Keyboard(inline=True)
            .add(Text("More.tv"))
            .add(Text("Start"))
            .row()
            .add(Text("IVI"))
            .add(Text("MEGOGO"))
            .row()
            .add(Text("Кинопоиск"))
        )

        self.select_vpn_keyboard = (
            Keyboard(inline=True)
            .add(Text("Windscribe VPN Pro"))
            .row()
            .add(Text("TunnelBear VPN"))
            .add(Text("IpVanish VPN"))
            .row()
            .add(Text("ZenMate Pro"))
            .add(Text("ZenMate Ultimate"))
            .row()
            .add(Text("UltraVPN"))
            .add(Text("VyprVPN"))
            .row()
            .add(Text("X-VPN"))
            .add(Text("ProtonVPN"))
        )

    def check_pay_keyboard(self,url):
        chek_pay_keyboard = (
            Keyboard(inline=True)
            .add(OpenLink(url, "Перевести"))
            .add(Text("Проверить оплату"))
        )
        return chek_pay_keyboard.get_json()


    def select_inline_keyboard(self, item_index):
        keybord = Keyboard(inline=True)
        keybord.add(Text(f"Выбрать аккаунт № {item_index}"))
        return keybord.get_json()


    def get_item_carusel(self,item_list):
        elements = []
        index = 0
        for item in item_list:
            element = TemplateElement(
                title=str(item["name"]),
                description=str(item["price"]),
                photo_id="-218478766_457239021",
                buttons=self.select_inline_keyboard(item_index=index)
            )
            print(element)
            elements.append(element)
            index += 1
        carusel = template_gen(*elements)
        return carusel