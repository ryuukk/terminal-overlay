
# COMPATIBILITY
# - Linux (x11): Yes
# - Linux (wayland): no clue, i need to find alternatives for the dependencies
#

# HOW TO USE
# - Linux (x11)
#   - install both 'wmctrl' and 'xdotool'
#
#
# - define your terminal of choice in the `start_terminal_command` function bellow
# - save this file in sublime text's Packages folder (File -> Preferenecs -> Browse Packages..)
# - setup a sublime text shortcut for the command `terminal_overlay_toggle`



import sublime
import sublime_plugin
import os
import subprocess


G_NO_TASKBAR_ICON = False
G_PID_ST = -1
G_PID_TERM = -1
G_WID_ST = -1
G_WID_TERM = -1


# change this to the terminal of your liking
def start_terminal_command(workingDir):
    return ['xfce4-terminal', '--disable-server', "--default-working-directory", workingDir]


class FocusManager(sublime_plugin.EventListener):
    def on_activated(self, view):
        global G_WID_TERM

        if G_WID_TERM == -1:
            return
        if os.path.exists("/proc/"+str(G_PID_TERM)) == False:
            return

        print("set term window above")
        # a = subprocess.Popen(['xwit', 'pop', '-i', str(G_WID_TERM)], shell=False)
        a = subprocess.Popen(['wmctrl', '-ir', str(G_WID_TERM), '-b', 'add,above', str(G_WID_ST)], shell=False)

    def on_deactivated(self, view):
        global G_WID_TERM

        if G_WID_TERM == -1:
            return
        if os.path.exists("/proc/"+str(G_PID_TERM)) == False:
            return

        print("remove term window above")
        # a = subprocess.Popen(['xwit', 'pop', '-i', str(G_WID_TERM)], shell=False)
        a = subprocess.Popen(['wmctrl', '-ir', str(G_WID_TERM), '-b', 'remove,above', str(G_WID_ST)], shell=False)

class TerminalOverlayToggleCommand(sublime_plugin.WindowCommand): 
    def run(self):
        global G_PID_ST
        global G_PID_TERM
        global G_WID_ST
        global G_WID_TERM

        # if known, give it focus
        if G_WID_TERM != -1:
            if os.path.exists("/proc/"+str(G_PID_TERM)):
                a = subprocess.Popen(['wmctrl', '-ia', str(G_WID_TERM)], shell=False)
                return
            else:
                G_PID_TERM = -1
                G_WID_TERM = -1

        # grab ST's window id
        if G_PID_ST == -1:
            pid = os.getpid()
            G_PID_ST = get_parent_process_id(pid) # this is python's pid, get the parent wich should be ST
            ids = get_window_id(G_PID_ST)
            G_WID_ST = ids[-1]

        if G_WID_ST == -1:
            print("error: no st wid")
            return

        # start terminal process
        if G_PID_TERM == -1:
            folders = self.window.folders()
            wdir = "$HOME"
            if len(folders) > 0:
                wdir = folders[0]

            args = start_terminal_command(wdir)
            print("terminal: starting:", args)
            proc = subprocess.Popen(args, shell=False)
            G_PID_TERM = proc.pid
            def grab_wid():
                global G_PID_TERM
                global G_WID_TERM
                ids = get_window_id(G_PID_TERM)
                if len(ids) == 0:
                    print("error: can't find terminal window id")
                    return
                G_WID_TERM = ids[-1]
                self.make_it_transient()

            # wait a little to grab its window id
            sublime.set_timeout(grab_wid, 500)

    def make_it_transient(self):
        global G_WID_ST
        global G_WID_TERM

        # make it modal
        if G_NO_TASKBAR_ICON == True:
            a = subprocess.Popen(['wmctrl', '-ir', str(G_WID_TERM), '-b', 'add,skip_pager,skip_taskbar', str(G_WID_ST)], shell=False)

def get_window_id(pid: int) -> int:
    p = subprocess.Popen(f"xdotool search --pid {pid}", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    pstatus = p.wait()
    if len(output) > 0 and err == None:
        arr = []
        for it in output.decode('utf-8').splitlines():
            arr += [int(it)]
        return arr
    return []

def get_parent_process_id(pid: int) -> int:
    with open(f"/proc/{pid}/status") as f:
        for line in f.readlines():
            if line.startswith("PPid:\t"):
                return int(line[6:])
    return -1
