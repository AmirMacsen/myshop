from django.test import TestCase

from celery import Celery

app = Celery('tasks')


@app.task
def add(x, y):
    return x + y


if __name__ == '__main__':
    print(add.name)  # tasks.add
    print(add)  # <@task: tasks.add of tasks at 0x1f72d6a6fd0>

    print(app.tasks)  # {'tasks.add': <@task: tasks.add of tasks at 0x1f72d6a6fd0>,。。。 }
    print(app.conf)  # Settings({}, {}, {'accept_content': ['json'], 。。。})

    print(*list(app.conf.items()), sep='\n')
