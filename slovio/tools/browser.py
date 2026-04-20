from playwright.async_api import async_playwright
import base64

class BrowserController:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    async def init(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()

    async def navigate(self, url):
        await self.page.goto(url)
        return f"Navigated to {url}"

    async def click(self, selector):
        await self.page.click(selector)
        return f"Clicked {selector}"

    async def type_into(self, selector, text):
        await self.page.fill(selector, text)
        return f"Typed {text} into {selector}"

    async def get_text(self, selector):
        return await self.page.inner_text(selector)

    async def get_page_content(self):
        return await self.page.content()

    async def screenshot(self):
        img_bytes = await self.page.screenshot()
        return base64.b64encode(img_bytes).decode("utf-8")

    async def execute_js(self, script):
        return await self.page.evaluate(script)

    async def wait_for(self, selector, timeout=5000):
        await self.page.wait_for_selector(selector, timeout=timeout)
        return f"Found {selector}"

    async def new_tab(self, url):
        self.page = await self.browser.new_page()
        await self.page.goto(url)
        return f"Opened new tab to {url}"

    async def close_tab(self):
        await self.page.close()
        pages = self.browser.contexts[0].pages
        if pages:
            self.page = pages[-1]
        return "Tab closed"

    async def scroll_to(self, selector):
        await self.page.evaluate(f"document.querySelector('{selector}').scrollIntoView()")
        return f"Scrolled to {selector}"
