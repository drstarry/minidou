from scrapy.extension import extensions

from scrapy.core.exceptions import IgnoreRequest
from crawl.cc98_util import extract_url, DOMAIN


class DuplicatesFilterMiddleware(object):
    def open_domain(self, domain):
        if domain == DOMAIN:
            self.init_fingerprints()

    def close_domain(self, domain):
        if domain == DOMAIN:
            self.fingerprints = None

    def enqueue_request(self, domain, request):
        if domain != DOMAIN or request.dont_filter:
            return
        fp = self.make_fingerprint(extract_url(request.url))
        if fp in self.fingerprints:
            raise IgnoreRequest('Skipped (request already seen)')
        self.fingerprints.add(fp)

    def make_fingerprint(self, dic):
        return '%s,%s,%s' % (dic['board_id'], dic['thread_id'], dic['page_num'])

    def init_fingerprints(self):
        self.fingerprints = set()