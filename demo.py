import sys
import readline

import page_finder


class ManualSpider(object):
    def __init__(self):
        self.link_annotation = page_finder.LinkAnnotation()
        self.visited = set()

    def visit(self, page, start=False):
        self.link_annotation.load(page)
        self.visited.add(page)
        if not start:
            self.link_annotation.mark_link(page)

    def best(self, n):
        ret = []
        for link in self.link_annotation.best_links_to_follow():
            if len(ret) >= n:
                break
            if link not in self.visited:
                ret.append(link)
        return ret

    def get_all_links(self):
        return list(self.link_annotation.links)


def make_completer(links):
    def completer(text, state):
        n = 0
        for link in links:
            if text in link:
                if state == n:
                    return link
                n += 1
    return completer


def link_prompt(links):
    readline.set_completer(make_completer(links))
    return raw_input('Enter link to follow (tab autocompletes): ')


class IncorrectSelection(Exception):
    pass


def link_menu(links):
    print '0) Quit'
    print '1) Enter link directly'
    for i, (link, scores) in enumerate(links):
        print '{0}) {1} (score={2})'.format(i + 2, link, scores[0])
    try:
        selection = int(raw_input('Select link to follow: '))
    except ValueError:
        raise IncorrectSelection
    if selection == 0:
        return None
    elif selection == 1:
        return link_prompt([link for link, _ in links])
    elif selection > len(links) + 2 or selection < 0:
        raise IncorrectSelection
    else:
        return links[selection - 2][0]


if __name__ == '__main__':
    USAGE =\
"""
python demo.py start_url
"""
    if len(sys.argv) != 2:
        sys.exit(USAGE)
    start_page = sys.argv[1]

    readline_config = [
        "tab: complete",
        "set show-all-if-unmodified on",
        "set skip-completed-text on",
        "set completion-ignore-case on"
    ]
    for line in readline_config:
        readline.parse_and_bind(line)
    readline.set_completer_delims('')

    spider = ManualSpider()
    spider.visit(start_page, start=True)

    link = link_prompt(spider.get_all_links())
    if not link:
        sys.exit()
    spider.visit(link)

    while True:
        best = spider.best(5)
        while True:
            try:
                link = link_menu([
                    (link, spider.link_annotation.link_scores(link))
                    for link in best])
                break
            except IncorrectSelection:
                print 'Incorrect selection. Try again'
        if not link:
            sys.exit()
        spider.visit(link)
