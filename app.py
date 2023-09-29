from flask import Flask , request , render_template
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

app = Flask(__name__)


def browser_setup(browse_visually = "no"):
    """ブラウザを起動する関数"""
    #ブラウザの設定
    options = webdriver.ChromeOptions()
    if browse_visually == "no":
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    #ブラウザの起動
    browser = webdriver.Chrome(options=options , service=ChromeService(ChromeDriverManager().install()))
    browser.implicitly_wait(3)
    return browser


@app.route("/")
def index():
    # if request.method == 'POST' and request.form['start_scraping'] == "true":
    #     browse_visually = request.form['browse_visually'] 

    #     searched_url = "https://www.bookoffonline.co.jp/"
    #     driver = browser_setup(browse_visually)
    #     driver.get(searched_url)
    #     p_text = driver.find_element(By.TAG_NAME , "p").text

    #     return render_template("index.html" , p_text = p_text)

    # else:
        return render_template("index.html")

@app.route("/call_from_ajax", methods = ["POST"])
def call_from_ajax():
    if request.method == "POST":
        # ここにPythonの処理を書く
        try:
            print(f"非同期処理開始")

            searched_url = "https://www.bookoffonline.co.jp/"
            driver = browser_setup()
            driver.get(searched_url)
            time.sleep(3)
            p_text = driver.find_element(By.TAG_NAME , "p").text

            html_str = f"""
            <h3>正常に取得できました</h3>
            <div class="button019">
                <h3>p_text : {p_text}</h3>
            </div>
            <p><br></p>
        """
        except Exception as e:
            html_str = str(e)
        dict = {"answer": html_str}      # 辞書
    return json.dumps(dict)             # 辞書をJSONにして返す

# @app.route("/call_from_ajax", methods = ["POST"])
# def call_from_ajax():
#     if request.method == "POST":
#         # ここにPythonの処理を書く
#         try:
#             name = request.form["data"]
#             message = f"フン。<b style='border: 2px solid red;'>{name}</b>というのかい。贅沢な名だねぇ。<br>"
#         except Exception as e:
#             message = str(e)
#         dict = {"answer": message}      # 辞書
#     return json.dumps(dict)             # 辞書をJSONにして返す


if __name__ == "__main__":
    app.run(port=7777 , debug=True)
