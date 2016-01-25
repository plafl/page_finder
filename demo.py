import sys

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


def link_menu(links):
    print '0) Quit'
    for i, link in enumerate(links):
        print '{0}) {1}'.format(i + 1, link)
    return int(raw_input('Select link to follow: '))


if __name__ == '__main__':
    page = sys.argv[1]
    spider = ManualSpider()
    spider.visit(page, start=True)
    all_links = spider.get_all_links()
    selection = link_menu(all_links)
    if selection == 0:
        sys.exit()
    spider.visit(all_links[selection - 1])
    while True:
        best = spider.best(3)
        selection = link_menu(best)
        if selection == 0:
            sys.exit()
        spider.visit(best[selection - 1])
