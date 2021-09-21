from flask import Flask, render_template, request,jsonify
from multiprocessing import Process
import smtplib
import requests,json,re


f=open('config.json','r')
params = json.load(f)["params"]


app = Flask(__name__, static_url_path='/static')
app = Flask(__name__,template_folder='./templates',static_folder='./static')
app = Flask(__name__)

#------smtp mail configuration--------------
mail_user = params["user"]
mail_pswd = params["password"]

#--------simple function--------------------
def registered(pkg_name,user_name,user_key,user_email):
    #----empty list of sent mails & initializing some counter Variables-----
    sent_revs=[]
    total_count=0
    neg_count=0
    neg_per=0
    while(True):
        #------------------deployed (gplay_api.py) on my heroku so using that link (you can refer gplay_api.py file)
        url='https://gplay-rev-api.herokuapp.com/'+pkg_name
        r = requests.get(url).text
        json_obj = json.loads(r)
        # print(json_obj)  
        
        #---------fetching reviews one by one from json & comparing with Topic registerd by user
        for element in json_obj:
            review = element["content"]
            # print(review)
            if re.search(user_key.lower(),review.lower()):
                if review not in sent_revs:
                    print("MATCHING : "+review)
                    
                    total_count+=1
                    if element["score"]<3:
                        neg_count+=1
                    
                    #----------------copying old negativity percentage
                    temp=neg_per    
                    
                    neg_per=((neg_count*100)/total_count)
                    neg_per=round(neg_per, 2) 
                    
                    per_diff= neg_per-temp
                    per_diff=round(per_diff, 2)
                    
                    #---------------Settingup message Format
                    msg="Username : "+element["userName"]+"\nReview : {}\nPosted at : ".format(element["content"])+element["at"]+"\nstars : " +str(element["score"])+" out of 5\n---------- STATISTICS --------- \nPercentage of negative reviews : "+str(neg_per)+"%\nPercentage Differnce : "+str(per_diff)+"%"
                    SUBJECT='Hello ,'+user_name+'!  Notification for new Review on Google Play related with topic : '+ user_key
                    msg = 'Subject: {}\n\n{}'.format(SUBJECT,msg)
                    msg=(msg).encode('utf-8')
                    
                    #---------------SMTP gmail login & sending mail to Registered User
                    server = smtplib.SMTP('smtp.gmail.com:587')
                    server.ehlo()
                    server.starttls()
                    server.login(mail_user,mail_pswd)
                    server.sendmail(mail_user,user_email,msg)
                    #--------------marking as sent to avoid repeating of same review-------
                    sent_revs.append(review)

@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    if request.method == "POST":
        pkg_name = request.form['pkg_name']
        user_email = request.form['email']
        user_name = request.form['name']
        user_key = request.form['key']
        
        #-----------Using Multiprocessing to Render template & to Run infinite Loop function at same time----------
        p1=Process(target = registered,args= (pkg_name,user_name,user_key,user_email,)).start()
        return render_template("done.html")

                                        

if __name__ =="__main__":
    app.run(debug=True)
