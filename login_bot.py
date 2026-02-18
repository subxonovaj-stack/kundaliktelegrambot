<<<<<<< HEAD
from playwright.sync_api import sync_playwright, TimeoutError
from accounts import PARENTS

LOGIN_URL = "https://login.emaktab.uz/login"


def run_login_cycle(bot, chat_id):


    with sync_playwright() as p:

        # Headless but disguised as real browser
        browser = p.firefox.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0",
            viewport={"width": 1280, "height": 800}
        )

        page = context.new_page()

        for acc in PARENTS:
            username = acc["username"]
            password = acc["password"]

            bot.send_message(chat_id, f"Logging in: {username}")


            page.goto(LOGIN_URL)

            # Click "Kirish" if present
            try:
                kirish = page.locator("a:has-text('Kirish')")
                if kirish.is_visible():
                    kirish.click()
                    page.wait_for_timeout(1000)
            except:
                pass

            # Wait for login form
            try:
                page.wait_for_selector("input[name='login']", timeout=15000)
            except TimeoutError:
                browser.close()
                return "captcha"

            page.fill("input[name='login']", username)
            page.fill("input[name='password']", password)

            # Click login button
            try:
                page.locator("input.login__submit.button_light-green").click(timeout=3000)
            except:
                page.evaluate("""
                    document.querySelector("input.login__submit.button_light-green").click()
                """)
                page.wait_for_timeout(1500)

            # If captcha appears → stop immediately
            if page.query_selector("img.captcha"):
                browser.close()
                return "captcha"

            # Wait for successful login
            try:
                page.wait_for_selector("form[name='logout']", timeout=10000)
            except TimeoutError:
                browser.close()
                return "captcha"

            bot.send_message(f"Logged in: {username}")

            # Small delay to simulate real user activity
            page.wait_for_timeout(5000)

            # Logout
            try:
                page.evaluate("document.logout.submit()")
            except:
                try:
                    page.locator("a:has-text('Chiqish')").click()
                except:
                    browser.close()
                    return "captcha"

            page.wait_for_selector("input[name='login']")
            bot.send_message(chat_id, f"Logged out: {username}")


        browser.close()
        return "finished"
=======
from playwright.sync_api import sync_playwright, TimeoutError
from accounts import PARENTS

LOGIN_URL = "https://login.emaktab.uz/login"


def run_login_cycle(bot, chat_id):


    with sync_playwright() as p:

        # Headless but disguised as real browser
        browser = p.firefox.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0",
            viewport={"width": 1280, "height": 800}
        )

        page = context.new_page()

        for acc in PARENTS:
            username = acc["username"]
            password = acc["password"]

            bot.send_message(chat_id, f"Logging in: {username}")


            page.goto(LOGIN_URL)

            # Click "Kirish" if present
            try:
                kirish = page.locator("a:has-text('Kirish')")
                if kirish.is_visible():
                    kirish.click()
                    page.wait_for_timeout(1000)
            except:
                pass

            # Wait for login form
            try:
                page.wait_for_selector("input[name='login']", timeout=15000)
            except TimeoutError:
                browser.close()
                return "captcha"

            page.fill("input[name='login']", username)
            page.fill("input[name='password']", password)

            # Click login button
            try:
                page.locator("input.login__submit.button_light-green").click(timeout=3000)
            except:
                page.evaluate("""
                    document.querySelector("input.login__submit.button_light-green").click()
                """)
                page.wait_for_timeout(1500)

            # If captcha appears → stop immediately
            if page.query_selector("img.captcha"):
                browser.close()
                return "captcha"

            # Wait for successful login
            try:
                page.wait_for_selector("form[name='logout']", timeout=10000)
            except TimeoutError:
                browser.close()
                return "captcha"

            bot.send_message(f"Logged in: {username}")

            # Small delay to simulate real user activity
            page.wait_for_timeout(5000)

            # Logout
            try:
                page.evaluate("document.logout.submit()")
            except:
                try:
                    page.locator("a:has-text('Chiqish')").click()
                except:
                    browser.close()
                    return "captcha"

            page.wait_for_selector("input[name='login']")
            bot.send_message(chat_id, f"Logged out: {username}")


        browser.close()
        return "finished"
>>>>>>> 2508e66 (update bot to webhook version)
