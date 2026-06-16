import webview
from api import API

api = API()
window = webview.create_window(
    title="FNICE Launcher",
    url="ui/index.html",
    js_api=api,
    width=1280,
    height=720,
)
api.window = window
webview.start()