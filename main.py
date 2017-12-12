#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 17:28:53 2017

@authors: emma & julia
"""

from flask import Flask, render_template, flash, request
# from flask_wtf import Form as FlaskForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import logging
from encrypt import Encryptor
app = Flask(__name__)

 
class EncryptForm(Form):

    text = TextField('Text to encrypt', validators=[validators.Required()])
   
class DecryptForm(Form):

    text = TextField('Text to Decrypt', validators=[validators.Required()]) 

 
@app.route("/", methods=['GET', 'POST'])
def process_form():
    
    encrypt_form = EncryptForm(request.form)
    decrypt_form = DecryptForm(request.form)
    # encrypt_form = EncryptForm()
    # decrypt_form = DecryptForm()

    if request.method == 'POST':

        if 'encrypt' in request.form:

            encrypt_dict = request.form.to_dict()
            text = encrypt_dict['encrypt']
            print(text)

            encryptor = Encryptor()
            encrypted_text = encryptor.encrypt_LFSR(text)
            seed = encryptor.seed
            tap = encryptor.tap

            # we need to give the user the seed and tap as well
            
            # TODO: ask the user if they want to encrypt with AES or 
            # symmetric authenticated cryptography

            # if encrypt_form.validate():
            if len(text) > 0:
                flash('Encryption Result: {}\n Seed:\n {} Tap: {} '.format(encrypted_text, seed, tap) , 'encrypt')
            else:
                flash('Error: All the form fields are required. ', 'encrypt')
            decrypt_form = None
        else:
            
            decrypt_dict = request.form.to_dict()
            text = decrypt_dict['decrypt']
            print(text)

            # TODO: ask the user if they want to decrypt with AES or 
            # symmetric authenticated cryptography

            seed = '' # user needs to provide seed online as well
            tap = 0 # user needs to provide tap position as well
            
            decrypted = Encryptor.decrypt_with_lfsr(seed, tap, text)

            # if decrypt_form.validate():
            if len(text) > 0:
                flash('Decryption Result:' + decrypted, 'decrypt')
            else:
                flash('Error: All the form fields are required. ', 'decrypt')
            encrypt_form = None
 
    return render_template('index.html', encrypt_form=encrypt_form, decrypt_form=decrypt_form)


def main():
    app.debug = True
    log_handler = logging.FileHandler('my_flask.log')
    log_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(log_handler)
    app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
    app.run()
    
if __name__ == '__main__':
    main()