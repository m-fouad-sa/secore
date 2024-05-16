from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
import uuid

User = get_user_model()

class TimeStampedUUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


# Create your models here.
class Client(TimeStampedUUIDModel):
    
    name = models.CharField(
        verbose_name=_("organization name"), max_length=255, unique=True
    )
    owner = models.OneToOneField(User, related_name="owner", on_delete=models.CASCADE)
    
    client_country = CountryField(
        verbose_name=_("country"), default="UK", blank=False, null=False
    )
    phone_number = PhoneNumberField(
        verbose_name=_("organization phone number"), max_length=30, default="+123456789"
    )
    client_email = models.EmailField(
        verbose_name=_("organization email address"), unique=True
    )
    client_description= models.TextField(max_length=500)
    
    logo_photo = models.ImageField(
        verbose_name=_("organization logo"), default="/logo_default.png"
    )
    
    
    def __str__(self):
        return f"{self.name} {self.client_country}"
    

    
class currency(models.Model):
    # Other fields in your model
    
    # Define currency choices
    CURRENCY_CHOICES = (
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('AUD', 'Australian Dollar'),
        ('CAD', 'Canadian Dollar'),
        ('CHF', 'Swiss Franc'),
        ('CNY', 'Chinese Yuan'),
        ('INR', 'Indian Rupee'),
        ('SGD', 'Singapore Dollar'),
        ('HKD', 'Hong Kong Dollar'),
        ('NZD', 'New Zealand Dollar'),
        ('SEK', 'Swedish Krona'),
        ('KRW', 'South Korean Won'),
        ('RUB', 'Russian Ruble'),
        ('ZAR', 'South African Rand'),
        ('BRL', 'Brazilian Real'),
        ('NOK', 'Norwegian Krone'),
        ('MXN', 'Mexican Peso'),
        ('TRY', 'Turkish Lira'),
        ('PLN', 'Polish Złoty'),
        ('THB', 'Thai Baht'),
        ('IDR', 'Indonesian Rupiah'),
        ('MYR', 'Malaysian Ringgit'),
        ('PHP', 'Philippine Peso'),
        ('CZK', 'Czech Koruna'),
        ('HUF', 'Hungarian Forint'),
        ('ILS', 'Israeli Shekel'),
        ('DKK', 'Danish Krone'),
        ('CLP', 'Chilean Peso'),
        ('AED', 'United Arab Emirates Dirham'),
        ('COP', 'Colombian Peso'),
        ('SAR', 'Saudi Riyal'),
        ('ARS', 'Argentine Peso'),
        ('TWD', 'New Taiwan Dollar'),
        ('VND', 'Vietnamese Đồng'),
        ('UAH', 'Ukrainian Hryvnia'),
        ('NGN', 'Nigerian Naira'),
        ('EGP', 'Egyptian Pound'),
        ('BDT', 'Bangladeshi Taka'),
        ('IQD', 'Iraqi Dinar'),
        ('QAR', 'Qatari Riyal'),
        ('KWD', 'Kuwaiti Dinar'),
        ('PKR', 'Pakistani Rupee'),
        ('OMR', 'Omani Rial'),
        ('LBP', 'Lebanese Pound'),
        ('JOD', 'Jordanian Dinar'),
        ('BHD', 'Bahraini Dinar'),
        ('GEL', 'Georgian Lari'),
        ('LKR', 'Sri Lankan Rupee'),
        ('GHS', 'Ghanaian Cedi'),
        ('MAD', 'Moroccan Dirham'),
        ('ETB', 'Ethiopian Birr'),
        ('NPR', 'Nepalese Rupee'),
        ('CRC', 'Costa Rican Colón'),
        ('HRK', 'Croatian Kuna'),
        ('BND', 'Brunei Dollar'),
        ('DZD', 'Algerian Dinar'),
        ('ISK', 'Icelandic Króna'),
        ('BYN', 'Belarusian Ruble'),
        ('LYD', 'Libyan Dinar'),
        ('ALL', 'Albanian Lek'),
        ('UYU', 'Uruguayan Peso'),
        ('UZS', 'Uzbekistani Som'),
        ('XAF', 'Central African CFA Franc'),
        ('RSD', 'Serbian Dinar'),
        ('AFA', 'Afghan Afghani'),
        ('XOF', 'West African CFA Franc'),
        ('MKD', 'Macedonian Denar'),
        ('TZS', 'Tanzanian Shilling'),
        ('GEL', 'Georgian Lari'),
        ('DOP', 'Dominican Peso'),
        ('UGX', 'Ugandan Shilling'),
        ('KZT', 'Kazakhstani Tenge'),
        ('MZN', 'Mozambican Metical'),
        ('YER', 'Yemeni Rial'),
        ('SSP', 'South Sudanese Pound'),
        ('XCD', 'East Caribbean Dollar'),
        ('SYP', 'Syrian Pound'),
        ('SCR', 'Seychellois Rupee'),
        ('NAD', 'Namibian Dollar'),
        ('BWP', 'Botswana Pula'),
        ('BBD', 'Barbadian Dollar'),
        ('TND', 'Tunisian Dinar'),
        ('MOP', 'Macanese Pataca'),
        ('HNL', 'Honduran Lempira'),
        ('BZD', 'Belize Dollar'),
        ('FJD', 'Fijian Dollar'),
        ('BSD', 'Bahamian Dollar'),
        ('GYD', 'Guyanese Dollar'),
        ('SRD', 'Surinamese Dollar'),
        ('MVR', 'Maldivian Rufiyaa'),
        ('KHR', 'Cambodian Riel'),
        ('GMD', 'Gambian Dalasi'),
        ('MWK', 'Malawian Kwacha'),
        ('AOA', 'Angolan Kwanza'),
        ('PGK', 'Papua New Guinean Kina'),
        ('XPF', 'CFP Franc'),
        ('SLL', 'Sierra Leonean Leone'),
        ('NIO', 'Nicaraguan Córdoba'),
        ('BMD', 'Bermudian Dollar'),
        ('LSL', 'Lesotho Loti'),
        ('LAK', 'Laotian Kip'),
        ('SZL', 'Swazi Lilangeni'),
        ('CVE', 'Cape Verdean Escudo'),
        ('FKP', 'Falkland Islands Pound'),
        ('BTN', 'Bhutanese Ngultrum'),
        ('GIP', 'Gibraltar Pound'),
        ('SHP', 'Saint Helena Pound'),
        ('GGP', 'Guernsey Pound'),
        ('IMP', 'Isle of Man Pound'),
        ('JEP', 'Jersey Pound'),
        ('SVC', 'Salvadoran Colón'),
        ('TMT', 'Turkmenistani Manat'),
        ('ERN', 'Eritrean Nakfa'),
        ('TJS', 'Tajikistani Somoni'),
        ('SOS', 'Somali Shilling'),
        ('FKP', 'Falkland Islands Pound'),
        ('SDG', 'Sudanese Pound'),
        ('SSP', 'South Sudanese Pound'),
        ('VEF', 'Venezuelan Bolívar'),
        ('VEB', 'Venezuelan Bolívar (old)'),
        ('ZMW', 'Zambian Kwacha'),
        ('ZWL', 'Zimbabwean Dollar'),
        ('ZMK', 'Zambian Kwacha (pre-2013)'),
    )
    
    # Define currency abbreviation field with choices
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    def __str__(self):
        return f"{self.currency}"