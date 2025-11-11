from flask import Flask,redirect,request,Response,render_template
import pandas as pd
import numpy as np
import joblib
import os
from validate import login,singup

model = joblib.load(os.path.join(os.path.dirname(__file__), "model.pkl"))
encoder = joblib.load(os.path.join(os.path.dirname(__file__), "encoder.pkl"))

app=Flask(__name__)

@app.route("/",methods=['POST','GET'])
def home():
    return render_template('login_signup.html')

@app.route("/login",methods=['GET','POST'])
def login_api():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        data=(email,password)
        res=login(data)
        if res:
            return redirect('/model')
        else:
            return render_template('login_signup.html',show='login',message='Email not found.Please singup',message_type='error')

@app.route("/signup",methods=['GET','POST'])
def signup_api():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        phone=request.form.get('phone')
        data=(name,email,password,phone)
        res=singup(data)
        if res:
            return redirect('/model')
        else:
            return render_template('login_signup.html',show='signup',message='Email already register.Please login',message_type='error')

@app.route('/model',methods=['GET','POST'])
def model_api():
    if request.method=='POST':
        State=request.form.get('State')
        City=request.form.get('City')
        Brand=request.form.get('Brand')
        Fuel_Type=request.form.get('Fuel_Type')
        Transmission=request.form.get('Transmission')
        Year=int(request.form.get('Year'))
        Engine_Size=int(request.form.get('Engine_CC'))
        Mileage=float(request.form.get('Mileage'))
        Power=float(request.form.get('Power'))
        Seats=int(request.form.get('Seats'))
        
        columns = ['State','City','Brand','Fuel_Type','Transmission','Year','Engine_CC','Mileage','Power','Seats']
        data=[[State,City,Brand,Fuel_Type,Transmission,Year,Engine_Size,Mileage,Power,Seats]]
        df=pd.DataFrame(data,columns=columns)
        
        #encode data
        col=df.select_dtypes(include=['object','category']).columns
        encode=encoder.transform(df[col])
        encode_df=pd.DataFrame(encode,columns=encoder.get_feature_names_out(col))
        final_df=pd.concat([df.drop(columns=col,axis=1),encode_df],axis=1)
        
        price=model.predict(final_df)[0]
        
        if price >= 10000000:
            formatted_price = f"{price/10000000:.2f} Crore"
        elif price >= 100000:
            formatted_price = f"{price/100000:.2f} Lakh"
        else:
            formatted_price = f"{price:,.0f}"
            
        return render_template('home.html', predicted_price=formatted_price)
        
    return render_template('home.html')

if __name__=="__main__":
    app.run(debug=True)