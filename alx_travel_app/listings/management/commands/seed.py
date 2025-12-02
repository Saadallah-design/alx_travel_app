from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample listings, bookings, and reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Listing.objects.all().delete()
            # Don't delete users, just listings data
            self.stdout.write(self.style.SUCCESS('Data cleared!'))

        # Create sample users (hosts and guests)
        self.stdout.write('Creating users...')
        hosts = self.create_users('host', 5)
        guests = self.create_users('guest', 10)
        self.stdout.write(self.style.SUCCESS(f'Created {len(hosts)} hosts and {len(guests)} guests'))

        # Create sample listings
        self.stdout.write('Creating listings...')
        listings = self.create_listings(hosts)
        self.stdout.write(self.style.SUCCESS(f'Created {len(listings)} listings'))

        # Create sample bookings
        self.stdout.write('Creating bookings...')
        bookings = self.create_bookings(listings, guests)
        self.stdout.write(self.style.SUCCESS(f'Created {len(bookings)} bookings'))

        # Create sample reviews
        self.stdout.write('Creating reviews...')
        reviews = self.create_reviews(bookings)
        self.stdout.write(self.style.SUCCESS(f'Created {len(reviews)} reviews'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))

    def create_users(self, prefix, count):
        """Create sample users"""
        users = []
        for i in range(1, count + 1):
            username = f'{prefix}{i}'
            email = f'{username}@example.com'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': username.capitalize(),
                    'last_name': 'User',
                    'is_active': True,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        return users

    def create_listings(self, hosts):
        """Create sample listings"""
        cities = [
            ('New York', 'USA'),
            ('Paris', 'France'),
            ('Tokyo', 'Japan'),
            ('London', 'UK'),
            ('Barcelona', 'Spain'),
            ('Dubai', 'UAE'),
            ('Sydney', 'Australia'),
            ('Rome', 'Italy'),
            ('Bangkok', 'Thailand'),
            ('Istanbul', 'Turkey'),
        ]

        property_types = ['APARTMENT', 'HOUSE', 'CONDO', 'CABIN', 'VILLA']
        
        adjectives = ['Cozy', 'Luxury', 'Modern', 'Charming', 'Spacious', 'Beautiful', 'Elegant', 'Stunning']
        nouns = ['Studio', 'Apartment', 'Loft', 'Villa', 'House', 'Suite', 'Retreat']

        listings = []
        for i in range(30):
            city, country = random.choice(cities)
            property_type = random.choice(property_types)
            title = f"{random.choice(adjectives)} {random.choice(nouns)} in {city}"
            
            listing = Listing.objects.create(
                title=title,
                description=f"Experience the best of {city} in this {title.lower()}. "
                           f"Perfect for travelers looking for comfort and convenience. "
                           f"Close to major attractions and public transportation.",
                property_type=property_type,
                address=f"{random.randint(1, 999)} {random.choice(['Main', 'Oak', 'Maple', 'Park', 'Lake'])} Street",
                city=city,
                country=country,
                has_air_conditioning=random.choice([True, False]),
                has_kitchen=random.choice([True, True, False]),  # More likely to have kitchen
                bedrooms=random.randint(1, 4),
                bathrooms=random.randint(1, 3),
                price_per_night=random.randint(50, 500),
                is_active=True,
                host=random.choice(hosts),
            )
            listings.append(listing)
        
        return listings

    def create_bookings(self, listings, guests):
        """Create sample bookings with various statuses"""
        bookings = []
        statuses = [
            Booking.STATUS_CHOICES.COMPLETED,
            Booking.STATUS_CHOICES.CONFIRMED,
            Booking.STATUS_CHOICES.PENDING,
            Booking.STATUS_CHOICES.CANCELLED,
        ]
        
        today = timezone.now().date()
        
        for i in range(50):
            listing = random.choice(listings)
            guest = random.choice(guests)
            status = random.choice(statuses)
            
            # Generate dates based on status
            if status == Booking.STATUS_CHOICES.COMPLETED:
                # Past bookings
                check_in = today - timedelta(days=random.randint(30, 180))
                check_out = check_in + timedelta(days=random.randint(2, 14))
            elif status == Booking.STATUS_CHOICES.CONFIRMED:
                # Upcoming bookings
                check_in = today + timedelta(days=random.randint(5, 60))
                check_out = check_in + timedelta(days=random.randint(2, 14))
            elif status == Booking.STATUS_CHOICES.PENDING:
                # Recent pending bookings
                check_in = today + timedelta(days=random.randint(10, 30))
                check_out = check_in + timedelta(days=random.randint(2, 7))
            else:  # CANCELLED
                # Cancelled bookings (past or future)
                check_in = today + timedelta(days=random.randint(-30, 30))
                check_out = check_in + timedelta(days=random.randint(2, 7))
            
            # Calculate pricing
            num_nights = (check_out - check_in).days
            price_per_night = listing.price_per_night
            subtotal = price_per_night * num_nights
            total_price = subtotal
            
            booking = Booking.objects.create(
                listing=listing,
                guest=guest,
                check_in=check_in,
                check_out=check_out,
                num_guests=random.randint(1, 4),
                price_per_night=price_per_night,
                subtotal=subtotal,
                total_price=total_price,
                status=status,
            )
            bookings.append(booking)
        
        return bookings

    def create_reviews(self, bookings):
        """Create reviews for completed bookings"""
        reviews = []
        
        # Only create reviews for completed bookings
        completed_bookings = [b for b in bookings if b.status == Booking.STATUS_CHOICES.COMPLETED]
        
        # Review about 70% of completed bookings
        bookings_to_review = random.sample(
            completed_bookings, 
            int(len(completed_bookings) * 0.7)
        )
        
        positive_comments = [
            "Amazing place! Highly recommend.",
            "The host was very welcoming and the place was spotless.",
            "Perfect location and great amenities. Will book again!",
            "Exceeded our expectations. Beautiful and comfortable.",
            "Great value for money. Loved our stay!",
        ]
        
        neutral_comments = [
            "Nice place, but could use some updates.",
            "Decent stay. Met our basic needs.",
            "Good location, average amenities.",
            "It was okay. Nothing special but not bad either.",
        ]
        
        negative_comments = [
            "Not as described. Disappointed with cleanliness.",
            "Location was inconvenient and noisy.",
            "Poor communication with host. Would not recommend.",
            "Overpriced for what you get.",
        ]
        
        for booking in bookings_to_review:
            rating = random.randint(1, 5)
            
            # Choose comment based on rating
            if rating >= 4:
                comment = random.choice(positive_comments)
            elif rating == 3:
                comment = random.choice(neutral_comments)
            else:
                comment = random.choice(negative_comments)
            
            review = Review.objects.create(
                listing=booking.listing,
                booking=booking,
                reviewer=booking.guest,
                overall_rating=rating,
                comment=comment,
                is_verified=True,  # Completed booking = verified
            )
            
            # Add host response to some reviews (about 50%)
            if random.random() < 0.5:
                host_responses = [
                    "Thank you for your wonderful review! We're glad you enjoyed your stay.",
                    "We appreciate your feedback and hope to host you again soon!",
                    "Thanks for staying with us! Your feedback means a lot.",
                    "We're sorry to hear about your experience. We're working to improve.",
                    "Thank you for your honest feedback. We'll address these issues.",
                ]
                review.host_response = random.choice(host_responses)
                review.host_responded_at = timezone.now() - timedelta(days=random.randint(1, 30))
                review.save()
            
            reviews.append(review)
        
        return reviews
