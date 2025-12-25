"""
Notification hooks for appointment events.
"""

import logging
from typing import Literal

from .models import Appointment

logger = logging.getLogger(__name__)

AppointmentEvent = Literal["created", "updated", "cancelled"]


def send_notification(appointment: Appointment, event: AppointmentEvent) -> None:
    """
    Dispatch notifications for appointment changes.

    In production this should integrate with email/SMS providers. For now we
    log the event so downstream systems can subscribe.
    """
    logger.info(
        "Appointment %s: patient=%s provider=%s start=%s status=%s",
        event,
        appointment.patient_id,
        appointment.provider_id,
        appointment.start_time.isoformat(),
        appointment.status,
    )
    notifications = list(appointment.notifications_sent or [])
    notifications.append(event)
    Appointment.objects.filter(pk=appointment.pk).update(notifications_sent=notifications)
