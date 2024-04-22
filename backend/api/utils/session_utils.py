from ..models import Sessions
from ..serializers import SessionsSerializer


def session_update(creation_time, user_id: int) -> None | str:
    existing_session = Sessions.objects.filter(user=user_id).first()

    if existing_session:
        existing_session.created_at = creation_time
        serializer = SessionsSerializer(
            instance=existing_session,
            data={"created_at": creation_time, "user": user_id},
        )
    else:
        session_data = {"created_at": creation_time, "user": user_id}
        serializer = SessionsSerializer(data=session_data)
    if serializer.is_valid():
        serializer.save()
        return None
    else:
        return str(serializer.errors)
