
from django.shortcuts import render
from .forms import dataForm
from django.http import HttpResponse
from .models import data

import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


def get_key(password): # Generate a 32 bit key from the user given key

    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password)
    return base64.urlsafe_b64encode(digest.finalize())


def index(request):
    if request.method == "POST":
        form = dataForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            pswd = form.cleaned_data["password"]
            data_tbe = form.cleaned_data["data"]
            encrypt = form.cleaned_data["encrypt"] == "Encrypt"
            m = data(password=pswd, data=data_tbe, encrypt=encrypt)
            m.save()
            print(m)
            return HttpResponse("<script type=\"text/javascript\">window.location.replace('http://{}/data/{}')</script>".format(request.get_host(), str(m.id)))


    else:
        form = dataForm()
    return render(request, 'index.html', {'form':form})


def show_data(request, pk):
    dat = data.objects.get(pk=pk)
    fernet = Fernet( get_key(dat.password.encode()))
    if dat.encrypt:
        output = {
            "title":"Encrypted Data",
            "data": str(fernet.encrypt(dat.data.encode())).strip("b\'").strip("'")
        }
    else:
        output = {
            "data":str(fernet.decrypt(bytes(dat.data.encode("utf-8")))).strip("b\'").strip("'"),
            "title":"Decrypted Data"
        }

    return render(request, 'data_output.html', output)