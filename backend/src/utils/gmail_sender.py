import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from aiosmtplib import send

load_dotenv()

async def send_email_verification_code(to_email: str, verification_code: str) -> bool:
    from_email = os.getenv("APP_GMAIL")
    app_password = os.getenv("APP_GMAIL_PASS")
    
    if not from_email or not app_password:
        raise ValueError("Gmail credentials are not set in environment variables.")
    
    subject = "Email Verification Code"
    
    html_body = f"""
    <html>
        <body>
            <h2>Email Verification</h2>
            <p>Dear user,</p>
            <p>Your verification code is: <strong>{verification_code}</strong></p>
            <p>Please use this code to complete your verification process. If you did not request this, please ignore this email.</p>
            <br>
            <p>Best regards,</p>
            <p><strong>UETStoreChat Team</strong></p>
        </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html"))

    try:
        await send(
            message=msg,
            hostname="smtp.gmail.com",
            port=465,
            username=from_email,
            password=app_password,
            use_tls=True,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
