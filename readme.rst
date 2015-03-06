Taskwarrior Subtask Capsule
===========================

This capsule makes it easy to create subtasks.

Note: although this capsule works just fine, it is still a work-in-progress.

Installation
------------

1. Make sure you have `Taskwarrior-Capsules <https://github.com/coddingtonbear/taskwarrior-capsules>`_ installed.
2. Install this library::

    pip install taskwarrior-subtask-capsule

3. That's all!


Use
---

::

  tw <some filter> subtask <task description>

Example
-------

Say that you have a task (id #28) that you'd like to create a subtask for::

  tw 28 subtask This is my subtask's title.
