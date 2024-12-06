from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField,PasswordField,SubmitField,EmailField
from wtforms.validators import *


# def sifre_dogrulama(form, field):
#     sifre = field.data    
#     if not any(karakter.islower() for karakter in sifre):
#         raise ValidationError("Şifre en az bir küçük harf içermelidir.")
#     if not any(karakter.isupper() for karakter in sifre):
#         raise ValidationError("Şifre en az bir büyük harf içermelidir.")
#     if not any(karakter.isdigit() for karakter in sifre):
#         raise ValidationError("Şifre en az bir rakam içermelidir.")



class YeniKayitFormu(FlaskForm) :
    kullaniciAdi = StringField("kullanıcı Adı ", validators=[DataRequired("bu alanı doldurmak zorunlu"),Length(min=2,max=25)])
    telefonNo =    StringField("Telefon Numarası ", validators=[DataRequired("Lütfen telefon numaranızı başında sıfır olmadan yazınız"),
        Length(min=10, max=10)])
    
    Eposta = EmailField("email ", validators=[  
        DataRequired(message="E-posta adresi gereklidir."),
        Email(message="Lütfen geçerli bir e-posta adresi girin !!")])

    sifre = PasswordField("Şifre", validators=[
        DataRequired(),
        Length(min=8, max=32, message="Şifre 8 ile 32 karakter arasında olmalıdır"),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,32}$', message="Şifre en az bir küçük harf, bir büyük harf, bir rakam ve en az iki özel karakter içermelidir.")
    ])
    sifreTekrar = PasswordField("Şifre Doğrulama", validators=[DataRequired(),Length(min=8 ,max=32), EqualTo('sifre', message="Şifreler eşleşmiyor.")])
    buton = SubmitField("kayıt ol")

class SifreSifirlama(FlaskForm):
    eposta = EmailField("E-posta", validators=[
        DataRequired(message="E-posta adresi gereklidir."),
        Email(message="Lütfen geçerli bir e-posta adresi girin.")
    ])
    buton = SubmitField("Şifremi Sıfırla")

# class forgotPass (YeniKayitFormu):
#     buton = SubmitField("Şifremi Unuttum")


class LoginForm(FlaskForm) :
    
    Eposta = EmailField("email ", validators=[  
        DataRequired(message="E-posta adresi gereklidir."),
        Email()])
    
    sifre = PasswordField("Şifre ", validators=[DataRequired("bu alanı doldurmak zorunlu")])

    rememberMe = BooleanField("beni hatırla ")
    
    buton = SubmitField("Giriş yap")
