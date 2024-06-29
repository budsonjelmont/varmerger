from varmerger.phasing import phasing

class PhaseSetup():
  def __init__(self, app=None, **kwargs):
    if app is not None:
      self.init_app(app, **kwargs)
  
  def init_app(self, app):
    phasehandlers = app.config['PHASE_CONFIG_DICT']
    phasors = {}
    for k,v in phasehandlers['handlers'].items():
      #phasor = SeqRepo.SeqRepo(url, build) # e.g. 'http://127.0.0.1:7777', 'grch37' # TODO dependency injection
      phasors[k] = phasing.Phasing(v['url'],v['build'])
    app.phasors = phasors
    return None
