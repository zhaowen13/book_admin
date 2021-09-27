# -*- coding: utf-8 -*-
import sys

import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
import requests


# 登录
def login(request):
    body = json.loads(request.body)
    username = body['username']
    password = body['password']
    res = {}
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        res["status"] = True
        response = requests.post("http://127.0.0.1:8000/api-token-auth/",
                                 body).json()
        res["token"] = response['token']
        
    else:
        res["msg"] = "账号或密码错误"
    return HttpResponse(json.dumps(res))


