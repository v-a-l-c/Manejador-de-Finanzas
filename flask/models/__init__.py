from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .users import Usuarios
from .tags import Tags
from .types import Types
from .transactions import Transactions
from .debts import Debts
from .interests import Interests

