from taskwarrior_capsules.capsule import CommandCapsule
from taskwarrior_capsules.exceptions import CapsuleError


class Subtask(CommandCapsule):
    MIN_VERSION = '0.2.4'
    MAX_VERSION = '1.0'
    MIN_TASKWARRIOR_VERSION = '2.3'
    MAX_TASKWARRIOR_VERSION = '2.4.999'

    def get_params_to_copy(self):
        return self.configuration.get(
            'params_to_copy',
            ','.join(
                [
                    'project',
                    'priority',
                    'tags',
                    'due',
                ]
            )
        ).split(',')

    def handle(self, filter_args, extra_args, **kwargs):
        results = self.get_matching_tasks(filter_args)
        if len(results) == 0:
            raise CapsuleError("No tasks matched filter")
        if len(results) > 1:
            raise CapsuleError("More than one task matched filter")
        parent_task = results[0]

        # Ideally, we'd also let people change tags and whatnot here,
        # but that's a little too complex for tonight.
        description = ' '.join(extra_args).strip()
        if not description:
            raise CapsuleError("Task description must be specified")

        kwargs = {}
        for param in self.get_params_to_copy():
            kwargs[param] = parent_task.get(param)

        new_task = self.client.task_add(
            description=description,
            **kwargs
        )
        parent_task['depends'] = [new_task['uuid']]

        self.client.task_update(parent_task)
