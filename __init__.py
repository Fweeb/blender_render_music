# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****


bl_info = {
    "name": "Render Music",
    "description": "Plays music while rendering and a tone when rendering is complete",
    "author": "Jason van Gumster (Fweeb)",
    "version": (0, 6, 0),
    "blender": (4, 0, 0),
    "location": "Properties > Render",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php?title=Extensions:2.6/Py/Scripts/Render/Render_Music",
    "tracker_url": "",
    "category": "Render"}

if "bpy" in locals():
    import imp
    imp.reload(render_music)
else:
    from . import render_music

import bpy, os
from bpy.types import AddonPreferences


# UI

class RenderMusicProperties(AddonPreferences):
    bl_idname = __name__
    scriptdir = bpy.path.abspath(os.path.dirname(__file__))

    #XXX Music CC-by 3.0, Sam Brubaker, http://soundcloud.com/worldsday/elevator-music-loop
    playfile : bpy.props.StringProperty(
        name = "Play Music",
        description = "Music to play while rendering",
        subtype = 'FILE_PATH',
        default = scriptdir + "/play.mp3")
    #XXX Sound CC-by 3.0, Mike Koenig, http://soundbible.com/1477-Zen-Temple-Bell.html
    endfile : bpy.props.StringProperty(
        name = "End Sound",
        description = "Sound to play when rendering completes",
        subtype = 'FILE_PATH',
        default = scriptdir + "/end.mp3")
    use_play : bpy.props.BoolProperty(
        name = "Play music while rendering",
        description = "Enable the ability to play music while rendering",
        default = True)
    use_end : bpy.props.BoolProperty(
        name = "Play sound upon render completion",
        description = "Enable the ability to play a sound when a render completes",
        default = True)

    def draw(self, context):
        layout = self.layout
        split = layout.split(factor=0.3)
        col = split.column()
        col.prop(self, "use_play", text="Play Music")
        col.prop(self, "use_end", text="End Music")
        col = split.column()
        col.prop(self, "playfile", text="")
        col.prop(self, "endfile", text="")


def render_panel(self, context):
    user_prefs = context.preferences
    addon_prefs = user_prefs.addons[__name__].preferences

    layout = self.layout
    layout.prop(addon_prefs, "use_play")
    layout.prop(addon_prefs, "use_end")


# Registration

def register():
    bpy.utils.register_class(RenderMusicProperties)
    bpy.types.RENDER_PT_context.append(render_panel)

    bpy.types.RenderSettings.music_handle = None
    bpy.app.handlers.render_pre.append(render_music.play_music)
    bpy.app.handlers.render_cancel.append(render_music.kill_music)
    bpy.app.handlers.render_complete.append(render_music.end_music)


def unregister():
    bpy.app.handlers.render_complete.remove(render_music.end_music)
    bpy.app.handlers.render_cancel.remove(render_music.kill_music)
    bpy.app.handlers.render_pre.remove(render_music.play_music)

    bpy.types.RENDER_PT_render.remove(render_panel)
    bpy.utils.unregister_class(RenderMusicProperties)


if __name__ == '__main__':
    register()
