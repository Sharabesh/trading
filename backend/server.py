#!/usr/bin/python
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient


# Import the trading suite
sys.path.append("trading/")

# All Critical Login operations
from UserRouteHandler import *



config = {
    "postgres_url": os.environ["HERMES_DB"],
    "production_flag": os.environ.get("PROD"),
    "cookie_secret": os.environ["COOKIE_SECRET"],
}



settings = {
    "login_url": "/login",
    "compress_reponse": True,
    "cookie_secret": config["cookie_secret"],
    "debug": not bool(config["production_flag"]),
    "compress_response": True,
}


def make_app():
    return tornado.web.Application(
        [
            (
                r"/static/(.*)",
                tornado.web.StaticFileHandler,
                {
                    "path": os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), "static"
                    )
                },
            ),
            (r"/logon", LoginHandler),
            (r"/getUserInfo", UserInfoHandler),
            (r"/logout", LogoutHandler),
            (r"/signup", UserSignupHandler),
            (r"/imageUpload", ImageUploadHandler),
        ],
        **settings
    )


if __name__ == "__main__":
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    print("Running at localhost:{0}".format(port))
    tornado.ioloop.IOLoop.current().start()
