import csv
import json
import typing
from http.server import HTTPServer, BaseHTTPRequestHandler


collector: typing.List[dict] = []


class StatisticsHandler(BaseHTTPRequestHandler):
    def __init__(self, *args):
        super().__init__(*args)

    def do_POST(self):
        print("got request")
        global collector
        content_length = int(self.headers['Content-Length'])
        collector.append(
            json.loads(
                self.rfile.read(content_length).decode('utf-8'),
            ),
        )
        self.send_response(200)


class Server(HTTPServer):
    MIN_SIZE = 120

    def __init__(self, server_address):
        super().__init__(server_address, StatisticsHandler)
        print(self.server_address)

    def service_actions(self):
        global collector
        if len(collector) <= Server.MIN_SIZE:
            return

        print(len(collector))
        collector = collector[-Server.MIN_SIZE:]
        print(collector)

        with open('a.csv', 'w') as file:
            writer = csv.DictWriter(file, fieldnames=['type', 'time_point', 'size'])
            for item in collector:
                writer.writerow(item)


def run():
    server_address = ('94.154.11.214', 8000)
    httpd = Server(server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
