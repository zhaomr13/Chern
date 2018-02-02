"""
This should have someting
A image can be determined uniquely by the ?
"""
class VImage(object):
    def __init__(self, image_id):
        inspect(image_id)
        self.status = "missing"

    def inspect(self):
        subprocess.call("")


def generate_docker_file(path):
    pass

def create_image(path):
    generate_docker_file(path)
    subprocess.call("docker build .")
    if check_failed:
        return -1
    return image_id
