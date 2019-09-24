

class Response:

    def createStatusLine(self, status_code):
        if status_code == 200:
            reason = 'OK'
        elif status_code == 405:
            reason = 'Method Not Allowed'
        elif status_code == 404:
            reason = 'Not Found'
        elif status_code == 403:
            reason = 'Forbidden'
        elif status_code == 400:
            reason = 'Bad Request'
        else:
            reason = ''
        return 'HTTP/1.1 {} {}'.format(status_code, reason)

    def createHeaders(self, header_pairs):
        print(header_pairs)
        headers = ['{}: {}'.format(k, v) for k, v in (header_pairs)]
        print('\r\n'.join(headers) + '\r\n')
        return '\r\n'.join(headers) + '\r\n'

    def createResponse(self, status_code, header_pairs):
        status_line = self.createStatusLine(status_code)
        headers_line = self.createHeaders(header_pairs)
        return '{}\r\n{}\r\n'.format(str(status_line), str(headers_line))
