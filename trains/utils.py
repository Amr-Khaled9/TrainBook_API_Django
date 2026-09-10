from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_seat_update(seat):
    channel_layer = get_channel_layer()
    group_name = f'train_{seat.train_id}_seats'

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'seat_update',   
            'seat_id': seat.id,
            'seat_number': seat.seat_number,
            'is_booked': seat.is_booked,
        }
    )