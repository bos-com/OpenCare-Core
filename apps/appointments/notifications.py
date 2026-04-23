"""
Notification hooks for appointment events with email/SMS support.
"""

import logging
from typing import Literal, Optional
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Appointment

logger = logging.getLogger(__name__)

AppointmentEvent = Literal["created", "updated", "cancelled", "reminder"]


def send_email_notification(
    appointment: Appointment,
    event: AppointmentEvent,
    recipient_email: str,
    recipient_name: str
) -> bool:
    """
    Send email notification for appointment events.
    
    Returns True if email was sent successfully, False otherwise.
    """
    try:
        subject = _get_email_subject(appointment, event)
        message = _get_email_message(appointment, event, recipient_name)
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@opencare-africa.com")
        
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        logger.info(f"Email sent to {recipient_email} for appointment {appointment.id} event {event}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
        return False


def send_sms_notification(
    appointment: Appointment,
    event: AppointmentEvent,
    recipient_phone: str,
    recipient_name: str
) -> bool:
    """
    Send SMS notification for appointment events.
    
    This is a hook for SMS providers. In production, integrate with:
    - Twilio
    - AWS SNS
    - Africa's Talking
    - Other SMS gateway services
    
    Returns True if SMS was sent successfully, False otherwise.
    """
    try:
        message = _get_sms_message(appointment, event, recipient_name)
        
        # TODO: Integrate with actual SMS provider
        # Example with Twilio:
        # from twilio.rest import Client
        # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # client.messages.create(
        #     body=message,
        #     from_=settings.TWILIO_PHONE_NUMBER,
        #     to=recipient_phone
        # )
        
        # For now, log the SMS that would be sent
        logger.info(f"SMS would be sent to {recipient_phone}: {message}")
        logger.info(f"SMS notification for appointment {appointment.id} event {event}")
        return True
    except Exception as e:
        logger.error(f"Failed to send SMS to {recipient_phone}: {str(e)}")
        return False


def _get_email_subject(appointment: Appointment, event: AppointmentEvent) -> str:
    """Generate email subject based on event type."""
    subjects = {
        "created": f"Appointment Scheduled - {appointment.start_time.strftime('%B %d, %Y at %I:%M %p')}",
        "updated": f"Appointment Updated - {appointment.start_time.strftime('%B %d, %Y at %I:%M %p')}",
        "cancelled": f"Appointment Cancelled - {appointment.start_time.strftime('%B %d, %Y at %I:%M %p')}",
        "reminder": f"Appointment Reminder - {appointment.start_time.strftime('%B %d, %Y at %I:%M %p')}",
    }
    return subjects.get(event, "Appointment Notification")


def _get_email_message(appointment: Appointment, event: AppointmentEvent, recipient_name: str) -> str:
    """Generate email message body."""
    provider_name = appointment.provider.get_full_name()
    patient_name = appointment.patient.get_full_name()
    facility_name = appointment.facility.name
    
    messages = {
        "created": f"""
Hello {recipient_name},

Your appointment has been scheduled:

Patient: {patient_name}
Provider: {provider_name}
Facility: {facility_name}
Date & Time: {appointment.start_time.strftime('%B %d, %Y at %I:%M %p')}
Duration: {appointment.duration_minutes} minutes
Type: {appointment.appointment_type or 'General Consultation'}
Reason: {appointment.reason or 'Not specified'}

Please arrive 10 minutes before your scheduled time.

Thank you,
OpenCare-Africa Team
        """,
        "updated": f"""
Hello {recipient_name},

Your appointment has been updated:

Patient: {patient_name}
Provider: {provider_name}
Facility: {facility_name}
New Date & Time: {appointment.start_time.strftime('%B %d, %Y at %I:%M %p')}
Duration: {appointment.duration_minutes} minutes

Please note the new time and arrive 10 minutes early.

Thank you,
OpenCare-Africa Team
        """,
        "cancelled": f"""
Hello {recipient_name},

Your appointment has been cancelled:

Patient: {patient_name}
Provider: {provider_name}
Facility: {facility_name}
Original Date & Time: {appointment.start_time.strftime('%B %d, %Y at %I:%M %p')}

If you need to reschedule, please contact the facility or book a new appointment.

Thank you,
OpenCare-Africa Team
        """,
        "reminder": f"""
Hello {recipient_name},

This is a reminder about your upcoming appointment:

Patient: {patient_name}
Provider: {provider_name}
Facility: {facility_name}
Date & Time: {appointment.start_time.strftime('%B %d, %Y at %I:%M %p')}
Duration: {appointment.duration_minutes} minutes

Please arrive 10 minutes before your scheduled time.

Thank you,
OpenCare-Africa Team
        """,
    }
    return messages.get(event, "Appointment notification").strip()


def _get_sms_message(appointment: Appointment, event: AppointmentEvent, recipient_name: str) -> str:
    """Generate SMS message body (shorter than email)."""
    provider_name = appointment.provider.get_full_name()
    date_str = appointment.start_time.strftime('%b %d, %Y at %I:%M %p')
    
    messages = {
        "created": f"Appointment scheduled: {date_str} with {provider_name} at {appointment.facility.name}. Arrive 10 mins early.",
        "updated": f"Appointment updated: {date_str} with {provider_name} at {appointment.facility.name}.",
        "cancelled": f"Appointment cancelled: {date_str} with {provider_name}. Contact facility to reschedule.",
        "reminder": f"Reminder: Appointment tomorrow {date_str} with {provider_name} at {appointment.facility.name}.",
    }
    return messages.get(event, "Appointment notification")


def send_notification(appointment: Appointment, event: AppointmentEvent) -> None:
    """
    Dispatch notifications for appointment changes via email and SMS.
    
    Sends notifications to both patient and provider when appropriate.
    """
    logger.info(
        "Appointment %s: patient=%s provider=%s start=%s status=%s",
        event,
        appointment.patient_id,
        appointment.provider_id,
        appointment.start_time.isoformat(),
        appointment.status,
    )
    
    notifications_sent = []
    
    # Send to patient
    if appointment.patient.email:
        email_sent = send_email_notification(
            appointment, event,
            appointment.patient.email,
            appointment.patient.get_full_name()
        )
        if email_sent:
            notifications_sent.append({"type": "email", "recipient": "patient", "method": "email", "sent_at": timezone.now().isoformat()})
    
    if appointment.patient.phone_number:
        sms_sent = send_sms_notification(
            appointment, event,
            appointment.patient.phone_number,
            appointment.patient.get_full_name()
        )
        if sms_sent:
            notifications_sent.append({"type": "sms", "recipient": "patient", "method": "sms", "sent_at": timezone.now().isoformat()})
    
    # Send to provider
    if appointment.provider.email:
        email_sent = send_email_notification(
            appointment, event,
            appointment.provider.email,
            appointment.provider.get_full_name()
        )
        if email_sent:
            notifications_sent.append({"type": "email", "recipient": "provider", "method": "email", "sent_at": timezone.now().isoformat()})
    
    if appointment.provider.phone_number:
        sms_sent = send_sms_notification(
            appointment, event,
            appointment.provider.phone_number,
            appointment.provider.get_full_name()
        )
        if sms_sent:
            notifications_sent.append({"type": "sms", "recipient": "provider", "method": "sms", "sent_at": timezone.now().isoformat()})
    
    # Update appointment with notification history
    existing_notifications = list(appointment.notifications_sent or [])
    existing_notifications.extend(notifications_sent)
    Appointment.objects.filter(pk=appointment.pk).update(notifications_sent=existing_notifications)
