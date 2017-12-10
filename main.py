#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 17:28:53 2017

@authors: emma & julia
"""

from flask import Flask
import logging

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Hello world!'

def main():
    app.debug = True
    log_handler = logging.FileHandler('my_flask.log')
    log_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(log_handler)
    app.run()
    
if __name__ == '__main__':
    main()