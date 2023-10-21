import subprocess
from os import path


class UeberzugLayer():
    """Wrapper for Ueberzug++"""

    def __init__(self, pid_file = "/tmp/ueberzug-py.pid", socket="/tmp/ueberzugpp-%pid%.socket", no_opencv=True):
        self._socket = None
        self._pid_file = pid_file
        self._pid = None
        ret = subprocess.run(["ueberzug", "layer", "--pid-file", pid_file, "--no-stdin", "--no-opencv" if no_opencv else ""], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not ret.returncode == 0:
            raise Exception(f"ueberzug layer exited with {ret.returncode}")
        if not path.isfile(pid_file):
            raise Exception(f"Ueberzug pid file not found: {pid_file}")
        with open(pid_file, "r") as file:
            try:
                self._pid = int(file.read())
            except ValueError as e:
                raise Exception(f"Invalid content of pid file {pid_file}: {e}")
        self._socket = socket.replace("%pid%", str(self._pid))
        # if not path.exists(self._socket):
        #     raise Exception(f"Ueberzug socket not found: {self._socket}")

    def display_image(self, image, x=0, y=0, max_width=0, max_height=0, identifier="Image"):
        ret = subprocess.run(["ueberzug", "cmd", "-s", self._socket, "-a", "add", "-i", identifier, "-f", image, "-x", str(x), "-y", str(y), "--max-width", str(max_width), "--max-height", str(max_height)])
        if not ret.returncode == 0:
            raise Exception(f"ueberzug cmd exited with {ret.returncode}")

    def remove_image(self, identifier="Image"):
        ret = subprocess.run(["ueberzug", "cmd", "-s", self._socket, "-a", "remove", "-i", identifier])
        if not ret.returncode == 0:
            raise Exception(f"ueberzug cmd exited with {ret.returncode}")

    def __del__(self):
        from os import remove
        try:
            remove(self._pid_file)
        except:
            pass
        import subprocess  # might be unloaded
        ret = subprocess.run(["ueberzug", "cmd", "-s", self._socket, "-a", "exit"])
        if not ret.returncode == 0:
            raise Exception(f"ueberzug cmd exited with {ret.returncode}")
