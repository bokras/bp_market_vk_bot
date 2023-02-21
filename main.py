from vkbottle.bot import Bot, Message
from config import vk_bot_api_key, Bot_Data
bot = Bot(token=vk_bot_api_key)
import undetected_chromedriver as uc
from functions import Func_Bot
import re
from db_control import DB
base = DB(db_file="market_db.db")
data = Bot_Data()


async def view_items(data,message):
    items = data.item_list
    index = 0
    if items != {}:
        for item in items:
            text = f"{item['name']} \n Цена: {item['price']} \n "
            await message.answer(text,keyboard=data.kayboards.select_inline_keyboard(item_index=index))
            index += 1

        await message.answer("Это все что я нашел, выберай")
    else:
        # Подходящие предложения не найдены
        await message.answer(
            "Упс, я не нашел подходящих для тебя аккаунтов, попробуй ввести название игры в формате: 'Grand Theft Auto V' либо увеличь максимальную стоимость аккаунта \n Чтобы начать заново напиши 'привет'")
        data.current_driver.close()


@bot.on.private_message(text=["Привет","привет","Старт"])
async def hi_handler(message: Message):
    global data
    await message.answer("Привет, чтобы купить аккаунт нажми кнопку ниже",keyboard=data.kayboards.main_menu_keyboard)
    if data.current_driver:
        data.current_driver.close()
        data.current_driver = None
    data.count_order.delete("start")
    data.count_order.delete("wait_user_email")
    data.count_order.delete("type")
    data.count_order.delete("game")
    data.count_order.delete("market")
    data.count_order.delete("change")
    data.count_order.delete("origin_activity")
    data.count_order.delete("uplay_activity")
    data.count_order.delete("origin_activity_date")
    data.item_list = {}
    data.attamp = 0

@bot.on.private_message(text="Купить")
async def start_buy(message: Message):
    global data
    await message.answer("Что вас интересует?", keyboard=data.kayboards.select_type_keyboard)
    data.count_order.set("start",True)
    print(data.count_order)


@bot.on.private_message(text=["Аккаунты","Ключи","Кино","Vpn"])
async def set_type(message: Message):
    global data
    if data.count_order.get("start"):

        if message.text == "Аккаунты":
            await message.answer("Какой аккаунт вы хотите?",keyboard=data.kayboards.select_market_keyboard)
            data.count_order.set("type","Account")
        elif message.text == "Ключи":
            await message.answer("Ключ в каком магазине вы хотите?",keyboard=data.kayboards.select_market_keyboard)
            data.count_order.set("type","Key")
            data.count_order.set("game","not")
            data.count_order.set("market","")
        elif message.text == "Кино":
            data.count_order.set("market", "")
            data.count_order.set("type", "Film")
            data.count_order.set("change", "unused")
            await message.answer("Выберете желаемый кинотеатр:",keyboard=data.kayboards.select_cinema_keyboard)
        elif message.text == "Vpn":
            data.count_order.set("market", "")
            data.count_order.set("type", "Vpn")
            data.count_order.set("change", "unused")
            await message.answer("Выберете желаемый Vpn-сервис:",keyboard=data.kayboards.select_vpn_keyboard)

    print(data.count_order)


@bot.on.private_message(text=["Windscribe VPN Pro","TunnelBear VPN","IpVanish VPN","ZenMate Pro","ZenMate Ultimate","UltraVPN","VyprVPN","X-VPN","ProtonVPN"])
async def select_vpn(message: Message):
    global data
    if data.count_order.get("start") and data.count_order.get("type") == "Vpn":
        data.count_order.set("game",message.text)
        data.count_order.set("market","Vpn")
        await message.answer("Введите желаемую длительность подписки (в днях):")
        data.count_order.set("origin_activity_date", "not")


@bot.on.private_message(text=["More.tv","Start","IVI","MEGOGO","Кинопоиск"])
async def select_cinema(message: Message):
    global data
    if data.count_order.get("start") and data.count_order.get("type") == "Film":
        data.count_order.set("game",message.text)
        data.count_order.set("market","Film")
        await message.answer("Введите желаемую длительность подписки (в днях):")
        data.count_order.set("origin_activity_date", "not")


@bot.on.private_message(text=["Steam","Social Club","Epic Games","Origin","Uplay","Vpn"])
async def select_market(message: Message):
    global data
    if data.count_order.get("start") == True:
        if data.count_order.get("type") == "Account":

            data.count_order.set("market",message.text)
            if data.count_order.get("market") == "Origin":
                data.count_order.set("origin_activity", "not")
                await message.answer("Выберите тип подписки origin:",keyboard=data.kayboards.origin_activity_keyboard)
                return
            data.count_order.set("game","not")
            await message.answer("Какая игра должна быть на аккаунте?",keyboard=data.kayboards.select_game_keyboard)
            print(data.count_order)

        elif data.count_order.get("type") == "Key":
            data.count_order.set("market", message.text)
            data.count_order.set("game", "not")
            await message.answer('Какую игру вы хотите?', keyboard=data.kayboards.select_game_keyboard)


@bot.on.private_message(text=["EA Play","EA Play Pro","Не важно"])
async def select_origin_activity(message:Message):
    if data.count_order.get("origin_activity") == "not":
        data.count_order.set("origin_activity",message.text)
    if data.count_order.get("origin_activity") != "Не важно":
        await message.answer("Введите желаемую длительность подписки (в днях):")
        data.count_order.set("origin_activity_date", "not")
    else:
        data.count_order.set("game", "not")
        await message.answer('Какая игра должна быть на аккаунте?', keyboard=data.kayboards.select_game_keyboard)




@bot.on.private_message(text=["GTA V", "Red Dead Redemption 2", "Ввести название вручную"])
async def choose_game(message: Message):
    global data
    if data.count_order.get("start"):
        data.count_order.set("game","not")
        if message.text == "GTA V":
            data.count_order.set("game",message.text)
            if data.count_order.get("type") == "Account":
                await message.answer(
                    "Выполнить перепривязку аккаунта на вас?\n Бот самостаятельно привяжет аккаунт к вашей почте, сменить пароль, и поможет настроить двухфакторную верификацию \n (Это дополнительная услуга +50р к стоимости аккаунта)",
                    keyboard=data.kayboards.change_user_keyboard)
                data.count_order.set("change", None)
            elif data.count_order.get("type") == "Key":
                await message.answer("Ищу для вас подходящий ключ...\n(Это может занять пару минут)")
                data.count_order.set("accaunt_selected", True)
                options = uc.ChromeOptions()
                data.current_driver = uc.Chrome(options=options)
                Func_Bot.start_ordering_processing(data,data.current_driver)
                await message.answer(data.answer_text, keyboard=data.kayboards.buy_selected_account_keyboard)
        elif message.text == "Red Dead Redemption 2":
            data.count_order.set("game",message.text)
            if data.count_order.get("type") == "Account":
                await message.answer(
                    "Выполнить перепривязку аккаунта на вас?\n Бот самостаятельно привяжет аккаунт к вашей почте, сменить пароль, и поможет настроить двухфакторную верификацию \n (Это дополнительная услуга +50р к стоимости аккаунта)",
                    keyboard=data.kayboards.change_user_keyboard)
                data.count_order.set("change", None)
            elif data.count_order.get("type") == "Key":
                await message.answer("Ищу для вас подходящий ключ...\n(Это может занять пару минут)")
                data.count_order.set("accaunt_selected", True)
                options = uc.ChromeOptions()
                data.current_driver = uc.Chrome(options=options)
                Func_Bot.start_ordering_processing(data,data.current_driver)
                await message.answer(data.answer_text,keyboard=data.kayboards.buy_selected_account_keyboard)
        else:
            data.count_order.set("game", "not")
            await message.answer('Введи название игры, в подобном формате: "Red Dead Redemption 2"')
            data.count_order.set("change", None)


@bot.on.private_message(text="Проверить оплату")
async def check_pay(message: Message):
    global data
    if data.wait_pay and data.bill != 0 and data.p2p:
        if str(data.p2p.check(bill_id= data.bill.bill_id)) == "PAID" or str(message.from_id) in data.DEBUG_IDS:
            await message.answer("Оплата прошла успешно обрабатываю ваш заказ...")
            base.set_status(data.bill.bill_id, str(data.p2p.check(bill_id= data.bill.bill_id)))
            data.wait_pay = False
            data.bill = None
            data.p2p = None
            if data.count_order.get("type") != "Key":
                Func_Bot.buy_accaunt_function(data.count_order.get("market"),data.current_driver,int(data.selected_item[0]), data.item_list,data)
                await message.answer(data.answer_text)
                if data.count_order.get("change") == True:
                    await message.answer("Выполняю перепривязку аккаунта")
                    Func_Bot.login_account_function(data.count_order.get("market"), data.current_driver,data.log_pass[0], data.log_pass[1])
                    data.count_order.set("wait_user_email",True)
                    await message.answer("Введите вашу почту:")
            else:

        else:
            await message.answer("Оплата не была проведена")
            await message.answer(f"Оплатите покупку: {data.item_list[int(data.selected_item[0])]['price']}р \n",
                                 keyboard=data.kayboards.check_pay_keyboard(url=data.bill.pay_url))


@bot.on.private_message()
async def all_message(message: Message):
    global data
    if data.count_order.get("start"):
        if data.count_order.get("game") == "not":
            data.count_order.set("game",message.text)
            if data.count_order.get("type") == "Account":
                await message.answer(
                    "Выполнить перепривязку аккаунта на вас?\n Бот самостаятельно привяжет аккаунт к вашей почте, сменит пароль, и поможет настроить двухфакторную верификацию \n (Это дополнительная услуга +50р к стоимости аккаунта)",
                    keyboard=data.kayboards.change_user_keyboard)
                data.count_order.set("change", None)
            elif data.count_order.get("type") == "Key":
                await message.answer("Ищу для вас подходящий ключ...\n(Это может занять пару минут)")
                data.count_order.set("accaunt_selected", True)
                options = uc.ChromeOptions()
                data.current_driver = uc.Chrome(options=options)
                Func_Bot.start_ordering_processing(data,data.current_driver)
                await message.answer(data.answer_text, keyboard=data.kayboards.buy_selected_account_keyboard)
# Составление заказа:
        if data.count_order.get("origin_activity_date") == "not":
            data.count_order.set("origin_activity_date", message.text)
            if data.count_order.get("type") == "Account":
                data.count_order.set("game", "not")
                await message.answer("Какая игра должна быть на аккаунте?", keyboard=data.kayboards.select_game_keyboard)


        if message.text == "Перепривязать аккаунт на меня" or message.text == "Нет, я сделаю это позже самостоятельно":
            if data.count_order.get("change") == None:
                if message.text == "Перепривязать аккаунт на меня":
                    data.count_order.set("change", True)
                else:
                    data.count_order.set("change", False)

        if data.count_order.get("change") != None and len(data.item_list) == 0:
            await message.answer("Ищу подходящие варианты для тебя (это может занять пару минут)",keyboard=data.kayboards.empty)
            options = uc.ChromeOptions()
            data.current_driver = uc.Chrome(options=options)
            Func_Bot.start_ordering_processing(data, data.current_driver)
            await view_items(data,message)

            # Выдача найденых предложений:

        if data.item_list != {}:
            if "Выбрать аккаунт №" in message.text and not data.count_order.get("accaunt_selected"):
                data.selected_item = re.findall('\d+', message.text)
                await message.answer("Собераю информацию об этом аккаунте...")
                text = Func_Bot.select_account_command(data=data,market=data.count_order.get("market"),items=data.item_list,selected=int(data.selected_item[0]),browser= data.current_driver)
                print(text)
                await message.answer(text,keyboard=data.kayboards.buy_selected_account_keyboard)
                data.count_order.set("accaunt_selected",True)

            #Выбор аккаунта

    if data.count_order.get("accaunt_selected") and len(data.item_list) != 0:
        if message.text == "купить":
            pay_info = Func_Bot.create_pay_form(data=data,message=message,base=base)
            await message.answer(pay_info[0], keyboard=data.kayboards.check_pay_keyboard(url=pay_info[1]))

        #Отмена выбора

        elif message.text == "посмотреть ещё":
            data.selected_item = None
            data.count_order.set("accaunt_selected", False)
            data.current_driver.close()
            await message.answer("Ищу подходящие варианты для тебя (это может занять пару минут)",
                                 keyboard=data.kayboards.empty)
            options = uc.ChromeOptions()
            data.current_driver = uc.Chrome(options=options)
            Func_Bot.start_ordering_processing(data, data.current_driver)
            await view_items(data, message)

    elif data.count_order.get("wait_user_email") == True:
        data.count_order.set("wait_user_email",False)




bot.run_forever()