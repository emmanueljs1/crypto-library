#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 17:28:53 2017

@authors: emma & julia
"""

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from functools import reduce
import logging
from encrypt import Encryptor

app = Flask(__name__)
 
encryption_algorithm = ""
decryption_algorithm = ""
encr_result = dict()
decr_result = dict()

@app.route("/process_form", methods=['POST'])
def process_form():

    global encryption_algorithm
    global decryption_algorithm
    
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

    return render_template('index.html', encrypt_alg=encrypt_alg, decrypt_alg=decrypt_alg, 
                            encr_result=encr_result, decr_result=decr_result, crypto_list=crypto_list)
 

@app.route("/", methods=['GET', 'POST'])
def encrypt_decrypt():
    global encryption_algorithm
    global decryption_algorithm
    global encr_result
    global decr_result
    
    if request.method == 'POST':
        request_dict = request.form.to_dict()
        if 'encrypt' in request.form:

            text = request_dict['encrypt']
            encryptor = Encryptor()
            encrypted_text = ""

            if encryption_algorithm == "LFSR":
            
                encrypted_text = encryptor.encrypt_LFSR(text)
                
                def app(s1, s2):
                    return str(s1) + '{}'.format(s2)

                seed = reduce(app, encryptor.seed)            
                tap = encryptor.tap

                encr_result['Encryption Result'] = encrypted_text
                encr_result['Seed'] = seed
                encr_result['Tap'] = tap

                if len(text) < 0:
                   
                    flash('Error: All the form fields are required. ', 'encrypt')

            elif encryption_algorithm == "AES":
    
                encrypted_text = encryptor.encrypt_AES(text)
                key = encryptor.AES_key

                encr_result['Encryption Result'] = encrypted_text
                encr_result['Key'] = key

                if len(text) < 0:
                
                    flash('Error: All the form fields are required. ', 'encrypt')

            else:

                encrypted_text = encryptor.encrypt(text)
                key = encryptor.key

                encr_result['Encryption Result'] = encrypted_text
                encr_result['Key'] = key

                if len(text) < 0:
                    
                    flash('Error: All the form fields are required. ', 'encrypt')
    
        else:
            text = request_dict['decrypt']           

            if decryption_algorithm == "LFSR":
        
                seed = request_dict['seed']
                tap = request_dict['tap']

                decrypted = Encryptor.decrypt_with_lfsr(seed, int(tap), text)
               
                if len(text) > 0:
                    flash('Decryption Result: {}\n'.format(decrypted) , 'decrypt')
                else:
                    flash('Error: All the form fields are required. ', 'decrypt')

            elif decryption_algorithm == "AES":

                key = request_dict['key']
                decrypted = Encryptor.decrypt_with_aes(key, text)

                if len(text) > 0:
                    flash('Decryption Result: {}\n'.format(decrypted) , 'decrypt')
                else:
                    flash('Error: All the form fields are required. ', 'decrypt')

            else:

                key = request_dict['key']
                decrypted = Encryptor.decrypt_with_sac(key, text)

                if len(text) > 0:
                    flash('Decryption Result: {}\n'.format(decrypted) , 'decrypt')
                else:
                    flash('Error: All the form fields are required. ', 'decrypt')
            
    print(encr_result)
    crypto_list = ['LFSR', 'AES', 'Symmetric Authenticated Cryptography']
    return render_template('index.html', encrypt_alg=encryption_algorithm, encr_result=encr_result, decr_result=decr_result,
                            decrypt_alg=encryption_algorithm, crypto_list=crypto_list)


def main():
    app.debug = True
    log_handler = logging.FileHandler('my_flask.log')
    log_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(log_handler)
    app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
    app.run()
    
if __name__ == '__main__':
    main()