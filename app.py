#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import io, os, sys, types
from IPython import get_ipython

from nbformat import current
from IPython.core.interactiveshell import InteractiveShell


# In[ ]:


def find_notebook(fullname, path=None):
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" if Foo_Bar
    does not exist.
    """
    name = fullname.rsplit('.', 1)[-1]
    if not path:
        path = ['']
    for d in path:
        nb_path = os.path.join(d, name + ".ipynb")
        if os.path.isfile(nb_path):
            return nb_path
        # let import Notebook_Name find "Notebook Name.ipynb"
        nb_path = nb_path.replace("_", " ")
        if os.path.isfile(nb_path):
            return nb_path


class NotebookLoader(object):
    """Module Loader for Jupyter Notebooks"""
    def __init__(self, path=None):
        self.shell = InteractiveShell.instance()
        self.path = path

    def load_module(self, fullname):
        """import a notebook as a module"""
        path = find_notebook(fullname, self.path)

        print ("importing Jupyter notebook from %s" % path)

        # load the notebook object
        with io.open(path, 'r', encoding='utf-8') as f:
            nb = current.read(f, 'json')


        # create the module and add it to sys.modules
        # if name in sys.modules:
        #    return sys.modules[name]
        mod = types.ModuleType(fullname)
        mod.__file__ = path
        mod.__loader__ = self
        mod.__dict__['get_ipython'] = get_ipython
        sys.modules[fullname] = mod

        # extra work to ensure that magics that would affect the user_ns
        # actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        try:
            for cell in nb.worksheets[0].cells:
                if cell.cell_type == 'code' and cell.language == 'python':
                    # transform the input to executable Python
                    code = self.shell.input_transformer_manager.transform_cell(cell.input)
                    # run the code in themodule
                    exec(code, mod.__dict__)
        finally:
            self.shell.user_ns = save_user_ns
        return mod


class NotebookFinder(object):
    """Module finder that locates Jupyter Notebooks"""
    def __init__(self):
        self.loaders = {}

    def find_module(self, fullname, path=None):
        nb_path = find_notebook(fullname, path)
        if not nb_path:
            return

        key = path
        if path:
            # lists aren't hashable
            key = os.path.sep.join(path)

        if key not in self.loaders:
            self.loaders[key] = NotebookLoader(path)
        return self.loaders[key]

sys.meta_path.append(NotebookFinder())


# In[ ]:


from Covi19 import model
import numpy as np
import keras
from keras.layers import *
from keras.models import *
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator,load_img, img_to_array
import matplotlib.pyplot as plt
import flask
import numpy as np
import pandas as pd
from flask import Flask,render_template, Response
from flask import Flask, request,jsonify
from keras import backend as K;
K.clear_session()


# In[ ]:


K.clear_session()


# In[ ]:


from flask import Flask, request,render_template,redirect,jsonify,json

import base64
import hashlib
import time
import os
from json import dumps

app = Flask(__name__)
@app.route("/") 
def index():
    return render_template("upload_image.html")

app.config["IMAGE_UPLOADS"]=r"C:\Users\win-10\flask\image"
app.config["ALLOWED_IMAGE_EXT"]=["JPEG","PNG","JPG"]
app.config["MAX_IMAGE_SIZE"]=0.5*1024*1024

def allowed_image(filename):
    
    print(filename)
    if not"." in filename:
        return False
    ext=filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXT"]:
        
        return True
    else:
        return False
    
def allowed_size(filesize):
    if int(filesize)<=app.config["MAX_IMAGE_SIZE"]:
        return True
    else:
        return False


@app.route("/success",methods=['GET','POST'])

def success():
    d={}
    new=""
    string={}
    
    
    if request.method=="POST":


            image=request.files["image"]

            if image.filename=="":

                print("No Filename")
                return redirect(request.url)  

            if allowed_image(image.filename):

            
                print(image.filename)


                date_string = time.strftime("%Y-%m-%d-%H:%M") 
                image.save(os.path.join(app.config["IMAGE_UPLOADS"] +"\\" +image.filename))


                add=os.path.join(app.config["IMAGE_UPLOADS"]+"\\" +image.filename)
                model=load_model('mod.h5')
                
                img=load_img(add,target_size=(224,224))
                img=img_to_array(img)
                img=np.expand_dims(img,axis=0)
                
                
                
                
                pred=model.predict_classes(img)
                if(pred[0][0]==0):
                    new='Covid'
                else:
                    new='Normal'
               



            response1=json.dumps(new)
            
            return new
    else:
        print(request.url)
        return redirect(request.url)

  
    
if __name__ == "__main__":
    app.run()


# In[ ]:




