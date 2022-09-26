import ssl
import smtplib
from email.message import EmailMessage


def sendmail(email_receiver=None, purchase=None, payment_method=None, total_price=None, branch=None, takedate=None):
    try:
        email_sender = 'sohin0121@gmail.com'
        # can change to list when sender to many people
        email_receiver = str(email_receiver)
        # os.get.enviro(PASSWORD}mail.py
        email_passwaord = 'kqms gpkt cbsh icpj'
        subject = "Receipt from Alex's supermarket"
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = ','.join(email_receiver)  # ','.join(email_receiver)
        em['subject'] = subject
        em.set_content(f'Dear customers,\n\n\n'
                       f'We are glad to inform that your order has been confirmed\n'
                       f'Your order are shown here:\n\n'
                       f'{purchase}\n'
                       f'Payment by {payment_method}\n final price:{total_price}\n'
                       f'Take Address:{branch}\n'
                       f'Take Date:{takedate}\n'
                       f'welcome to your next visit\n\n\n'
                       f'Best Regards,\n'
                       f'Alex So,\n'
                       f'Alex supermarket')
        if email_receiver == None or purchase == None:
            return 'Cannot send confirmation!Error occur on your email!'

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_passwaord)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            return True
    except:
        return 'Cannot send confirmation!Error occur on your email!'
