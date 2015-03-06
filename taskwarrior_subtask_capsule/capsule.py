from taskwarrior_capsules.capsule import CommandCapsule
from taskwarrior_capsules.exceptions import CapsuleError

from taskw.warrior import TaskWarriorShellout


class Capsule(CommandCapsule):
    MIN_VERSION = '0.1.3'
    MAX_VERSION = '1.0'

    def get_params_to_copy(self):
        try:
            configuration = self.get_configuration()
            return configuration['params_to_copy'].split(',')
        except KeyError:
            return [
                'project',
                'tags',
            ]

    def handle(self, filter_args, extra_args, terminal=None, **kwargs):
        client = TaskWarriorShellout(marshal=True)
        filter_command = filter_args + ['status:pending', 'export']
        results = client._get_json(*filter_command)
        if len(results) == 0:
            raise CapsuleError("No tasks matched filter")
        if len(results) > 1:
            raise CapsuleError("More than one task matched filter")
        _, parent_task = client.get_task(
            uuid=results[0]['uuid']
        )

        # Ideally, we'd also let people change tags and whatnot here,
        # but that's a little too complex for tonight.
        description = ' '.join(extra_args)

        kwargs = {}
        for param in self.get_params_to_copy():
            kwargs[param] = parent_task.get(param)

        new_task = client.task_add(
            description=description,
            **kwargs
        )
        parent_task['depends'] = [new_task['uuid']]

        client.task_update(parent_task)
