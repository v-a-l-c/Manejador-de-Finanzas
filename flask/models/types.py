from . import db

class Types(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f'<Type {self.type_name}>'

def initialize_types():
    initial_values = ['Ingreso', 'Egreso', 'Deuda']
    for value in initial_values:
        existing_type = db.session.execute(db.select(Types).filter_by(type_name=value)).scalar_one_or_none()
        if not existing_type:
            new_type = Types(type_name=value)
            db.session.add(new_type)
    db.session.commit()