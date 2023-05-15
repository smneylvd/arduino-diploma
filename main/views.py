import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from main.models import User, Device, AccessList, Log


# Create your views here.

def index(req):
    return render(req, 'launch_page.html')


def login_view(req):
    if req.method == "POST":
        try:
            user = authenticate(req, nickname=req.POST['nickname'], password=req.POST['password'])
            login(req, user)
            return redirect('main')
        except:
            messages.error(req, "Incorrect username or password")
            return render(req, 'login_page.html')

    return render(req, 'login_page.html')


def logout_view(req):
    logout(req)
    return redirect('index')


def register(req):
    if req.method == "POST":
        try:
            first_name = req.POST['firstname']
            last_name = req.POST['lastname']
            email = req.POST['email']
            phone = req.POST['phone']
            nickname = req.POST['nickname']
            password = req.POST['password']
            user = User(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone,
                        nickname=nickname)
            user.set_password(password)
            user.save()
        except:
            messages.error(req, "Email address or nickname is duplicated, try to use another one")
            return render(req, "register_page.html")
        return redirect('login')
        # print(first_name, last_name, email, phone, nickname, password)
    return render(req, "register_page.html")


def main(req):
    if not req.user.is_authenticated:
        return redirect("login")

    devices_access = AccessList.objects.filter(user=req.user)
    device_ids = []
    for obj in devices_access.values("device_id"):
        device_ids.append(obj['device_id'])
    devices = Device.objects.filter(id__in=device_ids)

    for i in range(len(devices)):
        print(devices)
        if devices_access[i].alias != "" and devices[i].id == devices_access[i].device_id:
            devices[i].name = devices_access[i].alias + " (" + devices[i].name + ")"

    if req.user.is_superuser:
        return render(req, 'admin_page.html', {
            "devices": devices
        })

    return render(req, 'main_page.html', {
        "devices": devices
    })


def addDevice(req):
    if not req.user.is_authenticated:
        return redirect("login")

    if req.method == "POST":
        device = Device(
            identifier=req.POST['id'],
            password=req.POST['password'],
            name=req.POST['name'],
        )
        device.save()
        access = AccessList(user=req.user, access_type=1, device=device)
        access.save()

        return redirect("main")


def getDeviceInfo(req, id):
    if not req.user.is_authenticated:
        return redirect("login")

    device = Device.objects.get(id=id)
    if device:
        user_id_query = AccessList.objects.filter(device=device).values("user_id")
        user_ids = []
        for i in user_id_query:
            user_ids.append(i['user_id'])
        users = User.objects.filter(id__in=user_ids)
        if users:
            return JsonResponse(serialize_models(users), safe=False)


def serialize_models(collection):
    serialized_data = serialize('json', collection)
    return serialized_data


def grantAccess(req):
    if not req.user.is_authenticated:
        return redirect("login")

    if req.method == "POST":
        try:
            device_id = req.POST['device_id']
            access = AccessList.objects.get(user=req.user, device_id=device_id)

            if access and access.access_type == 1:
                user = User.objects.get(nickname=req.POST['nickname'])

                if not User:
                    return redirect("main")

                new_access = AccessList(user_id=user.id, device_id=device_id, access_type=2)
                new_access.save()
        except:
            messages.error(req, "User with this nickname not found")
    return redirect("main")


def getAccess(req):
    if not req.user.is_authenticated:
        return redirect("login")

    if req.method == "POST":
        try:
            identifier = req.POST['identifier']
            password = req.POST['password']
            alias = req.POST['alias']
            device = Device.objects.get(identifier=identifier, password=password)
            if device:
                new_access = AccessList(user=req.user, device=device, access_type=1, alias=alias)
                new_access.save()
        except:
            messages.error(req, "Incorrect Device ID or password")
        return redirect("main")


def accessListView(req):
    devices_access = AccessList.objects.filter(user=req.user)
    device_ids = []
    for obj in devices_access.values("device_id"):
        device_ids.append(obj['device_id'])
    devices = Device.objects.filter(id__in=device_ids)

    for i in range(len(devices)):
        print(devices)
        if devices_access[i].alias != "" and devices[i].id == devices_access[i].device_id:
            devices[i].name = devices_access[i].alias + " (" + devices[i].name + ")"

    return render(req, "edit_locker.html", {
        "devices": devices,
    })


def deleteAccess(req):
    if not req.user.is_authenticated:
        return redirect("login")

    if req.method == "POST":
        user_nickname = req.POST['user_nickname']
        device_id = req.POST['device_id']
        access = AccessList.objects.get(user__nickname=user_nickname, device_id=device_id)
        if access:
            access.delete()

        return redirect("accessListView")


def getDeviceStatus(req, identifier):
    device = Device.objects.get(identifier=identifier)
    if device:
        status = "on" if device.status else "off"
        return HttpResponse(status)

    return HttpResponse("Device not found")


def setDeviceStatus(req):
    if not req.user.is_authenticated:
        return redirect("login")

    device_id = req.POST['device_id']
    user = req.user
    action = req.POST['action']
    device = Device.objects.get(id=device_id)
    device.status = action
    device.save()
    log = Log(user=user, device=device, action=action)
    log.save()
    return redirect("main")


def logsView(req):
    if not req.user.is_authenticated:
        return redirect("login")
    devices_access = AccessList.objects.filter(user=req.user)
    device_ids = []

    for obj in devices_access.values("device_id"):
        device_ids.append(obj['device_id'])
    devices = Device.objects.filter(id__in=device_ids)

    for i in range(len(devices)):
        print(devices)
        if devices_access[i].alias != "" and devices[i].id == devices_access[i].device_id:
            devices[i].name = devices_access[i].alias + " (" + devices[i].name + ")"

    return render(req, "logs.html", {"devices": devices})


def getDeviceLogs(req, device_id):
    logCollection = Log.objects.filter(device_id=device_id).order_by('-time')
    logs = []
    for i in range(len(logCollection)):
        logs.append({
            "nickname": logCollection[i].user.nickname,
            "device": logCollection[i].device.name,
            "action": "on" if logCollection[i].action == "True" else "off",
            "time": logCollection[i].time.strftime("%B %d, %Y, %H:%M:%S")
        })

    return JsonResponse(json.dumps(logs, indent=4, sort_keys=True, default=str), safe=False)
