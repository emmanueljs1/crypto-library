#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 17:28:53 2017

@authors: emma & julia
"""

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import logging
from encrypt import Encryptor
app = Flask(__name__)
 
encryption_algorithm = ""
decryption_algorithm = ""

@app.route("/process_form", methods=['GET', 'POST'])
def process_form():
    
    decrypt_alg = "LFSR"
    encrypt_alg = "LFSR"

    if request.method == 'POST':
        request_dict = request.form.to_dict()

        if 'encryption_select' in request.form:
            encrypt_alg = request_dict['encryption_select']
 
        elif 'decryption_select' in request.form:
            decrypt_alg = request_dict['decryption_select']
    
    crypto_list = ['LFSR', 'AES', 'Symmetric Authenticated Cryptography']

    # update global variable
    encryption_algorithm = encrypt_alg
    decryption_algorithm = decrypt_alg

    return render_template('index.html', encrypt_alg=encrypt_alg, decrypt_alg=decrypt_alg, crypto_list=crypto_list)


@app.route("/", methods=['GET', 'POST'])
def encrypt():
    
    if request.method == 'POST':
        request_dict = equest.form.to_dict()

        if 'encrypt' in request.form:

            text = request_dict['encrypt']
            encryptor = Encryptor()
            encrypted_text = ""

            if encryption_algorithm is "LFSR":
            
                encrypted_text = encryptor.encrypt_LFSR(text)
                seed = encryptor.seed
                tap = encryptor.tap

                if len(text) > 0:
                    flash('Encryption Result: {}\n Seed:{} \n Tap: {} \n '.format(encrypted_text, seed, tap) , 'encrypt')
                else:
                    flash('Error: All the form fields are required. ', 'encrypt')

            elif encryption_algorithm is "AES":
    
                encrypted_text = encryptor.encrypt_AES(text)
                key = encryptor.AES_key
                if len(text) > 0:
                    flash('Encryption Result: {}\n Key: {}\n '.format(encrypted_text, key) , 'encrypt')
                else:
                    flash('Error: All the form fields are required. ', 'encrypt')

            else:

                encrypted_text = encryptor.encrypt(text)
                key = encryptor.key

                if len(text) > 0:
                    flash('Encryption Result: {}\n Seed:\n {} Tap: {} '.format(encrypted_text, key) , 'encrypt')
                else:
                    flash('Error: All the form fields are required. ', 'encrypt')
    
        else:
            
            text = request_dict['decrypt']
            print(text)

            seed = '' # user needs to provide seed online as well
            tap = 0 # user needs to provide tap position as well
            
            decrypted = Encryptor.decrypt_with_lfsr(seed, tap, text)
            decrypt_form = decrypt_form2
            # if decrypt_form.validate():
            if len(text) > 0:
                flash('Decryption Result:' + decrypted, 'decrypt')
            else:
                flash('Error: All the form fields are required. ', 'decrypt')
            encrypt_form = None
    
    crypto_list = ['LFSR', 'AES', 'Symmetric Authenticated Cryptography']
    return render_template('index.html', decrypt_alg=decrypt_alg, crypto_list=crypto_list)


def main():
    app.debug = True
    log_handler = logging.FileHandler('my_flask.log')
    log_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(log_handler)
    app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
    app.run()
    
if __name__ == '__main__':
    main()