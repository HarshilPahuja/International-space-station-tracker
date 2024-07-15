#run the code overnight and keep your mail notif. on, If the ISS is above your head, you'll get a notif!
import requests
from datetime import datetime
import smtplib
import time

response=requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data=response.json()
iss_latitude=float(data['iss_position']['latitude'])
iss_longitude=float(data['iss_position']['longitude'])


#sunset-sunrise timing
parameters={
    "lat":69.456840,#your position's latitude
    "lng":30.050410,#your positions's longitude
    "formatted":0,
}

response=requests.get(url="https://api.sunrise-sunset.org/json",params=parameters)
response.raise_for_status()
data=(response.json())

def convert_ist(variable):
    var1=variable.split(':')
    var2=[int(i) for i in var1]
    hour=var2[0]
    minute=var2[1]
    hour=hour+5
    minute=minute+30
    if minute>60:
        minute=minute-60
        hour+=1
    if hour>=24:
        hour=hour-24
    var3=[hour,minute]
    return var3[0]

sunrise_var = (data['results']['sunrise'].split('T')[1])[0:5]
sunset_var=(data['results']['sunset'].split('T')[1])[0:5]
sunrise_hour=convert_ist(sunrise_var)
sunset_hour=convert_ist(sunset_var)
timenow=datetime.now()
current_hour=timenow.hour

def iss():
    iss_latitude_min=iss_latitude-5
    iss_latitude_max=iss_latitude+5
    iss_longitude_min=iss_longitude-5
    iss_longitude_max=iss_longitude+5
    if parameters["lat"]>=iss_latitude_min and parameters['lat']<=iss_latitude_max:
        if parameters["lng"]>=iss_longitude_min and parameters["lng"]<=iss_longitude_max:
            if current_hour>sunset_hour and current_hour<sunrise_hour: #i.e if its dark outside
                return True
            else:
                return False
        else:
            return False
    else:
        return False
        
i=1
while True:
    time.sleep(80) #every 80 seconds it searches for the ISS
    if iss():
        connection=smtplib.SMTP("smtp.gmail.com")
        my_email="pythontestharshil@gmail.com"
        reciever_email="pythontestharshil@yahoo.com"
        password="gwakgwakwompwomp"
        connection.starttls()
        connection.login(user=my_email,password=password)
        connection.sendmail(from_addr=my_email,to_addrs=reciever_email,msg="Subject:LOOK UP ITS THE ISS \n\n YOU MIGHT BE ABLE TO SEE THE ISS RIGHT NOW!!!!!!!!!!")
        connection.close()
    else:
        print(f"search cycle {i} done")
        i+=1
