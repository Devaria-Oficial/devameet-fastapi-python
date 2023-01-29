from fastapi import FastAPI
from fastapi_socketio import SocketManager
from src.core.logger import ApiLogger

from src.core.database import SessionLocal
from .schema import UpdatePosition, ToggleMute
from .service import RoomService

logger = ApiLogger(__name__)

class WebSocketObject:
    def __init__(self, sid: str, link: str, user_id: str):
        self.sid = sid
        self.link = link
        self.user_id = user_id

class WebSocketServer:
    def __init__(self, app: FastAPI, origins: list | str = '*'):
        logger.info("Socket server initialized")
        self.app = app
        self.socket_manager = SocketManager(app=app, cors_allowed_origins=origins, mount_location='/')
        self.active_sockets: list[WebSocketObject] = []
        self.run()

    def run(self):
        self.socket_manager.on('disconnect', self.on_disconnect)
        self.socket_manager.on('join', self.on_join)
        self.socket_manager.on('move', self.on_move)
        self.socket_manager.on('toggl-mute-user', self.on_toggl_mute_user)
        self.socket_manager.on('call-user', self.on_call_user)
        self.socket_manager.on('make-answer', self.on_make_answer)

    async def on_disconnect(self, sid, *args, **kwargs):
        logger.info("Disconnecting")

        user_socket = list(filter(lambda x: x.sid == sid, self.active_sockets))
        logger.debug("Removing user from room. User: " + str(user_socket))

        self.active_sockets = list(filter(lambda x: x.sid != sid, self.active_sockets))

        if len(user_socket) == 0:
            return

        user_socket = user_socket[0]

        with SessionLocal() as db_connection:
            service = RoomService(db_connection)
            service.delete_users_position(user_socket.sid)

        logger.debug("Emitting remove user")
        await self.socket_manager.emit(f'{user_socket.link}-remove-user', {'socketId': user_socket.sid}, skip_sid=sid)


    async def on_join(self, sid, data):
        logger.info("JOIN:Method called")
        link, user_id = data['link'], data['userId']

        logger.debug(f"JOIN:User - sid={sid}, link={link}, user_id={user_id}")

        logger.debug("JOIN:Checking if user is already in room")
        existing_socket = [x for x in self.active_sockets
                           if x.user_id == user_id
                           and x.link == link]
        if len(existing_socket) == 0:
            logger.debug("JOIN:Inserting user in room")
            self.active_sockets.append(WebSocketObject(sid, link, user_id))

            dto = UpdatePosition(x=2, y=2, orientation='bottom')

            with SessionLocal() as db_connection:
                service = RoomService(db_connection)
                service.update_user_position(user_id=user_id, link=link, client_id=sid, dto=dto)
                users = service.list_users_position(link)

            await self.socket_manager.emit(f'{link}-update-user-list', {'users': [user.to_json() for user in users]})
            await self.socket_manager.emit(f'{link}-add-user', {'user': sid}, skip_sid=sid)
        else:
            user = existing_socket[0]
            logger.debug(f"JOIN:User already in room: socket={user}")

    async def on_move(self, sid, *args, **kwargs):
        link, user_id, x, y, orientation =  args[0]['link'],  args[0]['userId'], args[0]['x'], args[0]['y'], args[0]['orientation']

        dto = UpdatePosition(x=x, y=y, orientation=orientation)

        with SessionLocal() as db_connection:
            service = RoomService(db_connection)
            service.update_user_position(user_id=user_id, link=link, client_id=sid, dto=dto)
            users = service.list_users_position(link)

        await self.socket_manager.emit(f'{link}-update-user-list', {'users': [user.to_json() for user in users]})

        logger.info("Moved")

    async def on_toggl_mute_user(self, sid, *args, **kwargs):
        logger.info("Toggl mute user")
        link, user_id, muted = args[0]['link'], args[0]['userId'], args[0]['muted']

        dto = ToggleMute(
            user_id=user_id,
            muted=muted,
            link=link
        )

        with SessionLocal() as db_connection:
            service = RoomService(db_connection)
            service.update_user_mute(dto)
            users = service.list_users_position(link)

        await self.socket_manager.emit(f'{link}-update-user-list', {'users': [user.to_json() for user in users]})

    async def on_call_user(self, sid, *args, **kwargs):
        logger.info("Call user")
        offer, to = args[0]['offer'], args[0]['to']
        call_made_dto = {
            'offer':offer,
            'socket': sid
        }

        logger.debug("Socket callUser: " + sid + " to " + to)
        await self.socket_manager.emit('call-made', call_made_dto, to=to)

    async def on_make_answer(self, sid, *args, **kwargs):
        logger.info("Make answer")
        answer, to = args[0]['answer'], args[0]['to']
        logger.debug("Socket callUser: " + sid + " to " + args[0]['to'])
        make_answer_dto = {
            'answer': answer,
            'socket': sid
        }

        await self.socket_manager.emit('answer-made', make_answer_dto, to=to)
