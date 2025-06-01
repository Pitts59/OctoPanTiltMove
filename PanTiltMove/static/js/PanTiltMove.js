/*
 * View model for Pantiltmove
 * 
 * Author: PP59
 * License: AGPLv3
 */
$(function() {
	function PanTiltMoveViewModel(parameters) {
		var self = this;
		
		self.controlViewModel = parameters[0];
		self.settingsViewModel = parameters[1];

		self.onStartup = function() {
			$('#control-jog-xy-servo').insertAfter('#control-jog-general');
		}

		self.onBeforeBinding = function() {
			self.controlViewModel.right = ko.observable('@PANTILTMOVE  ' + 'pan' + ' -1');
			self.controlViewModel.left = ko.observable('@PANTILTMOVE ' + 'pan' + ' 1');
			self.controlViewModel.up = ko.observable('@PANTILTMOVE ' + 'tilt' + ' -1');
			self.controlViewModel.down = ko.observable('@PANTILTMOVE ' + 'tilt' + ' 1');
		}

		self.onEventSettingsUpdated = function (payload) {            
			self.controlViewModel.right('@PANTILTMOVE ' + 'pan' + ' -1');
			self.controlViewModel.left('@PANTILTMOVE ' + 'pan' + ' 1');
			self.controlViewModel.up('@PANTILTMOVE ' + 'tilt' + ' -1');
			self.controlViewModel.down('@PANTILTMOVE ' + 'tilt' + ' 1');
		};
	}

	OCTOPRINT_VIEWMODELS.push({
		construct: PanTiltMoveViewModel,
		dependencies: [ "controlViewModel", "settingsViewModel" ],
		elements: [ "settings_plugin_PanTiltMove_form", "control-jog-xy-servo" ]
	});
});
