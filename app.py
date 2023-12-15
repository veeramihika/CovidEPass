import requests
from flask import Flask, render_template, request
from twilio.rest import Client
import requests_cache
account_sid='ACdf32bc394d5bd66f9f0994bf8de7a5be'#ur acct_id in single quotes
auth_token='b4e420db66d635c0f748ea97c2d502dd'#ur acct_token in single quotes
client=Client(account_sid,auth_token)
app=Flask(__name__, static_url_path='/static')
@app.route('/')
def registration_form():
    return render_template('test_page.html')
@app.route('/test_page',methods=['POST','GET'])
def login_registration_dtls():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source_state']
    source_dt = request.form['source']
    destination_st = request.form['dest_state']
    destination_dt = request.form['destination']
    phoneNumber = request.form['phoneNumber']
    id_proof = request.form['idcard']
    date = request.form['tripdate']
    full_name=first_name+"."+last_name
    r=requests.get('https://api.covid19india.org/v4/data.json')
    json_data=r.json()
    cnt=json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop=json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass=((cnt/pop)*100)
    if travel_pass<10 and request.method=='POST':
        status='CONFIRMED'
        client.messages.create(to="whatsapp:+918332913845",from_="whatsapp:+14155238886",
                            body="Hello "+" "+full_name+" "+"Your Travel From "+" "+source_dt+" "+"To"+" "+destination_dt+" "
                             +"Has"+ " "+status +" On"+" "+date+" "+", Confirmed")
        return render_template('user_registration_dtls.html',var=full_name,var1=email_id,var2=id_proof,
                               var3=source_st,var4=source_dt,var5=destination_st,var6=destination_dt,
                               var7=phoneNumber, var8=date, var9=status)
    else:
        status='Not confirmed'
        client.messages.create(to="whatsapp:+918332913845",
        from_="whatsapp:+14155238886",
             body = "Hello " + " " + full_name + " " + "Your Travel From " + " " + source_dt + " " + "To" + " " + destination_dt + " "
                    + "Has" + " " + status + " On" + " " + date + " " + ", Apply later")
        return render_template('user_registration_dtls.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phoneNumber, var8=date, var9=status)
if __name__ == "__main__":
    app.run(port=9001,debug=True)