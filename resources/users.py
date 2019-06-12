import falcon
import log
from sqlalchemy.orm.exc import NoResultFound
from resources.base import BaseResource
from utils.hooks import authorization
from utils.authorization import encrypt_token, hash_password, uuid
from models import User, Base
from utils.errors.errors import NotValidParameterError, UserNotExistsError, AppError, OperationError
from utils.validators import validate_user_create, validate_money_transfer_create

LOG = log.get_logger()


class Collection(BaseResource):
    """
    /resev/v1/users
    """
    @falcon.before(validate_user_create)
    def on_post(self, req, res):
        session = req.context['session']
        user_req = req.context['data']
        if user_req:
            user = User()
            user.username = user_req['username']
            user.email = user_req['email']
            user.password = hash_password(user_req['password']).decode('utf-8')
            user.details = user_req['details'] if 'info' in user_req else None
            user.balance = user_req['balance'] if 'balance'in user_req else 100.0
            uuid_id = uuid()
            user.uuid_id = uuid_id
            user.token = encrypt_token(uuid_id).decode('utf-8')
            session.add(user)
            user_db = session.query(User).filter_by(username=user_req['username']).one()
            self.on_success(res, user_db.to_dict())
        else:
            raise NotValidParameterError(req.context['data'])

    @falcon.before(authorization)
    def on_get(self, req, res):
        session = req.context['session']
        user_dbs = session.query(User).all()
        if user_dbs:
            obj = [user.to_dict() for user in user_dbs]
            self.on_success(res, obj)
        else:
            raise AppError()

    @falcon.before(authorization)
    def on_put(self, req, res):
        pass


class Item(BaseResource):
    """
    /resev/v1/users/{user_id}
    """

    @falcon.before(authorization)
    def on_get(self, req, res, user_id):
        session = req.context['session']
        try:
            user_db = User.find_one(session, user_id)
            self.on_success(res, user_db.to_dict())
        except NoResultFound:
            raise UserNotExistsError('user id: %s' % user_id)


class ItemTransfer(BaseResource):
    """
    /resev/v1/users/{user_id}/transfer
    """

    @falcon.before(authorization)
    @falcon.before(validate_money_transfer_create)
    def on_post(self, req, res, user_id):
        session = req.context['session']
        borrow_data = req.context['data']
        if borrow_data:
            try:
                user_lender = User.find_one(session, user_id)
                user_borrower = User.find_by_username(session, borrow_data['borrower'])
                quantity = borrow_data['quantity']
            except NoResultFound:
                raise UserNotExistsError('user id: %s' % user_id)
            try:
                if user_lender.balance < 0:
                    raise OperationError()
                lender_quantity = user_lender.balance - quantity
                borrower_quantity = user_borrower.balance + quantity
                user_lender.find_update(session, user_lender.user_id, {User.balance: lender_quantity})
                user_borrower.find_update(session, user_borrower.user_id, {User.balance: borrower_quantity})
                session.commit()
                user_updated = User.find_one(session, user_id)
            except Exception as e:
                raise OperationError()
            self.on_success(res, user_updated.to_dict())

        else:
            raise NotValidParameterError(req.context['data'])
