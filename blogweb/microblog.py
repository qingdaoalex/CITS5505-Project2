import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User, Post, Message, Notification
from flask_migrate import Migrate
from app import create_app, db
from config import DeploymentConfig 

# Create the Flask app using the factory function
app = create_app(config_class=DeploymentConfig)

migrate = Migrate()
migrate.init_app(app, db)
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': app.db, 'User': User, 'Post': Post, 'Message': Message, 'Notification': Notification}

if __name__ == '__main__':
    app.run(debug=True)