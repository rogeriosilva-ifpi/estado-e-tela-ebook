import asyncio, sys
from playwright.async_api import async_playwright
src, dst = sys.argv[1], sys.argv[2]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--no-sandbox'])
        pg = await b.new_page()
        await pg.emulate_media(media='print', color_scheme='light')
        await pg.route('**/*', lambda r: r.abort() if not r.request.url.startswith('file:') else r.continue_())
        await pg.goto('file://' + src, wait_until='load', timeout=60000)
        await pg.evaluate('document.fonts.ready')
        await pg.wait_for_timeout(2000)
        await pg.pdf(path=dst, prefer_css_page_size=True, print_background=True)
        await b.close()
asyncio.run(main())
