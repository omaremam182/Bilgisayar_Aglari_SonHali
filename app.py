from flask import Flask, flash , render_template,redirect, request, session, url_for
from Forms import *
import time
from firebase_config22 import fire,db
import firebase_config22
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO, emit
from datetime import datetime
import random

app = Flask (__name__)
app.config["SECRET_KEY"] = '5a46fc92d36e604f423286c04875437f' 
dogrulama = fire.auth()


def check_session_timeout():
    
    if 'last_activity' not in session:
        return redirect(url_for('login'))

    # Şu anki zaman
    current_time = time.time()

    # Son aktivite zamanı ile şu anki zaman farkı
    time_since_last_activity = current_time - session['last_activity']
    if time_since_last_activity > 300:  # 300 saniye = 5 dakika
        session.clear()  
        return redirect(url_for('login'))

    session['last_activity'] = current_time


@app.route("/", methods=["GET", "POST"])
@app.route("/KayitOl", methods=["GET", "POST"])
def kayitOl():
    form = YeniKayitFormu()

    if form.validate_on_submit():
        email = form.Eposta.data
        sifre = form.sifre.data
        telefon = form.telefonNo.data
        kullaniciAdi = form.kullaniciAdi.data
        
        for dosya in firebase_config22.tum_kullanicilar:
            us =  dosya.to_dict()
            if telefon == us["telefonNo"] :
                flash("Bu telefon no zaten kullanımda."," error")
                return render_template("KayitOl.html", baslik="Kayıt Ol", f=form)
            if email == us["email"] :
                flash("Bu e-posta adresi zaten kullanımda. Lütfen başka bir e-posta girin"," error")
                return render_template("KayitOl.html", baslik="Kayıt Ol", f=form)

        try:
            uye = dogrulama.create_user_with_email_and_password(email, sifre)
            # dogrulama.send_email_verification(uye['idToken'])
            uye_id = uye['localId'] 
            
            user_data = {
                "telefonNo": telefon,
                "kullaniciAdi": kullaniciAdi,
                "email": email 
            }

            db.collection("users").document(uye_id).set(user_data) 
            flash("Kayıt başarılı! ", "success")
            session['last_activity'] = time.time()
            return redirect(url_for('home', user_id=uye_id, e =email))
        
        except Exception as e:
            flash("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.", "error")
    
    return render_template("KayitOl.html", baslik="Kayıt Ol", f=form)

@app.route("/Login",methods =["GET","POST"] )
def login():
    form2 = LoginForm()
    if form2.validate_on_submit():
        email = form2.Eposta.data
        sifre = form2.sifre.data
        try:
            user = dogrulama.sign_in_with_email_and_password(email, sifre)
            
            if user:
                print(f"Giriş başarılı. Kullanıcı ID: {user['localId']}") # terminalde yazdırılacak
                session['user_id'] = user['localId']
                session['email'] = email
                session['last_activity'] = time.time()
                flash("Giriş başarılı.", "success")
                return redirect(url_for('home', user_id = user['localId'],e =email ))  
            else:
                flash("Giriş bilgileri yanlış. Lütfen tekrar deneyin.", "error")
        except Exception as e:
            flash("Giriş yaparken bir hata oluştu , Lütfen bilgilerinizin doğru olduğundan emin olun ", "error")

    return render_template("GirisYap.html", baslik="Login", f=form2)

@app.route("/sifremiUnuttum", methods=["GET", "POST"])
def sifremiunuttum():
    buEpostaKayitli = False
    form3 = SifreSifirlama()
    if form3.validate_on_submit():
        
        email = form3.eposta.data
        try:
            for e in firebase_config22.tum_kullanicilar :
                dosya= e.to_dict()
                if email == dosya.get("email") :
                    buEpostaKayitli = True 

            if buEpostaKayitli :
                dogrulama.send_password_reset_email(email)
                flash("E-posta adresinize şifre sıfırlama bağlantısı gönderildi.", "success")
                return redirect("/Login")
            else : 
                flash("Bu eposta adresi sitemizde kayıtlı değilidr ,Lütfen önce kayıt olun", "error")
                return redirect("/KayitOl")

        except Exception as e:
            flash("Bir hata oluştu: " + str(e), "error")
    return render_template("sifremiUnuttum.html", baslik="Forgot password", f=form3)


@app.route("/home",methods=["GET","POST"])
def home():

    eposta = request.args.get('e') 
    user_id = request.args.get('user_id')
    print(f"hello {user_id}")

    # if not user_id:
    #     flash("Geçersiz kullanıcı ID'si.", "error")
    #     return redirect(url_for("kayitOl"))

    kull = list(firebase_config22.tum_kullanicilar)
    for k in kull :
        e=  k.to_dict ().get ("email")
        if e == eposta : 
            kull.pop(kull.index(k))

    
    try:
        
        kullaniciAdlari = [
            {
                "ad": doc.to_dict().get("kullaniciAdi", "Bilinmeyen Kullanıcı"),
                "telefonNo": doc.to_dict().get("telefonNo", "Telefon Yok")
            }
            for doc in kull
        ]
        
        # Oturum kontrolü
        result = check_session_timeout()
        if result:  
            return result
        
        return render_template("home.html",  users = kullaniciAdlari )
    except Exception as e:
        flash("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.", "error")
        return redirect(url_for("kayitOl"))
        
if __name__ == "__main__": 
    app.run(debug=True)
    
