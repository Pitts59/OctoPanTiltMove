# coding=utf-8
from __future__ import absolute_import

#

import octoprint.plugin
import pantilthat
import time

class PanTiltMovePlugin(octoprint.plugin.StartupPlugin,
                        octoprint.plugin.SettingsPlugin,
                        octoprint.plugin.AssetPlugin,
                        octoprint.plugin.TemplatePlugin):

  def __init__(self):
    self.angle_pan = 0
    self.angle_tilt = 0
    self.angle_step = 10
    self.angle_stepmax = 10
    self.andle_steppan = 10
    self.angle_steptilt = 10
  
  
  def on_after_startup(self):

    self._logger.info(" Starting Pan-Tilt Move ")
     
    # set step angle
    self.angle_step = int(self._settings.get(["angleStep"]))  
  
    # Note - the stepping from (0,0) at start up is really just to show that the pan-tilt function
    # is working, otherwise, on re-start it just tries to move to the current position which may mean 
    # no movement.
    
    start_steps = 5 
    
    # Set initial pan angle
    try:
      self.angle_pan = int(self._settings.get(["anglePan"]))
    except:
      self._logger.info("don't know anglePan")
  
    for step in range (start_steps + 1):
      angle_pan_step = int(step * self.angle_pan / start_steps)
         
      try:   
        pantilthat.pan(angle_pan_step)
      except:
        self._logger.info("Pan & Tilt - ERROR setting pan angle")
          
      time.sleep(0.1)
      
    # Set initial tilt angle
    try:
      self.angle_tilt = int(self._settings.get(["angleTilt"]))
    except:
      self._logger.info("don't know angleTilt")
    
    for step in range (start_steps + 1):
      angle_tilt_step = int(step * self.angle_tilt / start_steps) 
        
      try:   
        pantilthat.tilt(angle_tilt_step)
      except:
        self._logger.info("Pan & Tilt - ERROR setting tilt angle")
            
      time.sleep(0.1)

  
	##~~ SettingsPlugin mixin

  def get_settings_defaults(self):
    return dict(
      # put your plugin's default settings here
      anglePan = 0,
      angleTilt = 0,
      angleStep = 10,
      angleStepMax = 10,
      anglePanMax = 90,
      angleTiltMax = 60
    )
	##~~ AssetPlugin mixin

  def get_assets(self):
    # Define your plugin's asset files to automatically include in the
    # core UI here.
    return dict(
      js=["js/PanTiltMove.js"]
    )

  ##-- Template hooks
  
  def get_template_configs(self):
	  return [dict(type="settings",custom_bindings=False)]

	##~~ Softwareupdate hook

  def get_update_information(self):
    # Define the configuration for your plugin to use with the Software Update
    # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
    # for details.
    return dict(
      pantiltmove = dict(
        displayName = "OctoPrint Pan-tilt Move",
        displayVersion = self._plugin_version,
        
        # version check: github repository
        type = "github_release",
        user = "PP59",
        repo = "OctoPrint-PanTiltMove",
        current = self._plugin_version,
        
        # update method: pip
        pip = "https://github.com/PP59/OctoPrint-PanTiltMove/archive/{target_version}.zip"
      )
    )

	##~~ atcommand hook
    
  def processAtCommand(self, comm_instance, phase, command, parameters, tags=None, *args, **kwargs):
    
    if command == 'PANTILTMOVE':
      #get direction and angle from parameters
      panortilt, stepdirection = parameters.split(' ')
      #self._logger.info("Pan & Tilt - ******* pan or tilt: %s, direction %d **" % (panortilt, int(stepdirection)))
	    
      if panortilt == 'pan':
        self.panCamera(int(stepdirection))
 
      elif panortilt == 'tilt':
        self.tiltCamera(int(stepdirection))
        
  ## Camera movement controls - PAN
  
  def panCamera(self, direction):
  
    self.angle_pan = self.changeAngle(self.angle_pan, int(self.angle_step), direction, self._settings.get_int(["anglePanMax"]))
    
    self._logger.info("Pan to %d degrees; panning %d degrees" % (self.angle_pan, int(direction * int(self.angle_step))))
    try:   
      pantilthat.pan(self.angle_pan)
    except:
      self._logger.info("Pan & Tilt - ERROR setting pan angle")  
      
 
  ## Camera movement controls - TILT
   
  def tiltCamera(self, direction):
  
    self.angle_tilt = self.changeAngle(self.angle_tilt, int(self.angle_step), direction, self._settings.get_int(["angleTiltMax"]))
    
    self._logger.info("Tilt to %d degrees; panning %d degrees" % (self.angle_tilt, int(direction * int(self.angle_step))))
    try:   
      pantilthat.tilt(self.angle_tilt)
    except:
      self._logger.info("Pan & Tilt - ERROR setting tilt angle")  
  
  ## change angle        

  def changeAngle(self, angle, step, direction, anglemax):
      
    angle = angle + int(step * direction)  
    
    if (angle > anglemax):
      angle = anglemax
    elif (angle < (-anglemax)):
      angle = -anglemax
    
    return angle
    
    
   

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Pan-Tilt Move"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = PanTiltMovePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.atcommand.queuing": __plugin_implementation__.processAtCommand
	}
