# Email backend configuration (for development, use console backend)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production, use SMTP backend:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your_gmail@gmail.com'
# EMAIL_HOST_PASSWORD = 'your_gmail_app_password'

# CORS settings (if frontend is on a different port)
CORS_ALLOW_ALL_ORIGINS = True