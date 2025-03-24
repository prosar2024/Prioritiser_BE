import smtplib

EMAIL = "admin@prosartech.com"
APP_PASSWORD = "8imXHDng965V"

try:
    server = smtplib.SMTP("smtp.zoho.com", 587)
    server.starttls()
    server.login(EMAIL, APP_PASSWORD)
    print("✅ Login successful")
    server.quit()
except smtplib.SMTPAuthenticationError as e:
    print("❌ Authentication failed:", e)
