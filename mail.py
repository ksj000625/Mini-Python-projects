import getpass                                                                                             
import smtplib                                                                        
HOST = "smtp.gmail.com"                                                                                  
PORT = 465
email = input("Enter email : ")
username = email                                                                            
password = getpass.getpass("Provide Gmail password: ")
server = smtplib.SMTP_SSL(HOST, PORT)

server.login(username, password)

text = input("Enter the mail text : \n")
to = input("Enter recepient email : ")

server.sendmail(
    "from@domain.com",
    to,
    text,
)

server.quit();
