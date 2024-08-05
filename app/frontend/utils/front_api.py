from taipy import Gui
import taipy.gui.builder as tgb

# Add a navbar to switch from one page to the other
with tgb.Page() as root_page:
    tgb.navbar()
    tgb.text("# Multi-page application", mode="md")

with tgb.Page() as page_1:
    tgb.text("## This is page 1", mode="md")
with tgb.Page() as page_2:
    tgb.text("## This is page 2", mode="md")

pages = {
    "/": root_page,
    "page1": page_1,
    "page2": page_2
}
Gui(pages=pages).run()