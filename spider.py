from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random
from datetime import datetime

KEYWORD = "智能营销机器人"
MAX_PAGE = 2
SAVE_PATH = f"./data/{KEYWORD}_raw_{datetime.now().strftime('%Y%m%d')}.xlsx"

def random_sleep(min_s=1, max_s=3):
    time.sleep(random.uniform(min_s, max_s))

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        ctx = browser.new_context(locale="zh-CN")
        page = ctx.new_page()

        page.goto("https://s.taobao.com/search?q=" + KEYWORD)
        random_sleep(2, 4)

        items = []
        for i in range(MAX_PAGE):
            print(f"采集第{i+1}页")
            cards = page.locator(".item.J_MouserOnverReq").all()
            for card in cards:
                try:
                    title = card.locator(".row-2 a").inner_text()
                    price = card.locator(".price strong").inner_text()
                    sales = card.locator(".deal-cnt").inner_text()
                    link = card.locator(".row-2 a").get_attribute("href")
                    items.append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "title": title,
                        "price": price,
                        "sales": sales,
                        "link": link
                    })
                except:
                    continue
            try:
                page.locator(".next.next-next").click()
                random_sleep(2, 4)
            except:
                break

        df = pd.DataFrame(items)
        df.to_excel(SAVE_PATH, index=False)
        print(f"保存至 {SAVE_PATH}，共{len(df)}条")
        ctx.close()
        browser.close()

if __name__ == "__main__":
    run()