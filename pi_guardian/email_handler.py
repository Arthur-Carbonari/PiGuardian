
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
import time

class EmailHandler:

    email_address = 'piguard81@gmail.com'
    email_password = 'cdbtonhgyjkjwhzz'
    email_server = 'smtp.gmail.com'
    email_port = 587

    email_timeout = 600
    last_email_time = 0

    def send_email(self, destination_address, image):

        current_time = time.time()

        if current_time - self.last_email_time < 30:
            return
        
        self.last_email_time = current_time

        msg = MIMEMultipart()
        msg['Subject'] = 'Automated Email'
        msg['From'] = self.email_address
        msg['To'] = 'arthurcarbonari99@gmail.com'

        msg.attach(MIMEText("An unkown person was spotted at one of your protected locations", 'plain'))

        # Load the image file
        image_path = 'dataset/arthur_martins/pic1.jpg'
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        # Create an image attachment
        image_attachment = MIMEImage(image_data)
        image_attachment.add_header('Content-Disposition', 'attachment', filename='image.jpg')
        msg.attach(image_attachment)

        with smtplib.SMTP(self.email_server, self.email_port) as server:
            server.starttls()
            server.login(self.email_address, self.email_password)
            server.sendmail(self.email_address, msg['To'], msg.as_string())

