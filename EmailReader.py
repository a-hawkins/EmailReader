import smtplib
import time
import imaplib
import email
import datetime


ORG_EMAIL   = "@[domain].com"     # Ex. @gmail.com or @outlook.com
FROM_EMAIL  = "[example]" + ORG_EMAIL
FROM_PWD    = "[password]"        
SMTP_SERVER = "smtp.gmail.com"  # smpt.outlook.com for outlook
SMTP_PORT   = 587               # 587 for both gmail and outlook


def read_new_email():
#--------------------------------------------------------------------------------
#
# Info: This method connects to an email, and writes the contents of new emails 
#       new text file.
#       In the current version, if there are no new emails, a new file is still 
#       created.
#
#--------------------------------------------------------------------------------
    try:
        ### Create Output File ###
        now = datetime.datetime.now()
        outfile = open("NewMail" + (now.strftime("%Y-%m-%d_%H.%M.%S")) + ".txt","a")

        ### Log in and connect ###
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        ### Identify messages to be read ###
        mail.select('inbox')
        #typ, data = mail.search(None, 'ALL') # Reads ALL messages
        typ, data = mail.search(None, '(Unseen)') # Reads just new messages
        unread_msgs = data[0].split()

        ### Write content to file ###
        for num in unread_msgs:
            typ, data = mail.fetch(num, '(UID BODY[TEXT])') # Grabs just the body text vomit
            #typ, data = mail.fetch(num,'(RFC822)' )  # Grabs all the text vomit
            outfile.write('Message %s\n%s\n' % (num, data[0][1]))
        outfile.write("============================ END OF FILE ============================")
            
        ### Mark them as seen ###
        for num in unread_msgs:
            mail.store(num, '+FLAGS', '\Seen')
        mail.close()
        mail.logout()
                    
    except Exception as e:
        print ('ERROR: ' + str(e) + ' :(')

read_new_email()
