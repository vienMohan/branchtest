from django.db import models
from django.utils.text import slugify
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
import random
from datetime import date
from django.core.validators import RegexValidator

class Candidate(models.Model):
    id = models.CharField(primary_key=True, max_length=50, editable=False)    
    name = models.CharField(max_length=255)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed."
    )
    number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    created_at = models.DateField(auto_now_add=True)
    gmail = models.EmailField(max_length=255)
    score = models.IntegerField(null=True, blank=True)
    topic = models.CharField(max_length=20, null=True, blank=True)
    tech_score = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True, null=True)

    dob = models.DateField(default=date(2000, 1, 1))  # ✅ Fixed

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer not to say', 'Prefer not to say'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)

    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Other', 'Other'),
    ]
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)
    nationality = models.CharField(max_length=100)

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)

    position_applied = models.CharField(max_length=255)

    DEPARTMENT_CHOICES = [
        ('IT', 'IT'), ('HR', 'HR'), ('Networking', 'Networking'),
        ('Digital Marketing', 'Digital Marketing'), ('Operations', 'Operations'),
        ('Sales', 'Sales'), ('Other', 'Other'),
    ]
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)

    ug_qualification = models.CharField(max_length=255)
    ug_category = models.CharField(max_length=255, null=True, blank=True)
    year_of_graduation = models.CharField(max_length=4)
    current_employer = models.CharField(max_length=255, null=True, blank=True)  # ✅ Fix
    total_experience = models.CharField(max_length=100, null=True, blank=True)  # ✅ Fix
    relevant_experience = models.CharField(max_length=255, blank=True, null=True)
    skills_certifications = models.TextField(blank=True, null=True)

    pg_qualification = models.CharField(max_length=255, blank=True, null=True)
    pg_category = models.CharField(max_length=255, null=True, blank=True)  # ✅ Remove duplicate
    year_of_pg_graduation = models.CharField(max_length=4, blank=True, null=True)

    resume_upload = models.FileField(upload_to="images")
    photo_upload = models.ImageField(upload_to="images")

    DEGREE_TYPE_CHOICES = [
        ('UG', 'Undergraduate (UG)'),
        ('PG', 'Postgraduate (PG)'),
        ('Diploma', 'Diploma'),
    ]
    degrees = models.CharField(max_length=100, help_text="Comma-separated: UG,PG,Diploma", null=True, blank=True)

    pg_degree_name = models.CharField(max_length=255, null=True, blank=True)

    payslip_upload = models.FileField(upload_to="images", blank=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    confirm_password = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
    # Generate custom ID if not already set
        if not self.id:
            prefix = "CANDIDATE_VN_CUST_"
            last_customer = Candidate.objects.filter(id__startswith=prefix).order_by('-id').first()
            if last_customer:
                last_id = int(last_customer.id.split('_')[-1])
                new_id = f"{prefix}{last_id + 1:03d}"
            else:
                new_id = f"{prefix}001"
            self.id = new_id

        # Call original save to persist other fields
        super().save(*args, **kwargs)

        # Now update slug if it's missing
        if not self.slug:
            self.slug = slugify(f"{self.name}_{self.id}")
            super().save(update_fields=["slug"])


    def __str__(self):
        return self.name

    
class OTPVerification(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)
    
class PhoneOTPVerification(models.Model):
    number = models.CharField(max_length=15,null=True, blank=True)
    otp = models.CharField(max_length=6,null=True, blank=True   )
    created_at = models.DateTimeField(default=timezone.now,null=True, blank=True)
    verified = models.BooleanField(default=False, null=True, blank=True )

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)


class CompanyDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    company_name = models.CharField(max_length=255)
    company_location = models.CharField(max_length=255)
    company_email = models.EmailField()
    company_phone = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', message="Phone number must be 10 digits")]
    )
        
    company_social_media_Linkedin = models.JSONField(default=list, blank=True)
    company_social_media_Instagram = models.JSONField(default=list, blank=True)
    company_social_media_Facebook = models.JSONField(default=list, blank=True)
    company_social_media_Twitter = models.JSONField(default=list, blank=True)
    company_social_media_Whatsapp_group = models.JSONField(default=list, blank=True)
    company_department = models.CharField(max_length=255, blank=True, null=True)
    company_employees = models.IntegerField()
    company_weblink = models.URLField(blank=True, null=True)
    start_year = models.IntegerField()
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    net_profit = models.DecimalField(max_digits=12, decimal_places=2)
    company_branch_no = models.CharField(max_length=100, blank=True, null=True)
    company_certification = models.CharField(max_length=100, blank=True, null=True)
    company_license = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.company_name
    
class Openings(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    job_description = models.TextField()
    requirements = models.TextField()
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    opening_date = models.DateField(auto_now_add=True)
    closing_date = models.DateField()
    
    def __str__(self):
        return f"{self.position} at {self.company.company_name}"