from config import qiwi_api_key
from config import lolz_url
from config import keys_url
from config import lolz_login
from config import lolz_password
from config import qiwi_number
from config import qiwi_password
from config import sikret_word
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from pyqiwip2p import QiwiP2P
import traceback
from threading import Thread
import time




def check_exists_by_xpath(browser,xpath):
    try:
        browser.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True



def check_exists_by_class(browser,class_name):
    try:
        browser.find_element(By.CLASS_NAME,class_name)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_selector(browser,selector):
    try:
        browser.find_element(By.CSS_SELECTOR,selector)
    except NoSuchElementException:
        return False
    return True



def Login_on_lolz(driver):
    try:
        driver.get(lolz_url+"login/")
        if check_exists_by_xpath(driver,"/html/body/div[2]/div/div/div/form/div[1]/div"):
            driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/form/input[1]").send_keys(lolz_login)
            driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/form/div[3]/input").send_keys(lolz_password)
            driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/form/div[5]/input").click()
            time.sleep(1)
    except:
        Login_on_lolz(driver)


def search_accaunt(data, driver,market,game,change,podpiska,long):
    try:
        url_response = ""
        if market == "steam":
            url_response = f"https://lzt.market/steam/?pmin=10&title={game}&mm_ban=nomatter&order_by=price_to_up"
        elif market == "origin":
            if podpiska != "Не важно":
                url_response = f"https://lzt.market/origin/?pmin=10&title={game}&subscription={podpiska.replace(' ', '+')}&subscription_length={long}&xbox_connected=no&order_by=price_to_up"
            else:
                url_response = f"https://lzt.market/origin/?pmin=10&title={game}&xbox_connected=no&order_by=price_to_up"
        elif market == "epicgames":
            url_response = f"https://lzt.market/epicgames/?pmin=10&title={game}&change_email=yes&order_by=price_to_up"
        elif market == "socialclub":
            url_response = f"https://lzt.market/socialclub/?{game}=on&order_by=price_to_up"
        elif market == "uplay":
            url_response = f"https://lzt.market/uplay/?pmin=10&title={game}&email_type[]=autoreg&order_by=price_to_up"
        elif game == "More.tv":
            url_response = f"https://lzt.market/cinema/?pmin=10&service_id[]=moretv&subscription_length={long}&order_by=price_to_up"
        elif game == "IVI":
            url_response = f"https://lzt.market/cinema/?pmin=10&service_id[]=ivi&subscription_length={long}&order_by=price_to_up"
        elif game == "Start":
            url_response = f"https://lzt.market/cinema/?pmin=10&service_id[]=start&subscription_length={long}&order_by=price_to_up"
        elif game == "MEGOGO":
            url_response = f"https://lzt.market/cinema/?pmin=10&service_id[]=megogo&subscription_length={long}&order_by=price_to_up"
        elif game == "Кинопоиск":
            url_response = f"https://lzt.market/cinema/?pmin=10&service_id[]=kinopoisk&subscription_length={long}&order_by=price_to_up"
        elif game == "Windscribe VPN Pro":
            url_response = f"https://lzt.market/vpn/?pmin=10&service_id[]=windscribeVPN&subscription_length={long}&order_by=price_to_up"
        elif game == "TunnelBear VPN":
            url_response = f"https://lzt.market/vpn/?pmin=10&service_id[]=tunnelbearVPN&subscription_length={long}&order_by=price_to_up"
        elif game == "IpVanish VPN":
            url_response = f"https://lzt.market/vpn/?pmin=10&service_id[]=vanishVPN&subscription_length={long}&order_by=price_to_up"
        elif game == "ZenMate Pro":
            url_response = f"https://lzt.market/vpn/?pmin=10&service_id[]=zenmateVPN&subscription_length={long}&order_by=price_to_up"
        elif game == "ZenMate Ultimate":
            url_response = f"https://lzt.market/vpn/?pmin=10&service_id[]=zenmateVPNUltimate&subscription_length={long}&order_by=price_to_up"
        elif game == "UltraVPN":
            url_response = f"https://lzt.market/vpn/?pmin=10&service_id[]=ultraVPN&subscription_length={long}&order_by=price_to_up"
        elif game == "VyprVPN":
            url_response = f"https://lzt.market/vpn/?pmin=10&service_id[]=vyprnVPN&subscription_length={long}&order_by=price_to_up"
        elif game == "X-VPN":
            url_response = f"https://lzt.market/vpn/?pmin=10&service_id[]=xVPN&subscription_length={long}&order_by=price_to_up"
        elif game == "ProtonVPN":
            url_response = f"https://lzt.market/vpn/?pmin=10&service_id[]=protonVPN&subscription_length={long}&order_by=price_to_up"


        driver.get(url_response)
        time.sleep(1)
        driver.find_element(By.ID,"XenForo").send_keys(Keys.PAGE_DOWN)
        page = driver.page_source
        if check_exists_by_xpath(driver,'/html/body/div[2]/div/div/div/div/div/div[9]/div[2]/form/p[@class="marketIndexView--nothingFound marketCloudContainer   muted"]'):
            data.item_list = {}
            return

        soup = BeautifulSoup(page,"lxml")
        items = soup.find("div",class_="marketMainContainer").find("div",class_="marketIndex--itemsContainer MarketItems marketIndex--Items").find("form",class_="InlineModForm section").find_all("li")
        print(len(items))
        goods = []
        for item in items:
            text = ""
            link = ""
            price = ""
            true_price = 0

            name = item.find("div", class_="marketIndexItem--topContainer").find("h4").find("a").text
            link = f'https://lzt.market/{item.find("div", class_="marketIndexItem--topContainer").find("h4").find("a").get("href")}'
            price = int(item.find("div", class_="rightCol").find("div").find("span").text)
            text = f"{name} \n"




            true_price = price
            price = true_price + round((true_price/100 * 25))
            if change:
                price += 50
            good = {
                "name": text,
                "url": link,
                "price": price,
                "true_price": true_price
            }
            goods.append(good)
        data.item_list = goods
    except:
        search_accaunt(data,driver,market,game,change,podpiska,long)


def search_key(data,driver,game,market):
    try:
        driver.get(keys_url)
        search_btn = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#games > div.row.mt-3.mb-2 > div.col-12.col-lg-auto > div')))
        search_btn.click()
        market_btn = None
        print(market)

        if market == "steam":
            market_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#games > div.row.mt-3.index-games-list-container > div.catalog-filter.d-none.d-flex > div:nth-child(3) > div > div.catalog-filter-selector_list > div:nth-child(1)')))
        elif market == "origin":
            market_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#games > div.row.mt-3.index-games-list-container > div.catalog-filter.d-none.d-flex > div:nth-child(3) > div > div.catalog-filter-selector_list > div:nth-child(2)')))
        elif market == "uplay":
            market_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#games > div.row.mt-3.index-games-list-container > div.catalog-filter.d-none.d-flex > div:nth-child(3) > div > div.catalog-filter-selector_list > div:nth-child(3)')))
        elif market == "socialclub":
            market_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#games > div.row.mt-3.index-games-list-container > div.catalog-filter.d-none.d-flex > div:nth-child(3) > div > div.catalog-filter-selector_list > div:nth-child(5)')))
        elif market == "epicgames":
            market_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#games > div.row.mt-3.index-games-list-container > div.catalog-filter.d-none.d-flex > div:nth-child(3) > div > div.catalog-filter-selector_list > div:nth-child(7)')))

        market_btn.click()
        game_name_input = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#games > div.row.mt-3.index-games-list-container > div.catalog-filter.d-none.d-flex > div:nth-child(2) > div > div.form-group.mb-0 > input')))
        game_name_input.send_keys(game)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source,"lxml")
        table = soup.find("div", class_="tab-pane fade show active").find("div", class_="row mt-3 index-games-list-container").find("div", class_="col-6 col-md-4 col-lg-3 col-xl-2")

        product_card = table.find("a", class_="product-card")
        print(product_card.get("title"))

    except:
        traceback.print_exc()
        search_key(data,driver,game,market)



def one_step_order_processing(data, driver,type,game,change,market,podpiska,long):
    if type != "Key":
        Login_on_lolz(driver)
        search_accaunt(data, driver,market,game,change,podpiska,long)
        print("items")
    else:
        search_key(data,driver,game,market)



def select_account(data,market,items,index,driver):
    try:
        print("попытка: ",data.attamp)
        message_text = f""
        acc_url = items[index]['url']
        print(acc_url, " url")
        driver.get(acc_url)
        print(market)
        soup = BeautifulSoup(driver.page_source, "lxml")

        if "Steam" in market:
            print("process")
            info_form = soup.find("div", class_="marketItemView--mainInfoContainer")
            name = items[index]["name"]
            price = items[index]["price"]
            balance_on_account = info_form.find_all("div", class_="marketItemView--counters")[0].find("div", class_="counter").find("div", class_="label").find("span", class_="Tooltip").text
            friends_on_account = info_form.find_all("div", class_="marketItemView--counters")[2].find_all("div", class_="counter")[1].find("div", class_="label").text
            games_on_account = info_form.find_all("div", class_="marketItemView--counters")[2].find_all("div", class_="counter")[3].find("div", class_="label").text
            country = info_form.find_all("div", class_="marketItemView--counters")[2].find_all("div", class_="counter")[4].find("div", class_="label").text
            last_activity = info_form.find_all("div", class_="marketItemView--counters")[1].find_all("div", class_="counter")[0].find("div", class_="label").find("span", class_="DateTime").text
            parsed_info = soup.find("div", class_="marketContainer marketItemView--Container").find("div", class_="marketItemView--AfterTabs").find("div", class_="marketItemView--ParsedInfo")
            scroll = parsed_info.find("div", class_="marketItemView--gamesContainer").find("div", class_= "scroll-wrapper MarketScrollBar scrollbar-macosx scrollbar-dynamic").find("div",class_="MarketScrollBar scrollbar-macosx scrollbar-dynamic scroll-content")
            game_table = scroll.find("ul")
            game_items = game_table.find_all("li")
            game_list = ""
            for game_item in game_items:
                name = game_item.find("div",class_="bottomContainer").find("div",class_="bold gameTitle").find("span").text
                print(name)
                game_list = game_list + "\n" + f"- {name}"
            print(game_list)
            message_text = f"{name} \n Цена: {price} \n Баланс аккаунта: {balance_on_account} \n Присутствующие игры: \n {game_list} \n и другие \n Колличество игр на аккаунте: {games_on_account} \n Количество друзей: {friends_on_account} \n Страна: {country} \n Последняя активность: {last_activity}"

        elif "Social Club" in market:
            info_form = soup.find("div", class_="marketItemView--mainInfoContainer")
            name = items[index]["name"]
            price = items[index]["price"]
            local_money = info_form.find_all("div", class_="counter")[2].find("div", class_="label").text
            bank_money = info_form.find_all("div", class_="counter")[3].find("div", class_="label").text
            last_activ = info_form.find_all("div", class_="counter")[0].find("div", class_="label").find("span", class_="DateTime").text
            acc_lvl = info_form.find_all("div", class_="counter")[1].find("div", class_="label").text
            message_text = f"{name} \n Цена: {price} \n Налчные денги игрока: {local_money} \n Деньги в банке: {bank_money} \n Уровень GTA V: {acc_lvl} \n Последняя активность аккаунта: {last_activ} "


        elif "Epic Games" in market:
            name = items[index]["name"]
            price = items[index]["price"]
            game_info_form = soup.find("div", class_="marketContainer marketItemView--Container").find("div", class_="marketItemView--AfterTabs").find("div", class_="marketItemView--ParsedInfo").find("div", class_="marketItemView--mainInfoContainer").find("div", class_="fortnitePastSeasonsSection mn-0-0-30").find("div", class_= "transactionList").find("div",class_="scroll-wrapper FortnitePastSeasons scrollbar-macosx scrollbar-dynamic").find("div",class_="FortnitePastSeasons scrollbar-macosx scrollbar-dynamic scroll-content scroll-scrolly_visible").find("table", class_="dataTable").find("tbody")
            info_form = soup.find("div", class_="marketContainer marketItemView--Container").find("div", class_="marketItemView--AfterTabs").find("div", class_="marketItemView--ParsedInfo").find("div", class_="marketItemView--mainInfoContainer").find("div",class_="marketItemView--counters")
            game_list = ""
            table_items = game_info_form.find_all("tr", class_="dataRow")

            for item in table_items:
                game_name = item.find_all("td")[0].text
                game_list = game_list + str(game_name + "\n")

            count_of_games = info_form.find_all("div",class_="counter")[0].find("div",class_="label").text
            mail_domian = info_form.find_all("div",class_="counter")[4].find("div",class_="label").text
            contry = info_form.find_all("div",class_="counter")[3].find("div",class_="label").text
            message_text = f"{name} \n Цена: {price} \n Игры: \n {game_list} \n Общее количество игр: {count_of_games} \n Почта: {mail_domian} \n Страна: {contry}"


        elif "Origin" in market:
            name = items[index]["name"]
            price = items[index]["price"]
            info_form = soup.find("div", class_="marketContainer marketItemView--Container").find("div",class_="marketItemView--AfterTabs").find("div", class_="marketItemView--ParsedInfo").find("div", class_="marketItemView--mainInfoContainer").find("div", class_="marketItemView--counters")
            if check_exists_by_xpath(driver,'//*[@id="content"]/div/div/div/div/div[3]/div/div/div[2]/div/div[1]/div[1]/span'):
                xbox_connection = info_form.find_all("div",class_="counter")[0].find("div",class_="label").find('span',class_="bold redc").text
            else:
                xbox_connection = info_form.find_all("div",class_="counter")[0].find("div",class_="label").text
            podpiska = info_form.find_all("div",class_="counter")[1].find("div",class_="label").text.split()[0]
            podpiska_do = "Неизвестно"
            contry = ""
            email_domian = ""
            game_list = "Не удалось получить список"
            print(podpiska)
            if not "Нет" in podpiska:
                podpiska_do = info_form.find("div",class_="counter ea_subscription_end_date").find("div",class_="label").find("abbr",class_="DateTime").text
            contry = info_form.find_all("div",class_="counter")[2].find("div", class_="label").text
            email_domian = info_form.find_all("div",class_="counter")[3].find("div", class_="label").text
            parsed_info = soup.find("div", class_="marketContainer marketItemView--Container").find("div",class_="marketItemView--AfterTabs").find("div", class_="marketItemView--ParsedInfo")
            if check_exists_by_class(driver,"marketItemView--gamesContainer") == True:
                scroll = parsed_info.find("div", class_="marketItemView--gamesContainer")
                game_list = ""
                game_table = scroll.find("ul")
                game_items = game_table.find_all("li")
                for game_item in game_items:
                    name = game_item.find("div", class_="bottomContainer").find("div", class_="bold gameTitle").text
                    print(name)
                    game_list = game_list + "\n" + f"- {name}"
            message_text = f"{name} \n Цена: {price} \n Игры:\n {game_list} \n \n Активная привязка к xbox: {xbox_connection}\n Тип подписки: {podpiska}\n Длится до: {podpiska_do}\n Почтовый домен: {email_domian}\n Страна регистрации: {contry}"

        elif "Uplay" in market:
            info_form = soup.find("div", class_="marketContainer marketItemView--Container").find("div",class_="marketItemView--AfterTabs").find("div", class_="marketItemView--ParsedInfo").find("div",class_="marketItemView--mainInfoContainer").find("div",class_="marketItemView--counters")
            name = items[index]["name"]
            price = items[index]["price"]
            game_list = "Не удалось получить список"
            country = info_form.find_all("div",class_="counter")[0].find("div",class_="label").text
            email_domian = info_form.find_all("div",class_="counter")[3].find("div",class_="label").text
            last_activ = info_form.find_all("div",class_="counter")[1].find("div",class_="label").find("span",class_="DateTime").text
            parsed_info = soup.find("div", class_="marketContainer marketItemView--Container").find("div",class_="marketItemView--AfterTabs").find("div", class_="marketItemView--ParsedInfo")
            if check_exists_by_xpath(driver, '//*[@id="content"]/div/div/div/div/div[3]/div/div/div[1]') == True:
                scroll = parsed_info.find("div", class_="marketItemView--gamesContainer")
                game_list = ""
                game_table = scroll.find("ul")
                game_items = game_table.find_all("li")
                for game_item in game_items:
                    name = game_item.find("div", class_="bottomContainer").find("div").text
                    print(name)
                    game_list = game_list + "\n" + f"- {name}"
                message_text = f"{name} \nЦена: {price}р \nИгры:\n {game_list}\n Последняя активность: {last_activ}\n Страна регистрации: {country}\nПочтовый домен: {email_domian}"
        elif market in ["Film","Vpn"]:
            name = items[index]["name"]
            price = items[index]["price"]
            cinema_name = driver.find_element(By.CSS_SELECTOR,"#content > div > div > div > div > div.marketContainer.marketItemView--Container > div > div > div > div.counter.region > div.label > span").text
            auto_pay = driver.find_element(By.CSS_SELECTOR,"#content > div > div > div > div > div.marketContainer.marketItemView--Container > div > div > div > div.counter.renewal > div.label > span").text
            ending = driver.find_element(By.CSS_SELECTOR,"#content > div > div > div > div > div.marketContainer.marketItemView--Container > div > div > div > div.counter.expire_date > div.label > span").text
            message_text = f"{name}\n {price}p\n Сервис: {cinema_name}\nТекущая подписка длится до: {ending}\nАвтопродление подписки: {auto_pay}"




        print(message_text," text")
        data.answer_text = message_text
    except Exception as ex:
        traceback.print_exc()
        data.attamp += 1
        if data.attamp <= 10:
            select_account(data, market, items, index, driver)
        else:
            data.answer_text = "Неудалось собрать информацию о даннам аккаунте, выберите другой"
            data.attamp = 0
            return


def add_money_to_lolz(driver,item_list,sindex):
    try:
        money = int(item_list[sindex]["true_price"])
        driver.get(lolz_url)
        print(money)
        add_to_balnce_btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#content > div > div > aside > div > div > div:nth-child(3) > div > div.marketSidebarMenu.bordered-top > a:nth-child(2)")))
        add_to_balnce_btn.click()
        money_input = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#AmountInput")))
        money_input.send_keys(money)
        qiwi_btn = driver.find_element(By.CSS_SELECTOR,"body > div.modal.fade.in > div > div > div > form > div.marketRefillBalance-Body > div:nth-child(2) > div.methods.SelectMethod > div.Method.method.Lava_Qiwi.qiwi.selected")
        qiwi_btn.click()
        pay_btn = driver.find_element(By.CSS_SELECTOR,"body > div.modal.fade.in > div > div > div > form > div:nth-child(3) > input")
        pay_btn.click()
        lava_qiwi_btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#root > div > div > div.InvoicePage_container__\+Ah1X > div > div.InvoicePage_payment__NQ9xT > div > div.Services_services__2zqs2 > div > div:nth-child(2)")))
        lava_qiwi_btn.click()
        number_input = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#root > div > div > div.InvoicePage_container__\+Ah1X > div > div.InvoicePage_payment__NQ9xT > div > div.container__input > div > input")))
        number_input.send_keys(qiwi_number)
        pay_with_qiwi_btn = driver.find_element(By.CSS_SELECTOR,"#root > div > div > div.InvoicePage_container__\+Ah1X > div > div.InvoicePage_payment__NQ9xT > div > button")
        pay_with_qiwi_btn.click()
        qiwi_password_input = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#PasscodeForm-PasswordInput")))
        qiwi_password_input.send_keys(qiwi_password)
        login_qiwi_btn = driver.find_element(By.CSS_SELECTOR,"#PasscodeForm-Submit")
        login_qiwi_btn.click()
        time.sleep(5)
        time.sleep(30)
    except:
        add_money_to_lolz(driver,item_list,sindex)


def buy_accaunt(market, driver, sindex, item_list,data):
    try:
        buy_btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#content > div > div > div > div > div.market--titleBar.market--spec--titleBar > div.AfterPurchaseContainer > div.mn-30-0-0.buttons > a.button.primary.InlinePurchase.OverlayTrigger.DisableButton.marketViewItem--buyButton")))
        buy_btn.click()
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        add_money_to_lolz(driver,item_list,sindex)
        driver.execute_script("window.close('');")
        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()
        buy_btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#content > div > div > div > div > div.market--titleBar.market--spec--titleBar > div.AfterPurchaseContainer > div.mn-30-0-0.buttons > a.button.primary.InlinePurchase.OverlayTrigger.DisableButton.marketViewItem--buyButton")))
        buy_btn.click()
        sickret_word_input = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,"secret_answer")))
        sickret_word_input.send_keys(sikret_word)
        confirm_buy_btn = driver.find_element(By.CSS_SELECTOR,"body > div.modal.fade.in > div > div > form > div.SA--bottom > input.button.primary.mn-15-0-0.OverlayTrigger")
        confirm_buy_btn.click()
        driver.get("https://lzt.market/46217655/")
        log_pass_out = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#loginData--login_and_password")))
        data.log_pass = log_pass_out.text.split(":")
    except:
        traceback.print_exc()
        buy_accaunt(market,driver,sindex,item_list,data)


def login_account_social_club(driver,login,password):
    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://signin.rockstargames.com/signin/user-form?cid=socialclub")
        login_input = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div[1]/div[2]/div[1]/div/div/form/fieldset[1]/span/input[@name="email"]')))
        password_input = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div[1]/div[2]/div[1]/div/div/form/fieldset[2]/span[1]/span/input[@name="password"]')))
        login_btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#app-page > div:nth-child(2) > div:nth-child(1) > div > div > form > fieldset.loginform__submitField__NdeFI > div > button")))
        login_input.send_keys(login)
        password_input.send_keys(password)
        login_btn.click()
        time.sleep(10)
        if check_exists_by_xpath(driver,'//*[@id="textInput__176"]'):
            driver.switch_to.window(driver.window_handles[0])
            get_code_btn = driver.find_element(By.CSS_SELECTOR,"")
            get_code_btn.click()
            code_label = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR," ")))
            code = code_label.text
            driver.switch_to.window(driver.window_handles[1])
            driver.find_element(By.XPATH,'//*[@id="textInput__176"]').send_keys(code)
            driver.find_element(By.CSS_SELECTOR,"#app-page > div:nth-child(2) > div > div > div:nth-child(5) > div > button").click()
    except:
        traceback.print_exc()


class Func_Bot():
    def start_ordering_processing(data,driver):
        tipe = data.count_order.get("type")
        game = str(data.count_order.get("game"))
        market = str(data.count_order.get("market")).replace(" ","").lower()
        podpiska = data.count_order.get("origin_activity")
        long = data.count_order.get("origin_activity_date")


        if market == "epicgames" and game == "GTA V":
            game = "Grand Theft Auto V"
        elif market == "socialclub" and game == "GTA V":
            game = "gtav"
        elif market in ["socialclub",None] and game == "Red Dead Redemption 2":
            game = "rdr2"
        elif tipe == "Key" and game == "GTA V":
            game = "Grand Theft Auto V"
        change = data.count_order.get("change")
        process = Thread(target=one_step_order_processing,args=(data, driver,tipe,game,change,market,podpiska,long))
        process.start()
        process.join()


    def select_account_command(data,market,items,selected, browser):
        process = Thread(target=select_account,args=(data,market,items,selected,browser))
        process.start()
        process.join()
        text = data.answer_text
        print(text," returned text")
        return text


    def create_pay_form(data,message,base):
        if data.selected_item != None:
            item = data.item_list[int(data.selected_item[0])]
            p2p = QiwiP2P(auth_key=qiwi_api_key)
            comment = str(message.from_id) + str(data.count_order['type']) + str(data.count_order['market']) + str(data.count_order['game']) + "_" + str(time.time())
            bill = p2p.bill(amount=item['price'], lifetime=15, comment=comment)
            base.add_chek(user_id=int(message.from_id), price=int(item["price"]), accaunt_url=item["url"],market=data.count_order['market'], bill_id=bill.bill_id)
            data.wait_pay = True
            data.bill = bill
            data.p2p = p2p
            print(bill.pay_url)
            text = f"Ваш заказ оформлен, для оплаты товара вам нужно перевестм на наш счет qiwi {item['price']}р \n После чего вы получите свой товар"
            pay_url = bill.pay_url
            return [text,pay_url]




    def buy_accaunt_function(market, driver, sindex, item_list,data):
        process = Thread(target=buy_accaunt,args=(market, driver, sindex, item_list,data))
        process.start()
        process.join()
        if len(data.log_pass) > 0:
            data.answer_text = f"Данные вашей учетной записи:\nЛогин: {data.log_pass[0]} \nПароль: {data.log_pass[1]}"


    def login_account_function(market,driver,login,password):
        print(market)
        if market == "Social Club":
            process = Thread(target=login_account_social_club,args=(driver,login,password))
            process.start()
            process.join()
            return

