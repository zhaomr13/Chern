"""

"""
class VContainer(object):
    """
    A VContainer should manage the physical container.
    The VContainer should be able to interact with the, or a
    A container should be able to be created from a task?
    What to determine a container?
    """
    def __init__(self):
        """
        Set the uuid
        """
        pass

    def image_from(self, )

    def set_parameters(self)

    def inspect(self):
        ps = subprocess.Popen("docker inspect {0}".format(self.container_id) )
        ps.wait()
        output = ps.communicate()[0]
        json_result = json.loads(output)
        return json_result[0]

    def status(self):
        status = self.inspect().get("State")
        if status.get("Running") return "running"
        return status.get("Status")

    def start(self):
        subprocess.Popen("docker run -v inputs, outputs, {0}".format(image()) )
        pass
