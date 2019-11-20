import re

rePO = re.compile(r'^(?P<method>[A-Z]+) ((?P<scheme>\w+)://)?(?(3)[^/]*)/?(?P<path>[^\?#]*/?)?(\?[^#]*)?(\#.*)? HTTP/1.[0|1]$')


class RequestParser:

    # def __init__(self):
        # self.request_line = RequestLineParser()
        # self.headers = RequestHeadersParser()


    def __call__(self, request):
        if not isinstance(request, str):
            return False

        split = request.split('\r\n\r\n')
        if len(split) == 2:
            request_head, _ = split
            head = request_head.split('\r\n')
            if len(head) == 1:
                return self.parseRequestLine(*head)
            elif len(head) > 1:
                req_line, *headers = head
                return self.parseRequestLine(req_line) and self.parseRequestHeaders(headers)
            else:
                return False


    def parseRequestLine(self, request_line):
        if not isinstance(request_line, str):
            return False

        match = rePO.match(request_line)

        self.method = match.group('method')

        if match.group('scheme') not in [None, 'http', 'https']:
            return False

        if match.group('path') != '/':
            self.path = match.group('path') or 'index.html'
        else:
            self.path = 'index.html'

        return True

    def parseRequestHeaders(self, request_headers):
        if not isinstance(request_headers, list):
            return False
        self.headers = []
        for header in request_headers:
            key_value = [x for x in header.split(': ') if x]

            if len(key_value) == 2:
                key, value = key_value
                self.headers.append([key.lower(), value])
            else:
                return False

        return True