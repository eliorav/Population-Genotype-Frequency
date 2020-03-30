import os
from abc import ABC
import docker
from constants import IMAGE_SHARE_FOLDER_PATH, DATA_FOLDER, VCF_TOOLS_IMAGE_NAME


class DockerRunner(ABC):
    """
    Run a command inside the container
    """

    def __init__(self):
        self.client = docker.from_env()
        self.volumes = {
            os.path.abspath(DATA_FOLDER): {'bind': IMAGE_SHARE_FOLDER_PATH, 'mode': 'rw'},
        }

    def __call__(self, command, detach=False):
        self.client.containers.run(
            self.get_image_name(),
            f"sh -c '{command}'",
            remove=True,
            volumes=self.volumes,
            detach=detach,
        )

    def get_image_name(self):
        """
        :return: image name
        """


class VCFToolsDockerRunner(DockerRunner):
    """
    Run VCFTools command
    """

    def get_image_name(self):
        return VCF_TOOLS_IMAGE_NAME
