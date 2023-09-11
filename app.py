from .import create_app

app = create_app()


@app.route('/')
def hello():
    return "Hello World!"

from .api.v1 import urls
from .users import urls

if __name__ == "__main__":
    app.run()
