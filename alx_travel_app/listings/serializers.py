from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - basic info only"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model with calculated fields"""
    host = UserSerializer(read_only=True)
    host_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='host', 
        write_only=True
    )
    
    # Include calculated properties as read-only fields
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Listing
        fields = [
            'id',
            'title',
            'description',
            'property_type',
            'address',
            'city',
            'country',
            'has_air_conditioning',
            'has_kitchen',
            'bedrooms',
            'bathrooms',
            'price_per_night',
            'image_url',
            'is_active',
            'host',
            'host_id',
            'average_rating',
            'review_count',
            'is_available',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_price_per_night(self, value):
        """Ensure price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price per night must be greater than 0.")
        return value
    
    # validating that the host or listing has at least 1 bedroom and 1 bathroom
    def validate(self, data):
        """Custom validation for the entire object"""
        if data.get('bedrooms', 0) < 1:
            raise serializers.ValidationError("Listing must have at least 1 bedroom.")
        if data.get('bathrooms', 0) < 1:
            raise serializers.ValidationError("Listing must have at least 1 bathroom.")
        return data


class ListingListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing lists (without full details)"""
    host_username = serializers.CharField(source='host.username', read_only=True)
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Listing
        fields = [
            'id',
            'title',
            'property_type',
            'city',
            'country',
            'price_per_night',
            'image_url',
            'bedrooms',
            'bathrooms',
            'host_username',
            'average_rating',
            'review_count',
            'is_active',
        ]


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model with validation"""
    guest = UserSerializer(read_only=True)
    guest_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='guest',
        write_only=True
    )
    
    listing_detail = ListingListSerializer(source='listing', read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(),
        source='listing',
        write_only=True
    )
    
    # Include calculated properties
    num_nights = serializers.ReadOnlyField()
    days_until_checkin = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    can_cancel = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id',
            'listing_id',
            'listing_detail',
            'guest',
            'guest_id',
            'check_in',
            'check_out',
            'num_guests',
            'num_nights',
            'price_per_night',
            'subtotal',
            'total_price',
            'status',
            'days_until_checkin',
            'is_active',
            'can_cancel',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 
            'price_per_night', 
            'subtotal', 
            'total_price', 
            'created_at', 
            'updated_at'
        ]
    
    def validate(self, data):
        """Validate booking dates and availability"""
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        
        # Validate check-out is after check-in
        if check_out <= check_in:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )
        
        # Validate dates are in the future
        today = timezone.now().date()
        if check_in < today:
            raise serializers.ValidationError(
                "Check-in date cannot be in the past."
            )
        
        # Validate num_guests doesn't exceed listing capacity
        listing = data.get('listing')
        num_guests = data.get('num_guests')
        
        if listing and num_guests:
            # Note: might add max_guests field to Listing model
            if num_guests < 1:
                raise serializers.ValidationError(
                    "Number of guests must be at least 1."
                )
        
        return data
    
    def create(self, validated_data):
        """Calculate and lock prices when creating booking"""
        listing = validated_data['listing']
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']
        
        # Calculate pricing
        num_nights = (check_out - check_in).days
        price_per_night = listing.price_per_night
        subtotal = price_per_night * num_nights
        total_price = subtotal  # Can add fees here later
        
        # Lock the prices
        validated_data['price_per_night'] = price_per_night
        validated_data['subtotal'] = subtotal
        validated_data['total_price'] = total_price
        
        return super().create(validated_data)


class BookingListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for booking lists"""
    guest_username = serializers.CharField(source='guest.username', read_only=True)
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    num_nights = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id',
            'listing_title',
            'guest_username',
            'check_in',
            'check_out',
            'num_nights',
            'total_price',
            'status',
            'created_at',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    reviewer = UserSerializer(read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        write_only=True
    )
    
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(),
        source='listing',
        write_only=True
    )
    
    booking_id = serializers.PrimaryKeyRelatedField(
        queryset=Booking.objects.all(),
        source='booking',
        write_only=True
    )
    
    # Include calculated property
    has_host_responded = serializers.ReadOnlyField()
    
    class Meta:
        model = Review
        fields = [
            'id',
            'listing_id',
            'booking_id',
            'reviewer',
            'reviewer_id',
            'overall_rating',
            'comment',
            'is_verified',
            'host_response',
            'host_responded_at',
            'has_host_responded',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'is_verified',
            'created_at',
            'updated_at',
        ]
    
    def validate_overall_rating(self, value):
        """Ensure rating is within valid range"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    
    def validate(self, data):
        """Validate review constraints"""
        booking = data.get('booking')
        
        # Ensure booking is completed before allowing review
        if booking and booking.status != Booking.STATUS_CHOICES.COMPLETED:
            raise serializers.ValidationError(
                "Reviews can only be created for completed bookings."
            )
        
        # Ensure reviewer is the guest who made the booking
        reviewer = data.get('reviewer')
        if booking and reviewer and booking.guest != reviewer:
            raise serializers.ValidationError(
                "Only the guest who made the booking can review it."
            )
        
        return data
    
    def create(self, validated_data):
        """Mark review as verified when created from completed booking"""
        booking = validated_data.get('booking')
        if booking and booking.status == Booking.STATUS_CHOICES.COMPLETED:
            validated_data['is_verified'] = True
        return super().create(validated_data)


""" lightweight serializer for review lists """

# class ReviewListSerializer(serializers.ModelSerializer):
#     """Lightweight serializer for review lists"""
#     reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)
#     listing_title = serializers.CharField(source='listing.title', read_only=True)
#     has_host_responded = serializers.ReadOnlyField()
    
#     class Meta:
#         model = Review
#         fields = [
#             'id',
#             'listing_title',
#             'reviewer_username',
#             'overall_rating',
#             'comment',
#             'is_verified',
#             'has_host_responded',
#             'created_at',
#         ]


# class HostResponseSerializer(serializers.ModelSerializer):
#     """Serializer for host to respond to reviews"""
#     class Meta:
#         model = Review
#         fields = ['host_response', 'host_responded_at']
#         read_only_fields = ['host_responded_at']
    
#     def update(self, instance, validated_data):
#         """Auto-set timestamp when host responds"""
#         if 'host_response' in validated_data:
#             validated_data['host_responded_at'] = timezone.now()
#         return super().update(instance, validated_data)
