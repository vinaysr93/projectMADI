from flask import Flask, url_for,send_from_directory,session
from flask import render_template, request, redirect
from flask import current_app as app
from models import User,TrackerList,Tracker
from datetime import date,time
from datetime import datetime
from datetime import date as todaysDate
from datetime import datetime as todaysDateTime
from database import db
from datetime import date
import requests
import os,random
import csv
import uuid
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.io as pio
pio.renderers.default = "browser"
import plotly.graph_objects as go



numl=[]
session= {}

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message='')

    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        pwd2 = request.form.get("pwd2")
        username=request.form.get("username")
        query_email = User.query.filter_by(useremail=email).first()
        if query_email:

            return render_template("register.html", message="Email already registered ")
        else:
            if pwd == pwd2:  # Checks if the password is the same
                user_entry = User(useremail=email, userpass=pwd,username=username)
                db.session.add(user_entry)
                db.session.commit()
                return render_template("login.html", message='')
            else:
                return render_template("register.html", message="Password doesn't match")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", message='')

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("pwd")
        data_email = User.query.filter_by(useremail=email).first()

        if data_email:
            if data_email.useremail == email:
                data_password = User.query.filter_by(useremail=email).first()

                if password == data_password.userpass:
                    uidq=User.query.filter_by(useremail=email).first()
                    uid=int(uidq.userid)

                    return redirect("/dashboard/{uid}".format(uid=uid))
                else:

                    return render_template("login.html", message="Wrong Password")
            else:

                return render_template("login.html", message="Email Doesn't exist")
        else:

            return render_template("login.html", message="Email doesn't exists")


@app.route("/dashboard/<uid>", methods=["GET", "POST"])
def dashboard(uid):

    username=User.query.filter_by(userid=uid).first().username
    if request.method == "POST" and "login" in request.form:

        item = TrackerList.query.filter_by(userid=uid).all()

        if item == []:

            return render_template("dashboard.html", message='No events are present Add them', item=item,uid=uid,username=username)

        else:


            user_tlist=TrackerList.query.filter_by(userid=uid).all()

            return render_template("dashboard.html",message='',user_tlist=user_tlist,uid=uid,username=username)


    elif request.method == "POST" and 'Add' in request.form:  # Takes care of addition into database

        name = request.form.get('name').strip()
        description = request.form.get("description").strip()
        trackertype = request.form.get("trackertype").strip()
        mcqvalue = request.form.get("mcqvalues").strip()


        checkquery=TrackerList.query.filter_by(tracker_name=name,trackerdescription=description,trackertype=trackertype,mcqvalue=mcqvalue).first()
        if checkquery:

            message="Tracker with same details present please use a different one"
            return render_template("tracker_individual.html", uid=uid, message=message)

        else:


                addentry_tl=TrackerList(tracker_name=name,trackerdescription=description,trackertype=trackertype,mcqvalue=mcqvalue,userid=uid)
                db.session.add(addentry_tl)
                db.session.commit()

                get_id=TrackerList.query.filter_by(tracker_name=name,trackerdescription=description,trackertype=trackertype,mcqvalue=mcqvalue).first()




                return redirect("/dashboard/{uid}".format(uid=uid))

    elif request.method == "GET":

        usert_tlist = TrackerList.query.filter_by(userid=uid).all()

        if usert_tlist==[]:


            return render_template("dashboard.html", message='No Events are present', usert_tlist=usert_tlist,uid=uid,username=username)

        else:
            return render_template("dashboard.html",message='', usert_tlist=usert_tlist,uid=uid,username=username)





    elif request.method == "POST" and 'Update' in request.form:  # Takes care of updation into database
        usert_tlist = TrackerList.query.filter_by(userid=uid).all()
        return render_template("dashboard.html", message='', usert_tlist=usert_tlist,username=username)



@app.route("/tracker_individual/<uid>", methods=["GET", "POST"])
def tracker_individual(uid):
    if request.method == "GET":
        return render_template("tracker_individual.html",uid=uid,message='')

    if request.method == "POST":
        pass

@app.route("/log/<uid>/<tid>",methods=["GET","POST"])
def log(uid,tid):

    query=TrackerList.query.filter_by(userid=uid,tid=tid).first()
    query2=Tracker.query.filter_by(userid=uid,trackerid=tid).first()

    activity_name=query.tracker_name
    tracker_type=query.trackertype




    if query2:
        pass
    else:

        pass



    if request.method=="GET":

        if tracker_type=="binary":

            return render_template("logb.html",activity_name=activity_name,uid=uid,tid=tid)


        elif tracker_type=="numerical":

            return render_template("logn.html",activity_name=activity_name,uid=uid,tid=tid)


        elif tracker_type=="mcq":

            mcq_values=list(query.mcqvalue.split(","))
            return render_template("logm.html",activity_name=activity_name,uid=uid,tid=tid,mcq_values=mcq_values)


    if request.method=="POST":

        if tracker_type=="binary":

            dater=request.form.get("date")
            timer=request.form.get("appt")
            date_split=list(map(int,dater.split("-")))

            datea=date(date_split[0],date_split[1],date_split[2])

            time_split=list(map(int,timer.split(":")))
            timea=time(time_split[0],time_split[1])




            date_time= datetime.combine(datea,timea)
            time_stamp=datetime.timestamp(date_time)




            value=request.form.get("activity_completion")
            notes=request.form.get('Notes')

            add_entry=Tracker(trackerid=tid,userid=uid,date=dater,time=timer,notes=notes,value=value,timestamp=time_stamp)
            add_entry2= TrackerList.query.filter_by(userid=uid,tid=tid).first()
            add_entry2.last_tracked=datetime.fromtimestamp(time_stamp)  # Used to update the last tracked column in tracker list.
            db.session.add(add_entry)
            db.session.commit()

            return redirect("/dashboard/{uid}".format(uid=uid))


        elif tracker_type=="numerical":



            dater = request.form.get("date")
            timer = request.form.get("appt")
            date_split = list(map(int, dater.split("-")))

            datea = date(date_split[0], date_split[1], date_split[2])

            time_split = list(map(int, timer.split(":")))
            timea = time(time_split[0], time_split[1])

            date_time = datetime.combine(datea, timea)
            time_stamp = datetime.timestamp(date_time)



            value = request.form.get("activity_quantity")
            notes = request.form.get('Notes')


            add_entry = Tracker(trackerid=tid, userid=uid, date=dater, time=timer, notes=notes, value=value,
                                timestamp=time_stamp)
            add_entry2 = TrackerList.query.filter_by(userid=uid, tid=tid).first()
            add_entry2.last_tracked = datetime.fromtimestamp(
                time_stamp)  # Used to update the last tracked column in tracker list.
            db.session.add(add_entry)
            db.session.commit()

            return redirect("/dashboard/{uid}".format(uid=uid))


        elif tracker_type == "mcq":
            dater = request.form.get("date")
            timer = request.form.get("appt")
            date_split = list(map(int, dater.split("-")))

            datea = date(date_split[0], date_split[1], date_split[2])

            time_split = list(map(int, timer.split(":")))
            timea = time(time_split[0], time_split[1])

            date_time = datetime.combine(datea, timea)
            time_stamp = datetime.timestamp(date_time)
            value = request.form.get("mcq")
            notes = request.form.get('Notes')

            add_entry = Tracker(trackerid=tid, userid=uid, date=dater, time=timer, notes=notes, value=value,
                                timestamp=time_stamp)

            add_entry2 = TrackerList.query.filter_by(userid=uid, tid=tid).first()
            add_entry2.last_tracked = datetime.fromtimestamp( time_stamp)
            db.session.add(add_entry)
            db.session.commit()

            return redirect("/dashboard/{uid}".format(uid=uid))





@app.route(("/activitylog/<uid>/<tid>"),methods=["GET","POST"])
def     tracker_mod(uid,tid):

    if request.method=="GET":
        tquery = Tracker.query.filter_by(userid=uid,trackerid=tid).all()
        tquery2=TrackerList.query.filter_by(userid=uid,tid=tid).first()
        tquery3 = Tracker.query.filter_by(userid=uid, trackerid=tid).all()
        name=tquery2.tracker_name
        description=tquery2.trackerdescription
        timestampl=[]
        valuel=[]



        for x in tquery:
            timestampl.append(datetime.fromtimestamp(float(x.timestamp)))
            valuel.append(x.value)


        l=len(valuel)
        x=pd.to_datetime(timestampl)
        y=pd.DataFrame(valuel)

        plt.scatter(timestampl,valuel)
        plt.xlabel("Timestamp")
        plt.ylabel("Value")
        plt.tight_layout()
        plt.xticks(rotation=30, ha='right')
        plt.savefig('./static/graph.png')
        plt.close()


        return render_template("activitylog_details.html",uid=uid,tid=tid,img="{{url_for('static', filename='graph.png')}}",tlist=tquery3,name=name,description=description)





@app.route(("/activitylog/update/<uid>/<tid>/<timestamp>"),methods=["GET","POST"])
def activity_log_update(uid,tid,timestamp):


    if request.method=='GET':

        q=TrackerList.query.filter_by(tid=tid,userid=uid).first()
        type=q.trackertype
        name=q.tracker_name
        if type=='numerical':

            subq=Tracker.query.filter_by(userid=uid,trackerid=tid,timestamp=timestamp).first()
            date=subq.date
            time=subq.time
            value=subq.value
            notes=subq.notes

            return render_template('activity_log_update_n.html',date=date,time=time,value=value,name=name,tid=tid,uid=uid,timestamp=timestamp)

        elif type=='binary':
            subq = Tracker.query.filter_by(userid=uid, trackerid=tid, timestamp=timestamp).first()
            date = subq.date
            time = subq.time
            notes= subq.notes
            return render_template('activity_log_update_b.html', date=date, time=time,notes=notes,name=name,tid=tid,uid=uid,timestamp=timestamp)

        elif type=='mcq':

            subq = Tracker.query.filter_by(userid=uid, trackerid=tid, timestamp=timestamp).first()
            date = subq.date
            time = subq.time
            notes = subq.notes
            mcqvalue=list(q.mcqvalue.split(","))
            return render_template('activity_log_update_m.html', date=date, time=time, notes=notes,name=name,tid=tid,uid=uid,timestamp=timestamp,mcq_values=mcqvalue)





    if request.method=='POST':
        q = Tracker.query.filter_by(trackerid=tid, userid=uid,timestamp=timestamp).first()
        q2= TrackerList.query.filter_by(tid =tid,userid=uid).first()
        type = q2.trackertype

        if type == 'numerical':

            value=request.form.get('activity_quantity')
            notes=request.form.get('Notes')

            q.value=value
            q.notes=notes
            db.session.commit()

            return redirect("/activitylog/{uid}/{tid}".format(uid=uid, tid=tid))



        if type=='binary':

            value=request.form.get("activity_completion")
            notes=request.form.get("Notes")

            q.value = value
            q.notes = notes
            db.session.commit()

            return redirect("/activitylog/{uid}/{tid}".format(uid=uid, tid=tid))

        if type=='mcq':


            value=request.form.get("mcq")
            print(value)
            notes=request.form.get("Notes")
            q.value = value
            q.notes = notes
            db.session.commit()

            return redirect("/activitylog/{uid}/{tid}".format(uid=uid, tid=tid))




@app.route(("/activitylog/delete/<uid>/<tid>/<timestamp>"),methods=["GET","POST"])
def activity_log_delete(uid,tid,timestamp):

        queryt=Tracker.query.filter_by(userid=uid,trackerid=tid,timestamp=timestamp).all()



        for x in queryt:
            db.session.delete(x)
            db.session.commit()

        return redirect("/activitylog/{uid}/{tid}".format(uid=uid,tid=tid))



























@app.route("/delete/<uid>/<tid>", methods=["GET", "POST"])
def delete_entry(uid,tid):

    del_entry = TrackerList.query.filter_by(userid=uid,tid=tid).first()
    del_entry2= Tracker.query.filter_by(userid=uid,trackerid=tid).all()


    for x in del_entry2:
        db.session.delete(x)
    db.session.commit()

    db.session.delete(del_entry)
    db.session.commit()

    return redirect("/dashboard/{uid}".format(uid=uid))

@app.route("/update/<uid>/<tid>",methods=["GET","POST"])
def update(uid,tid):
    if request.method=="GET":

        tquery=TrackerList.query.filter_by(userid=uid,tid=tid).first()
        tname=tquery.tracker_name
        tdescription=tquery.trackerdescription
        mcqvalue=tquery.mcqvalue
        trackertype=tquery.trackertype
        return render_template("tracker_update.html", uid=uid,tid=tid,tname=tname,tdescription=tdescription,mcqvalue=mcqvalue,trackertype=trackertype)

    if request.method=="POST":

        description = request.form.get("description")
        trackertype = request.form.get("trackertype")
        mcqvalue = request.form.get("mcqvalues")

        update_query=TrackerList.query.filter_by(userid=uid,tid=tid).first()
        update_query.trackerdescription=description
        update_query.trackertype=trackertype
        update_query.mcqvalue=mcqvalue

        db.session.commit()
        return redirect("/dashboard/{uid}".format(uid=uid))



