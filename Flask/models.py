from flask_security import UserMixin, RoleMixin
import uuid
from db_object import db

# Association table between users and roles
roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id"))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    users = db.relationship("User", secondary=roles_users, back_populates="roles")
    def __repr__(self):
        return f"<Role {self.name}>"



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=True)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    password = db.Column(db.String(255))
    roles = db.relationship("Role", secondary=roles_users, back_populates='users')

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Name : {self.username}"