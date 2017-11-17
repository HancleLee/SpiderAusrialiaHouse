from urllib import parse

from scrapy.core.downloader.handlers.http11 import HTTP11DownloadHandler, ScrapyAgent, _RequestBodyProducer
from time import time
from twisted.internet import reactor
from twisted.web.http_headers import Headers as TxHeaders
from scrapy.utils.python import to_bytes

# print"MyDownloadHandler...=============================================================="

# backwards compatibility
class MyDownloadHandler(HTTP11DownloadHandler):
    def __init__(self, settings, *args, **kwargs):
        super(MyDownloadHandler, self).__init__(settings)

    def download_request(self, request, spider):
        """Return a deferred for the HTTP download"""
        agent = ScrapyAgentRefact(contextFactory=self._contextFactory, pool=self._pool,
                                  maxsize=getattr(spider, 'download_maxsize', self._default_maxsize),
                                  warnsize=getattr(spider, 'download_warnsize', self._default_warnsize))
        return agent.download_request(request)


class ScrapyAgentRefact(ScrapyAgent):
    def download_request(self, request):
        timeout = request.meta.get('download_timeout') or self._connectTimeout
        agent = self._get_agent(request, timeout)

        # request details
        url = parse.urldefrag(request.url)[0]
        method = to_bytes(request.method)
        headers = TxHeaders(request.headers)
        # if isinstance(agent, self._TunnelingAgent):
        #     headers.removeHeader(b'Proxy-Authorization')
        if request.body:
            bodyproducer = _RequestBodyProducer(request.body)
        else:
            bodyproducer = None

            if method == b'POST':
                headers.addRawHeader(b'Content-Length', b'0')

        start_time = time()
        d = agent.request(
            method, to_bytes(url, encoding='ascii'), headers, bodyproducer)
        # set download latency
        d.addCallback(self._cb_latency, request, start_time)
        # response body is ready to be consumed
        d.addCallback(self._cb_bodyready, request)
        d.addCallback(self._cb_bodydone, request, url)
        # check download timeout
        self._timeout_cl = reactor.callLater(timeout, d.cancel)
        d.addBoth(self._cb_timeout, request, url, timeout)
        return d
