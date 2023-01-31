from conductor.client.configuration.configuration import Configuration,AuthenticationSettings
from conductor.client.http.models import Task, TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.worker.worker import Worker
import json


class ehazak_hello_world_worker(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_result = self.get_task_result_from_task(task)
        name = task.input_data["name"]
        hello_message = "hello {}".format(name)
        task_result.add_output_data('hello_message', hello_message)
        task_result.status = TaskResultStatus.COMPLETED
        return task_result


class ehazak_reverse_message_worker(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_result = self.get_task_result_from_task(task)
        hello_message = task.input_data["hello_message"]
        reverse_message = hello_message[::-1]
        task_result.add_output_data('reverse_message', reverse_message)
        task_result.status = TaskResultStatus.COMPLETED
        return task_result


def main():
    with open('configuration.json') as f:
        config_dict = json.load(f)
    configuration = Configuration(
    server_api_url=config_dict["api_url"],
    authentication_settings=AuthenticationSettings(
        key_id=config_dict['key_id'],
        key_secret=config_dict['key_secret']
        )
    )
    
    workers = [
        ehazak_hello_world_worker(
            task_definition_name="ehazak-hello-world"
        ),
        ehazak_reverse_message_worker(
            task_definition_name="ehazak-reverse-message"
        )
    ]

    with TaskHandler(workers, configuration) as task_handler:
        task_handler.start_processes()
        task_handler.join_processes()


if __name__ == "__main__":
    main()