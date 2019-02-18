#!/usr/bin/env python
import os

from weather_api.app import app

if __name__ == "__main__":
    port = os.environ["API_PORT"]
    app.run(host="localhost", port=port)
