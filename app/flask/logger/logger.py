from logging.config import dictConfig

class LogSetup():
  def __init__(self, app=None, **kwargs):
    if app is not None:
      self.init_app(app, **kwargs)

  def init_app(self, app):
    # Check if yaml config was passed, and if it was use that
    if app.config['LOG_CONFIG_DICT']:
      log_config = app.config['LOG_CONFIG_DICT']
      dictConfig(log_config)
    else:
      logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        handlers=[logging.StreamHandler()]
      )
    return None
