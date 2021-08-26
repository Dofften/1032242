# from wsgiref.simple_server import make_server
from waitress import serve
from urls import url_patterns
from models import create_database


class WebApp:
    def __call__(self, environ, start_response):
        def content_type(path):
            if path.endswith(".gif"):
                return "image/gif"
            elif path.endswith(".js"):
                return "text/js"
            elif path.endswith(".css"):
                return "text/css"
            elif path.endswith(".png"):
                return "image/png"
            else:
                return "text/html"
        func = None
        for item in url_patterns:
            if item[0] == environ.get('PATH_INFO'):
                func = item[1]
                break
        if func:
            start_response('200 OK', [('Content-Type', content_type(environ.get('PATH_INFO')))])
            data = func(environ)
            return [data]
        else:
            start_response('404 Not Found', [('Content-Type', content_type(environ.get('PATH_INFO')))])
            data = b''
            with open("assets/404.html", 'rb') as f:
                data = f.read()
            return [data]
app = WebApp()
create_database()


if __name__ == '__main__':
    try:
        print('serving at http://127.0.0.1:8000\nPress"ctrl+c" to stop serving')
        myserver = serve(app, port=8000, threads=12)
        print("Server has been stopped")
        with open("temp.txt", "r+") as logged_in:
            logged_in.truncate(0)
    except:
        print("an error occured please check your server setup")

