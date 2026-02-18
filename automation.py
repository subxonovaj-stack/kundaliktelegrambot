from playwright.sync_api import sync_playwright, TimeoutError

LOGIN_URL = "https://login.emaktab.uz/login"


def run_automation(parents, notify_function):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()

        for acc in parents:
            username = acc["username"]
            password = acc["password"]

            notify_function(f"🔄 Logging in: {username}")

            try:
                page.goto(LOGIN_URL)
                page.wait_for_selector("input[name='login']")
                page.fill("input[name='login']", username)
                page.fill("input[name='password']", password)
                page.click("input.login__submit.button_light-green")

                page.wait_for_selector("form[name='logout']", timeout=8000)
                page.wait_for_timeout(7000)


                notify_function(f"✅ Logged in: {username}")

                page.evaluate("document.logout.submit()")
                page.wait_for_selector("input[name='login']")

                notify_function(f"[ok] Logged out: {username}")

            except TimeoutError:
                notify_function(f"[WARNING] Error with {username}")

        browser.close()
        notify_function("🎉 Finished all accounts.")
