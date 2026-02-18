import socketio

from src.utils.security import verify_access_token
from src.config.database import session_scope
from src.services.conversation_service import ConversationService
from src.services.user_service import UserService
from src.exceptions.exceptions import HTTPError

def register_socketio_events(sio: socketio.AsyncServer) -> None:
    
    @sio.event
    async def connect(sid, environ, auth):
        try:
            user_id = verify_access_token(auth["token"])
            
            with session_scope() as db:
                user_service = UserService(db)
                username = user_service.get_user(user_id).username
                
        except HTTPError as e:
            raise ConnectionRefusedError(str(e))
        except Exception as e:
            print(str(e))
            raise ConnectionRefusedError("Authentication failed")

        await sio.save_session(sid, {"user_id": user_id, "username": username})
        await sio.enter_room(sid, f"user_id:{user_id}")
        print(f"{sid} connected (username: {username}; user_id: {user_id})")

    @sio.event
    async def disconnect(sid, reason):
        print(f"{sid} disconnected for reason: {reason}")

    @sio.event
    async def send_message(sid, text: str, recipient_id: int):
        session = await sio.get_session(sid)
        user_id = session["user_id"]

        with session_scope() as db:
            conv_service = ConversationService(db)
            try:
                message = conv_service.send_user_message(recipient_id, user_id, text)
            except HTTPError as e:
                return error(e.code, str(e))

        data = {
            "message_id": message.id, 
            "user_id": user_id, 
            "conversation_id": message.conversation_id,
            "text": message.text,
            "is_deleted": message.is_deleted,
            "created_at": message.created_at.isoformat()
        }

        print(f"user_id:{user_id} is sending a message to recipient_id:{recipient_id}")

        await sio.emit("message_received", data, room=f"user_id:{recipient_id}")
        return success(data)

    @sio.event
    async def delete_message(sid, message_id: int):
        session = await sio.get_session(sid)
        user_id = session["user_id"]

        with session_scope() as db:
            conv_service = ConversationService(db)
            try:
                message = conv_service.delete_user_message(user_id, message_id)
                conversation = conv_service.get_conversation(message.conversation_id)
            except HTTPError as e:
                return error(e.code, str(e))

        recipient_id = next((u.id for u in conversation.users if u.id != user_id), None)
        data = {
            "message_id": message.id,
            "user_id": message.user_id,
            "conversation_id": message.conversation_id,
            "text": message.text,
            "is_deleted": message.is_deleted,
            "created_at": message.created_at.isoformat()
        }

        await sio.emit("message_deleted", data, room=f"user_id:{recipient_id}")
        return success()

    @sio.event
    async def mark_conversation_read(sid, conversation_id: int):
        session = await sio.get_session(sid)
        user_id = session["user_id"]

        with session_scope() as db:
            conv_service = ConversationService(db)
            try:
                conv_service.mark_conversation_read(user_id, conversation_id)
                conversation = conv_service.get_conversation(conversation_id)
            except HTTPError as e:
                return error(e.code, str(e))

        recipient_id = next((u.id for u in conversation.users if u.id != user_id), None)
        data = {
            "conversation_id": conversation_id,
            "user_id": user_id
        }

        await sio.emit("conversation_read", data, room=f"user_id:{recipient_id}")
        return success()
    
    @sio.event
    async def is_typing(sid, conversation_id: int):
        session = await sio.get_session(sid)
        user_id = session["user_id"]

        with session_scope() as db:
            conv_service = ConversationService(db)
            try:
                conversation = conv_service.get_conversation(conversation_id)
            except HTTPError as e:
                return error(e.code, str(e))
            
        recipient_id = next((u.id for u in conversation.users if u.id != user_id), None)
        data = {
            "conversation_id": conversation_id,
            "user_id": user_id
        }

        await sio.emit("user_is_typing", data, room=f"user_id:{recipient_id}")
        return success()

    @sio.event
    async def accept_friend_request(sid, friend_id: int):
        session = await sio.get_session(sid)
        user_id = session["user_id"]
        username = session["username"]

        with session_scope() as db:
            user_service = UserService(db)
            try:
                user_service.accept_friend_request(friend_id, user_id)
            except HTTPError as e:
                return error(e.code, str(e))
            
        data = {
            "user_id": user_id,
            "username": username
        }

        await sio.emit("friend_request_accepted", data, room=f"user_id:{friend_id}")
        return success()
    
    @sio.event
    async def decline_friend_request(sid, friend_id: int):
        session = await sio.get_session(sid)
        user_id = session["user_id"]
        username = session["username"]

        with session_scope() as db:
            user_service = UserService(db)
            try:
                user_service.decline_friend_request(friend_id, user_id)
            except HTTPError as e:
                return error(e.code, str(e))
            
        data = {
            "user_id": user_id,
            "username": username
        }

        await sio.emit("friend_request_declined", data, room=f"user_id:{friend_id}")
        return success()
    
    @sio.event
    async def send_friend_request(sid, friend_id: int):
        session = await sio.get_session(sid)
        user_id = session["user_id"]
        username = session["username"]

        with session_scope() as db:
            user_serivce = UserService(db)
            try:
                user_serivce.send_friend_request(friend_id, user_id)
            except HTTPError as e:
                return error(e.code, str(e))
        
        data = {
            "user_id": user_id,
            "username": username
        }

        await sio.emit("friend_request_received", data, room=f"user_id:{friend_id}")
        return success()
    
    @sio.event
    async def remove_friend(sid, friend_id: int):
        session = await sio.get_session(sid)
        user_id = session["user_id"]
        username = session["username"]

        with session_scope() as db:
            user_service = UserService(db)
            try:
                user_service.remove_friend(friend_id, user_id)
            except HTTPError as e:
                return error(e.code, str(e))

        data = {
            "user_id": user_id,
            "username": username
        }

        await sio.emit("friend_removed", data, room=f"user_id:{friend_id}")
        return success()

def success(data = None):
    return {"ok": True, "data": data}

def error(code, message):
    return {"ok": False, "error": {"code": code, "message": message}}