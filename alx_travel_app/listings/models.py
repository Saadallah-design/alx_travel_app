from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Listing(models.Model):
    PROPERTY_TYPE = [
        ('APARTMENT', 'Apartment'),
        ('HOUSE', 'House'),
        ('CONDO', 'Condominium'),
        ('CABIN', 'Cabin'),
        ('VILLA', 'Villa'),
        ('OTHER', 'Other'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=100, choices=PROPERTY_TYPE)

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    # Amenities: simplified one, can add others later
    has_air_conditioning = models.BooleanField(default=False)
    has_kitchen = models.BooleanField(default=False)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()

    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.ImageField(upload_to='listing_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # Host relationship
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at'] # to simplify the querying of latest listings first
        # this adds a database index on the created_at field for faster lookups (imporving performance)
        indexes = [
            models.Index(fields=['city', 'is_active']), 
            models.Index(fields=['price_per_night'])]
        # used indexes to speed up queries that filter or sort by created_at field

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(review.overall_rating for review in reviews) / reviews.count()
        return 0
    
    @property
    def review_count(self):
        return self.reviews.count()
    
    @property
    def is_available(self):
        return self.is_active and self.host.is_active


    def __str__(self):
        return self.title
    
class Booking(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        COMPLETED = 'COMPLETED', 'Completed'
        

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guest_bookings')

    # dates fields
    check_in = models.DateField()
    check_out = models.DateField()

    #guests
    num_guests = models.PositiveIntegerField()

    # locking price at the time of booking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # check in and out
    
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.PENDING)

    @property
    def num_nights(self):
        return (self.check_out - self.check_in).days

    @property
    def days_until_checkin(self):
        """Calculate days until check-in"""
        from django.utils import timezone
        if self.check_in > timezone.now().date():
            return (self.check_in - timezone.now().date()).days
        return 0

    @property
    def is_active(self):
        """Check if booking is active"""
        from django.utils import timezone
        today = timezone.now().date()
        return self.status == 'CONFIRMED' and self.check_in <= today <= self.check_out

    @property 
    def can_cancel(self):
        """Check if booking can be cancelled"""
        from django.utils import timezone
        if self.status == 'CANCELLED':
            return False
        return self.days_until_checkin > 2

    class Meta:
        ordering = ['-created_at'] # to simplify the querying of latest bookings first
        indexes = [
            models.Index(fields=['guest', 'status']),
            models.Index(fields=['listing', 'check_in', 'check_out']),
        ]

    def __str__(self):
        return f"Booking by {self.guest.username} for {self.listing.title}"
    
class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')


    overall_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )    

    is_verified = models.BooleanField(default=False) #from a completed booking
    comment = models.TextField()

    # host response
    host_response = models.TextField(blank=True, null=True)
    host_responded_at = models.DateTimeField(blank=True, null=True)

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def has_host_responded(self):
        return bool(self.host_response) # making it a simple boolean check

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.listing.title}"
    

# adding supportive models like Amenities, Photos, etc can be done later as needed
# like: LisingImage, Availability, Message, etc.