import os
import datetime
import re
import praw
from .objects import Config, MSTYear, WikiYear


def mst_to_grc(update_year="all", cfg_file=None):

    if cfg_file is not None:
        cfg = Config(cfg_file)
    else:
        here = os.path.abspath(os.path.dirname(__file__))
        cfg = Config(os.path.join(here, os.path.pardir, "config.json"))

    current_year = str(datetime.date.today().year)
    MSTYear.set_fmts(cfg.title_md, cfg.url_md)

    # Load data from MST
    mst = {}
    for y in cfg.google_docs:
        mst[y] = MSTYear(y, cfg.google_docs[y])

    # Load markdown for years
    update_years = [y for y in cfg.wiki_pages] if update_year == 'all' else [update_year]

    r = praw.Reddit(client_id = cfg.client_id,
                    client_secret = cfg.client_secret,
                    refresh_token = cfg.refresh_token,
                    user_agent = cfg.useragent)

    for year in update_years:
        wiki = r.subreddit(cfg.subreddit).wiki[cfg.wiki_pages[year]]
        new_wiki = WikiYear(wiki.content_md, mst[year].list_md)
        wiki.edit(new_wiki.content_md, reason="Update from MST")

    # Update Sidebar
    total_shootings = sum(mst[y].total for y in mst)

    sidebar = r.subreddit(cfg.subreddit).wiki['config/sidebar']

    sidebar_md = sidebar.content_md
    sidebar_md = re.sub(cfg.total_pattern, str(total_shootings), sidebar_md)
    sidebar_md = re.sub(cfg.current_year_pattern, str(mst[current_year].total), sidebar_md)
    sidebar_md = re.sub(cfg.days_since_pattern, str(mst[current_year].days_since_last), sidebar_md)

    sidebar.edit(sidebar_md, reason="Update from MST")

if __name__ == "__main__":
    print(mst_to_grc())
