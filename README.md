# ALX Travel App

> **A Django-based travel listing platform for booking accommodations**

## About the Project

The **ALX Travel App** is a real-world Django application that serves as the foundation for a travel listing platform. This milestone focuses on setting up the initial project structure, configuring a robust database, and integrating tools to ensure API documentation and maintainable configurations. The aim is to equip learners with industry-standard best practices for starting and managing Django-based projects efficiently.

## Current Milestone: 0x00 - Foundation

This milestone teaches you to set up a scalable backend, integrate MySQL for database management, and use Swagger for automated API documentation. These foundational steps are critical in preparing the application for future features and seamless team collaboration.

### What's Been Implemented

✅ **Core Models**
- Listing model with property types, amenities, and pricing
- Booking model with locked pricing and status management
- Review model with ratings and host responses
- Calculated properties for dynamic data
- Strategic database indexes for performance

✅ **Serializers**
- Complete DRF serializers for all models
- Validation logic for bookings and reviews
- Automatic price calculation and locking
- Lightweight serializers for list views

✅ **Database Management**
- MySQL integration with PyMySQL
- Environment-based configuration
- Custom management command for seeding sample data

✅ **Project Structure**
- Django 5.2 with REST Framework
- CORS headers for API access
- Swagger/OpenAPI documentation setup
- Git version control

### Learning Objectives

As a professional developer, this task enables you to:

**Master Advanced Project Initialization:**
- Bootstrap Django projects with modular, production-ready configurations
- Employ environment variable management for secure and scalable settings
- Design robust database models with relationships and constraints

**Integrate Key Developer Tools:**
- Set up and use Swagger (via drf-yasg) for API documentation
- Implement CORS headers and MySQL configurations for robust API interactions
- Create serializers with validation for RESTful APIs

**Collaborate Effectively Using Git:**
- Structure your projects for team collaboration with version-controlled setup
- Use branching strategies for feature development

**Adopt Industry Best Practices:**
- Follow best practices in managing dependencies, database configurations, and application structure
- Understand when to store vs calculate data
- Implement data seeding for testing and development

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
cd alx_travel_app
python manage.py migrate

# Seed sample data
python manage.py seed --clear

# Start development server
python manage.py runserver
```

## Next Steps

- [ ] Implement API views and endpoints
- [ ] Add authentication and permissions
- [ ] Create API tests
- [ ] Build search and filtering functionality

For detailed documentation, see `README_OVERVIEW.md`
