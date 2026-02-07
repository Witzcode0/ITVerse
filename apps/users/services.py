from django.db.models import Q
from apps.users.models import User, Connection

def send_connection_request(sender, receiver):
    if sender == receiver:
        return None

    connection, created = Connection.objects.get_or_create(
        sender=sender,
        receiver=receiver
    )
    return connection

def accept_connection(sender, receiver):
    try:
        connection = Connection.objects.get(
            sender=sender,
            receiver=receiver
        )
        connection.is_accepted = True
        connection.save()
        return True
    except Connection.DoesNotExist:
        return False
    
def pending_connection_request(receiver):
    return Connection.objects.filter(
            receiver=receiver,
            is_accepted=False
        )

def get_connected_users(user):
    return User.objects.filter(
        Q(sent_requests__receiver=user, sent_requests__is_accepted=True) |
        Q(received_requests__sender=user, received_requests__is_accepted=True)
    ).distinct()

def total_connections(user):
    return get_connected_users(user).count()

def is_connected(user1, user2):
    return Connection.objects.filter(
        (
            Q(sender=user1, receiver=user2) |
            Q(sender=user2, receiver=user1)
        ),
        is_accepted=True
    ).exists()
