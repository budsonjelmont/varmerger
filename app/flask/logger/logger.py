from logging.config import dictConfig

class LogSetup():

  __name__ = 'logger'

  def __init__(self, app=None, **kwargs):
    if app is not None:
      self.init_app(app, **kwargs)

  def init_app(self, app):
    # Check if app config has a log dictionary config defined and use that if it does
    if app.config['LOG_CONFIG_DICT']:
      dictConfig(app.config['LOG_CONFIG_DICT'])
    else:
      logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        handlers=[logging.StreamHandler()]
      )
    return None
