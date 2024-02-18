import os


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "site.db")}'
    SQLALCHEMY_BINDS = {
        'Elements': f'sqlite:///{os.path.join(BASE_DIR, "calc_pages/x_ray_mirrors/data_collections/Elements.db")}',
        'Compounds': f'sqlite:///{os.path.join(BASE_DIR, "calc_pages/x_ray_mirrors/data_collections/Compounds.db")}'
    }
