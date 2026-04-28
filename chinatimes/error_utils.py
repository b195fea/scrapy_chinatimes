"""
爬蟲錯誤頁面保存工具
發生異常時自動保存當前頁面 HTML，便於後續除錯與重跑
"""
import os
from datetime import datetime


def save_error_page(spider_name, url, html_content, error_msg,
                    output_dir='error_pages', extra_info=None):
    """
    保存錯誤頁面 HTML

    :param spider_name: 爬蟲名稱（用於檔名前綴）
    :param url: 當前頁面 URL
    :param html_content: 頁面 HTML 內容（response.text 或 driver.page_source）
    :param error_msg: 錯誤訊息
    :param output_dir: 輸出目錄，預設 'error_pages'
    :param extra_info: 額外資訊字典（可選）
    :return: 保存的檔案路徑
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_url = url.replace('https://', '').replace('http://', '').replace('/', '_').replace('?', '_').replace('&', '_')[:80]
    filename = f"{spider_name}_{timestamp}_{safe_url}.html"

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    meta_lines = [
        f"<!-- Spider: {spider_name} -->",
        f"<!-- URL: {url} -->",
        f"<!-- Error: {error_msg} -->",
        f"<!-- Time: {timestamp} -->",
    ]
    if extra_info:
        for key, value in extra_info.items():
            meta_lines.append(f"<!-- {key}: {value} -->")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(meta_lines) + '\n')
        f.write(html_content)

    print(f"[ERROR] 頁面已保存: {filepath}")
    return filepath
