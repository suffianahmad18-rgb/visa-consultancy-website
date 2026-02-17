def site_settings(request):
    return {
        'site_name': 'Uni World Consultancy',
        'site_description': 'Professional Visa Consultation Services in Gujranwala',
        'study_destinations_title': 'Study Destinations',
        'contact_email': 'info@gujranwalavisaconsultancy.com',
        'contact_phone': '+92 33 44476332',
        'contact_address': 'CB 181, Kashmir Colony Rahwali Cantt, Gujranwala, Punjab 52350, Pakistan',
        'site_url': request.build_absolute_uri('/')[:-1],
        'office_city': 'Gujranwala',
        'office_country': 'Pakistan',
    }

def unread_messages_count(request):
    if request.user.is_authenticated:
        from messaging.models import Message
        if request.user.is_staff:
            # For admin: count all unread messages where admin is receiver
            count = Message.objects.filter(receiver__is_staff=True, is_read=False).count()
        else:
            # For regular users: count their own unread messages
            count = Message.objects.filter(receiver=request.user, is_read=False).count()
        return {'unread_count': count}
    return {'unread_count': 0}