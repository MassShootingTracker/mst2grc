import os
import datetime
import re
import praw
import praw.errors
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

    r = praw.Reddit(cfg.useragent)
    r.config.api_request_delay = cfg.api_request_delay
    r.set_oauth_app_info(cfg.client_id, cfg.client_secret, cfg.redirect_uri)
    r.refresh_access_information(cfg.refresh_token)

    for year in update_years:
        wiki = r.get_wiki_page(cfg.subreddit, cfg.wiki_pages[year])
        new_wiki = WikiYear(wiki.content_md, mst[year].list_md)
        r.edit_wiki_page(cfg.subreddit, cfg.wiki_pages[year], new_wiki.content_md, reason="Update from MST")

    # Update Sidebar
    total_shootings = sum(mst[y].total for y in mst)

    sidebar = r.get_settings(cfg.subreddit)['description']
    sidebar = re.sub(cfg.total_pattern, str(total_shootings), sidebar)
    sidebar = re.sub(cfg.current_year_pattern, str(mst[current_year].total), sidebar)
    sidebar = re.sub(cfg.days_since_pattern, str(mst[current_year].days_since_last), sidebar)

    r.edit_wiki_page(r.get_subreddit(cfg.subreddit), "config/sidebar", sidebar, reason="Update from MST")

if __name__ == "__main__":
    print(mst_to_grc())