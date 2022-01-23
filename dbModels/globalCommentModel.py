from dbModels import db
from sqlalchemy.exc import IntegrityError


class GlobalCommentModel(db.Model):

    __tablename__ = 'globalComment'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    comment = db.Column(db.String())

    def __init__(self):
        pass

    def save_comment(self, comment, email):
        user_session = GlobalCommentModel.query.filter_by(email=email).first()
        if user_session:
            self._update(user_session, comment)
        else:
            self.email = email
            self._save_to_db(comment)

    def _update(self, session, comment):
        try:
            session.comment = comment
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def _save_to_db(self, comment):
        try:
            self.comment = comment
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
