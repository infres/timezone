import json
from html import escape
from pytz import timezone
from datetime import datetime
from wsgiref.simple_server import make_server
#import logging

#logger = logging.getLogger(__name__)
#logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

def TimeZone(env, get_resp):
    response_headers = [('Content-type', 'text/plain')]
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    print(env['REQUEST_METHOD'], get_resp)
    if env['REQUEST_METHOD'] == 'GET':
        path = escape(env.get('PATH_INFO', ''))
        if path != '/index':
            global response, status
            if path == '/':
                tz = timezone('GMT')
                dt = datetime.now(tz)
                response = dt.strftime(fmt)
                status = '200 OK'
            else:
                try:
                    tz = timezone(path[1:])
                    dt = datetime.now(tz)
                    response = dt.strftime(fmt)
                    status = '200 OK'
                except Exception:
                    response = 'Invalid timezone'
                    status = '400 Bad Request'
            get_resp(status, response_headers)
            yield bytes(response, 'utf-8')
        else:
            status = '200 OK'
            get_resp(status, response_headers)
    elif env['REQUEST_METHOD'] == 'POST':
        if env['PATH_INFO'] == '/api/v1/convert':
            try:
                request_size = int(env.get('CONTENT_LENGTH', 0))
            except ValueError:
                request_size = 0
            request_body = env['wsgi.input'].read(request_size).decode('utf-8')
            data = json.loads(request_body)
           # logger.info(data)

            target_tz_str = data['target_tz']
            target_tz = timezone(target_tz_str)
            current_tz_str = data['tz']
            current_date_time_str = data['date']
            current_date_time = datetime.strptime(current_date_time_str, '%m.%d.%Y %H:%M:%S')
            target_date_time = current_date_time.astimezone(target_tz)
            response = target_date_time.strftime(fmt)
            status = '200 OK'

            get_resp(status, response_headers)
            yield bytes(response, 'utf-8')

        elif env['PATH_INFO'] == '/api/v1/datediff':
            try:
                request_size = int(env.get('CONTENT_LENGTH', 0))
            except (ValueError):
                request_size = 0

            request_body = env['wsgi.input'].read(request_size).decode('utf-8')
            data = json.loads(request_body)

            try:
                first_date_str = data['first_date']
                first_tz_str = data['first_tz']
                second_date_str = data['second_date']
                second_tz_str = data['second_tz']
                first_tz = timezone(first_tz_str)
                first_date_time = datetime.strptime(first_date_str, '%m.%d.%Y %H:%M:%S')
                first_date_time = first_tz.localize(first_date_time)
                second_tz = timezone(second_tz_str)
                second_date_time = datetime.strptime(second_date_str, '%I:%M%p %Y-%m-%d')
                second_date_time = second_tz.localize(second_date_time)
                time_diff = abs((second_date_time - first_date_time).total_seconds())
                response = str(time_diff)
                status = '200 OK'
            except Exception as err:
              #  logger.error(err)
                response = 'Invalid parameters'
                status = '400 Bad Request'

            get_resp(status, response_headers)
            yield bytes(response, 'utf-8')
        else:
            status = '400 Bad Request'
            get_resp(status, response_headers)

    ret = [("%s: %s\n" % (key, value)).encode("utf-8")
           for key, value in env.items()]
    return ret


with make_server('', 8000, TimeZone) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()