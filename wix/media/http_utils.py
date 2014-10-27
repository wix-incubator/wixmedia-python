from io import BytesIO
import mimetypes
import urllib2
from uuid import uuid4


def encode_multipart(fields, files, boundary=None):

    def escape_quote(s):
        return s.replace('"', '\\"')

    if boundary is None:
        boundary = uuid4().hex

    lines = []

    for name, value in fields.items():
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
            '',
            str(value),
        ))

    for name, value in files.items():
        filename = value['filename']
        if 'mimetype' in value:
            mimetype = value['mimetype']
        else:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(
                    escape_quote(name), escape_quote(filename)),
            'Content-Type: {0}'.format(mimetype),
            '',
            value['content'],
        ))

    lines.extend((
        '--{0}--'.format(boundary),
        '',
    ))

    s = BytesIO()
    for element in lines:
        s.write(str(element))
        s.write('\r\n')
    body = s.getvalue()

    content_type = 'multipart/form-data; boundary={0}'.format(boundary)

    return body, content_type


def get(url, headers=None):
    opener   = urllib2.build_opener(urllib2.HTTPHandler)
    request  = urllib2.Request(url.encode("utf-8"), headers=headers)
    response = opener.open(request)

    return response.code, response.read(), response.headers


def post_multipart(url, headers=None, fields=None, files=None):
    data, content_type = encode_multipart(fields, files)

    headers.update({
        'Content-Type':   content_type,
        'Content-Length': str(len(data)),
    })

    opener   = urllib2.build_opener(urllib2.HTTPHandler)
    request  = urllib2.Request(url.encode("utf-8"), data=data, headers=headers)
    response = opener.open(request)

    return response.code, response.read(), response.headers