import time
import os

from selenium.webdriver.chrome import webdriver

# 中華明國經濟部、公司資料查詢
# Chrome 瀏覽器設定
chrome_options = webdriver.ChromeOptions()
prefs = {
    "safebrowsing.enabled": True,
    "profile.default_content_settings.popups": 0,  # 禁用彈出視窗
    "profile.content_settings.exceptions.automatic_downloads.*.setting": 1  # 允許自動下載
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option('detach', True)


def download_file(driver, years, months):
    for year in years:
        for month in months:
            # print(year, month)
            select_year = Select(driver.find_element(By.ID, 'sYear'))  # 年
            select_month = Select(driver.find_element(By.ID, 'sMonth'))  # 月
            select_year.select_by_visible_text(str(year))
            select_month.select_by_visible_text(str(month))
            time.sleep(2)  # 基本等待，可依需求增加
            # # 定位並點擊下載按鈕(請自行修改定位方式)
            download_button = driver.find_element(By.NAME, "DwnldDoc")
            download_button.click()

            # --- 新增的下載完成檢查機制 ---
            max_wait = 120  # 最大等待時間(秒)
            start_time = time.time()

            while time.time() - start_time < max_wait:
                # 檢查是否有暫存檔(.crdownload 是 Chrome 的未完成下載副檔名)
                downloading_files = [f for f in os.listdir(download_dir) if f.endswith('.tmp')]

                # 檢查檔案是否正在下載
                if not downloading_files:
                    # 確認是否有新檔案出現
                    downloaded_files = [f for f in os.listdir(download_dir)]

                    if downloaded_files:
                        print("下載完成！檔案已儲存至:", os.path.join(download_dir, '{}年{}月'.format(year, month)))
                        break

                time.sleep(1)  # 每秒檢查一次
            else:
                print("錯誤：下載超時！")


if __name__ == '__main__':
    # 啟動瀏覽器
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 訪問目標網頁（三個網頁，格式一樣）
        # driver.get("https://serv.gcis.nat.gov.tw/StatisticQry/cmpy/StaticFunction1.jsp")
        # driver.get("https://serv.gcis.nat.gov.tw/StatisticQry/cmpy/StaticFunction2.jsp")
        driver.get("https://serv.gcis.nat.gov.tw/StatisticQry/cmpy/StaticFunction3.jsp")
        print(driver.title)

        # 109~113年 1~2月
        years = list(range(109, 114))
        months = list(range(1, 13))
        download_file(driver, years, months)

        # 104年 1~2月
        months = list(range(1, 3))
        years = list(range(114, 115))
        download_file(driver, years, months)
    finally:
        # 關閉瀏覽器
        driver.quit()
