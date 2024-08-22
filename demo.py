from DrissionPage import ChromiumPage, ChromiumOptions
co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9116)