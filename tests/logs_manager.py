"""logs_manager.py.

Модуль, содержащий класс для работы с логами Docker.
"""
import docker


class DockerLogs:
    """Класс для вывода логов Docker."""

    CONTAINERS = (
        "scanner",
        "vuln-service",
        "render-service",
        "netscan-service",
        "pauth-server",
        "postgres",
    )

    def __init__(self) -> None:
        """Метод инициализации экземпляра класса."""
        self.client = docker.from_env()

    def get_docker_logs(self, **kwargs) -> None:
        """Метод класса для вывода логов Docker."""
        for container_name in self.CONTAINERS:
            print(container_name.upper() + " CONTAINER LOGS")
            container = self.client.containers.get(container_name)
            print(container.logs(**kwargs).decode("utf-8"))
