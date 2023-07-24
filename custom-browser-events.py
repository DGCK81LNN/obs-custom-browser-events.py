# Custom JavaScript events for OBS Studio browser sources
# Copyright (C) 2023  DGCK81LNN
# Documentation can be found at https://github.com/DGCK81LNN/obs_custom-browser-events.py
#
# This program is free software: you can redistribute and/or modify it
# under the terms of the GNU General Public License version 3.
#
# This program is distributed WITHOUT ANY WARRANTY;
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import obspython as obs
from datetime import datetime

def obs_data_get_string_array(data, name):
  items = []
  array = obs.obs_data_get_array(data, name)
  for i in range(obs.obs_data_array_count(array)):
    item = obs.obs_data_array_item(array, i)
    items.append(obs.obs_data_get_string(item, "value"))
    obs.obs_data_release(item)
  obs.obs_data_array_release(array)
  return items

events = []
hotkey_ids = {}
hotkey_callbacks = []

def script_description():
  return "Assign hotkeys to custom browser events. Set hotkeys in OBS settings.\n\nby DGCK81LNN <https://github.com/DGCK81LNN>"

def script_defaults(settings):
  array = obs.obs_data_array_create()
  for i in range(3):
    item = obs.obs_data_create()
    obs.obs_data_set_string(item, "value", "obsCustomEvent%d" % (i + 1))
    obs.obs_data_array_insert(array, obs.obs_data_array_count(array), item)
    obs.obs_data_release(item)
  obs.obs_data_set_default_array(settings, "events", array)
  obs.obs_data_array_release(array)

def script_properties():
  props = obs.obs_properties_create()
  obs.obs_properties_add_editable_list(props, "events", "Events", obs.OBS_EDITABLE_LIST_TYPE_STRINGS, None, None)
  return props

def script_load(settings):
  global events, hotkey_ids
  events = obs_data_get_string_array(settings, "events")
  hotkey_ids = {}

  for event_name in events:
    hotkey_callback = callback_for(event_name)
    hotkey_id = obs.obs_hotkey_register_frontend(
      script_path() + "//" + event_name,
      "Custom browser event %r" % event_name,
      hotkey_callback
    )
    hotkey_callbacks.append(hotkey_callback)
    hotkey_save_array = obs.obs_data_get_array(settings, event_name)
    obs.obs_hotkey_load(hotkey_id, hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
    hotkey_ids[event_name] = hotkey_id

def script_unload():
  for callback in hotkey_callbacks:
    obs.obs_hotkey_unregister(callback)
  hotkey_callbacks.clear()

def script_update(settings):
  if obs_data_get_string_array(settings, "events") != events:
    script_unload()
    script_load(settings)

def script_save(settings):
  for event_name in events:
    hotkey_save_array = obs.obs_hotkey_save(hotkey_ids[event_name])
    obs.obs_data_set_array(settings, event_name, hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)

def callback_for(event_name):
  return lambda pressed: trigger(event_name) if pressed else None

def trigger(event_name):
  print(
    "[%s] Triggered event %r" % (
      datetime.now().astimezone().isoformat(timespec="seconds"),
      event_name
    )
  )
  for src in obs.obs_enum_sources():
    if obs.obs_source_get_id(src) == "browser_source":
      cd = obs.calldata_create()
      obs.calldata_set_string(cd, "eventName", event_name)
      obs.calldata_set_string(cd, "jsonString", "{}")
      obs.proc_handler_call(obs.obs_source_get_proc_handler(src), "javascript_event", cd)
      obs.calldata_destroy(cd)
