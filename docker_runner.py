import os
from abc import ABC
import docker

from constants import IMAGE_SHARE_FOLDER_PATH, DATA_FOLDER, VCF_TOOLS_IMAGE_NAME, PLINK2_IMAGE_NAME, HG38DB_IMAGE_NAME


class DockerRunner(ABC):
    """
    Run a command inside the container
    """

    def __init__(self):
        self.client = docker.from_env()
        self.volumes = {
            os.path.abspath(DATA_FOLDER): {'bind': IMAGE_SHARE_FOLDER_PATH, 'mode': 'rw'},
        }

    def __call__(self, command=None, environment=None, detach=False):
        self.client.containers.run(
            self.get_image_name(),
            command=f"sh -c '{command}'" if command is not None else None,
            remove=True,
            volumes=self.volumes,
            environment=environment,
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


class Plink2DockerRunner(DockerRunner):
    """
    Run Plink2 command
    """

    def get_image_name(self):
        return PLINK2_IMAGE_NAME


class Hg38dbDockerRunner(DockerRunner):
    """
    Run hg38db query
    """

    def get_image_name(self):
        return HG38DB_IMAGE_NAME
