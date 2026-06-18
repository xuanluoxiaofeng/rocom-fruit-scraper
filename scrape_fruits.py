import json
import requests
from bs4 import BeautifulSoup

def scrape_fruit_data():
    # 1. 目标网页URL
    url = "https://wiki.biligame.com/rocom/%E7%B2%BE%E7%81%B5%E6%9E%9C%E5%AE%9E%E5%9B%BE%E9%89%B4"
    
    # 2. 发送请求获取网页内容
    try:
        # 设置请求头，模拟浏览器访问，避免被服务器拒绝
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status() # 如果响应状态码不是200，将抛出HTTPError异常
        response.encoding = 'utf-8' # 确保使用正确的编码
        html_content = response.text
        print("网页下载成功！")
    except requests.exceptions.RequestException as e:
        print(f"错误：下载网页时出现问题 - {e}")
        return

    # 3. 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 4. 查找所有包含精灵果实信息的 div 元素
    # 根据网页结构，这些信息都在 class 为 'divsort' 的 div 中
    # 这比使用完整的XPath更稳定，因为XPath容易因页面微小改动而失效
    fruit_divs = soup.find_all('div', class_='divsort')
    
    if not fruit_divs:
        print("警告：未找到任何包含果实信息的元素。可能是网页结构已更改。")
        return

    fruits_data = []

    # 5. 遍历每个 div，提取名称和图片链接
    for div in fruit_divs:
        # 提取果实名称
        # 名称在 <p> 标签内的 <a> 标签里
        name_tag = div.find('p', class_='rocom_prop_name').find('a')
        name = name_tag.text.strip() if name_tag else None

        # 提取图片 URL
        # 图片链接在 <img> 标签的 src 属性中
        img_tag = div.find('img', class_='rocom_prop_icon')
        # 处理相对链接，将其转换为绝对链接
        image_url = img_tag.get('src') if img_tag else None
        if image_url and image_url.startswith('/'):
            image_url = "https://wiki.biligame.com" + image_url

        # 只有当名称和链接都存在时，才添加到结果列表中
        if name and image_url:
            fruits_data.append({
                "name": name,
                "image_url": image_url
            })

    # 6. 将结果保存为 JSON 文件
    with open('fruits.json', 'w', encoding='utf-8') as f:
        json.dump(fruits_data, f, ensure_ascii=False, indent=2)
    
    print(f"成功！共提取到 {len(fruits_data)} 个精灵果实的信息，已保存到 'fruits.json'。")

if __name__ == '__main__':
    scrape_fruit_data()