from dbModels import db


class ConsentFormModel(db.Model):

    __tablename__ = 'consentForm'

    email = db.Column(db.String(), db.ForeignKey('users.email'), primary_key=True)
    acceptance = db.Column(db.String())

    def __init__(self):
        pass

    def get_consentForm(self):
        pass

    def save_consentForm(self, acceptance, email):
        self.email = email
        self.acceptance = acceptance

        user_session = ConsentFormModel.query.filter_by(email=email).first()

        if user_session:
            self.update(user_session)
        else:
            self.save_to_db()

    def update(self, session):
        session.acceptance = self.acceptance
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

