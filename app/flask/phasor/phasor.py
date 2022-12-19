from varmerger.phasing import phasing

class PhaseSetup():
  def __init__(self, app=None, **kwargs):
    if app is not None:
      self.init_app(app, **kwargs)
  
  def init_app(self, app):
    phasehandlers = app.config['PHASE_CONFIG_DICT']
    phasors = {}
    for k,v in phasehandlers['handlers'].items():
      phasors[k] = phasing.Phasing(v['url'],v['build'])
    app.phasors = phasors
    return None
