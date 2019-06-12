import falcon
import sqlalchemy.orm.scoping as scoping
from sqlalchemy.exc import SQLAlchemyError
import log
from config import config
from utils.errors.errors import DatabaseError, ERROR_DATABASE_ROLLBACK
LOG = log.get_logger()


class DBSessionManager(object):
    def __init__(self, db_session):
        self._session_factory = db_session
        self._scoped = isinstance(db_session, scoping.ScopedSession)

    def process_request(self, req, res):
        """
        request post-processing
        """
        req.context['session'] = self._session_factory

    def process_response(self, req, res, req_succeeded, resource=None):
        """
        response postprocessing
        """
        session = req.context['session']

        if config.DB_AUTOCOMMIT:
            try:
                session.commit()
            except SQLAlchemyError as ex:
                session.rollback()
                raise DatabaseError(ERROR_DATABASE_ROLLBACK, ex.args, None)

        if self._scoped:
            session.remove()
        else:
            session.close()