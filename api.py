import time
from navigator import Browser
from playwright.sync_api import sync_playwright

URL_BASE = "https://odin.sportingtech.com"
result_crashs = None


def get_crashs():
    return result_crashs


class Aviator(Browser):

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.browser = None
        self.context = None
        self.page = None
        self.s7oryo9stv = None
        self.player_link = None
        self.thread_browser = None
        self.stop_threads = False

    def auth(self):
        payload = {
            "requestBody": {
                "username": self.username,
                "email": None,
                "phone": None,
                "keepLoggedIn": None,
                "password": self.password,
                "loginType": 1,
                "fingerPrint": "41f50ea5ac05b9a804b41958b3dd5cde"
            },
            "languageId": 23,
            "device": "d"
        }
        self.headers["Origin"] = "https://estrelabet.com"
        self.headers["Referer"] = "https://estrelabet.com/"
        self.headers["finger_print"] = "41f50ea5ac05b9a804b41958b3dd5cde"

        self.response = self.send_request(
            "POST",
            f"{URL_BASE}/api/user/login",
            json=payload
        )
        if self.response:
            self.s7oryo9stv = self.response.headers["s7oryo9stv"]
            return self.response.json()
        return None

    def get_player_link(self):
        payload = {
            "requestBody":
                {
                    "gameId": "7787",
                    "channel": "web",
                    "vendorId": 78,
                    "redirectUrl": "https://estrelabet.com/ptb/games/detail/casino/normal/7787"
                },
            "identity": None,
            "device": "d",
            "languageId": 23
        }
        self.headers["Origin"] = "https://estrelabet.com"
        self.headers["Referer"] = "https://estrelabet.com/"
        self.headers["X-PGDevice"] = "d"
        self.headers["X-PGtradername"] = "536"
        self.headers["X-PGusername"] = "2022055415066"
        self.headers["s7oryO9STV"] = self.s7oryo9stv
        self.response = self.send_request(
            "POST",
            f"{URL_BASE}/api/user/casinoapi/openGame",
            json=payload
        )
        if self.response:
            self.response = self.send_request(
                "GET",
                self.response.json()["data"]["gameUrl"]
            )
            self.player_link = self.response.request.url.replace(
                "https://launch.spribegaming.com/aviator",
                "https://aviator-next.spribegaming.com/"
            )
            return self.player_link
        return None

    def start(self):
        global result_crashs
        with sync_playwright() as playwright:
            self.browser = playwright.chromium.launch(headless=True)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            self.page.goto(self.player_link)
            with self.page.expect_navigation():
                while True:
                    content = self.page.locator("app-stats-widget").text_content()
                    result_text = content.split("HISTÓRICO DE RODADAS")[0].replace("x", "").split()
                    result_crashs = {"items": [{"color": "preto" if float(i) < 2 else "verde", "value": i}
                                               for i in result_text]}
                    print(result_crashs)
                    time.sleep(1)


if __name__ == "__main__":
    aviator = Aviator("user", "senha")

    user_data = aviator.auth()
    print(user_data)

    player_link = aviator.get_player_link()
    print(player_link)

    aviator.start()
