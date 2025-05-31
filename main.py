from time import sleep
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

import webbrowser
import shutil

class UrlOpener:
    def __init__(self):
        # Try to use default browser first
        try:
            self.browser = webbrowser.get()
        except:
            # Fallback to Firefox if default is not available
            if shutil.which("firefox"):
                webbrowser.register("firefox", None, webbrowser.BackgroundBrowser(shutil.which("firefox")))
                self.browser = webbrowser.get("firefox")
            else:
                raise EnvironmentError("No browser found (default or Firefox)")

    def open(self, url):
        url = self.complete_url(url)
        self.browser.open(url)

    def complete_url(self, url):
        if url == None:
            return "www.google.com"
        if "https://www." in url:
            pass
        elif "www." in url:
            url = "https://" + url
        else:
            url = "https://www." + url
        if len(url.split(".")) == 2:
            url += ".com"
        return url

url_opener = UrlOpener()

class DemoExtension(Extension):
    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        input_url = event.get_argument()
        completed_url = url_opener.complete_url(input_url)

        url = [
            ExtensionResultItem(
                icon='images/icon.png',
                name= f"Open in browser",
                description=f"Open URL {completed_url} in browser",
                on_enter=ExtensionCustomAction({"url": input_url}, keep_app_open=False)
            )
        ]
        return RenderResultListAction(url)

class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        url_opener.open(data["url"])
        return RenderResultListAction([])  # Hide window after opening

        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=data["url"],
                                                           on_enter=url_opener.open(data["url"])
                                                          )])

if __name__ == '__main__':
    DemoExtension().run()
