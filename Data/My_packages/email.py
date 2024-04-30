import smtplib
import random
class Mail():
    def send_to_mail(self,email,message):
        my_email="hmr778993@gmail.com"
        password="xpmx vyvl aalh lthy"
        connection=smtplib.SMTP("smtp.gmail.com",587)
        connection.starttls()
        connection.login(user=my_email,password=password)
        connection.sendmail(from_addr=my_email,to_addrs=f"{email}",msg=f"Subject:Hello testrunnn\n\n {message}")
        connection.close()
    def send_to_all(self,message):
        my_email="hmr778993@gmail.com"
        password="xpmx vyvl aalh lthy"
        connection=smtplib.SMTP("smtp.gmail.com",587)
        connection.starttls()
        connection.login(user=my_email,password=password)
        connection.sendmail(from_addr=my_email,to_addrs="hgp991554@gmail.com",msg=f"Subject:Hello testrunnn\n\n{message}")
        connection.close()