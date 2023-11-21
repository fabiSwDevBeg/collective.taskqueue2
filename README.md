# collective.taskqueue2


A taskqueue implementation for Plone 5/6 based on the Huey package.

See https://huey.readthedocs.io/en/latest/


## Features

This package can be used as a nearly seamless replacement for
`collective.taskqueue`. It does not interfere with WSGI or ZServer and should be
compatible with most up-to-date Plone 5.2 and Plone 6.X installations. Its main
purpose is to allow you to schedule asynchronous operations directly from your
application code. Additionally, thanks to the integration of Huey as the
foundation for `collective.taskqueue2`, you can also schedule periodic tasks in
a cron-style manner.

The `collective.taskqueue` package supports multiple backend storage options,
including Redis, Sqlite, in-memory, and filesystem. However, in most cases,
Redis is the preferred choice for production environments, while Sqlite or
in-memory storage are commonly used for development purposes.


## Installation

Install collective.taskqueue2 by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.taskqueue2


and then running ``bin/buildout``

## Configuration

### Environment variable `HUEY_CONSUMER`

The `HUEY_CONSUMER` environment variable determines whether the current
Plone/Zope instance functions as a consumer of the task queue. It can have the
values `1`, `True`, `true`, or `on` to indicate that the instance is a consumer.
Any other value will be considered as indicating that the instance is not a
consumer.

### Environment variable `HUEY_LOG_LEVEL`

`HUEY_LOG_LEVEL` is an environment variable used to configure the logging level
for the `collective.taskqueue2` package, which is based on the Huey package.

Here are some key points about `HUEY_LOG_LEVEL`:

- It is an environment variable, which means it is a configuration setting that can be set outside of the code.
- The variable is used to control the logging level of the task queue implementation.
- The logging level determines the verbosity of the log messages generated by the `collective.taskqueue2` package.
- The available logging levels vary depending on the logging framework being used. Common levels include `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`, with `DEBUG` being the most verbose and `CRITICAL` being the least verbose.
- By setting the `HUEY_LOG_LEVEL` environment variable, you can control the amount of log output produced by the task queue implementation.
- The specific values that `HUEY_LOG_LEVEL` can take and their corresponding meanings will depend on the implementation details of the `collective.taskqueue2` package.



### Environment variable `HUEY_TASKQUEUE_URL`

The code relies on the `HUEY_TASKQUEUE_URL` environment variable to determine the configuration of the task queue. If the environment variable is not set, it falls back to a default value (`sqlite:///tmp/huey_queue.sqlite`). The `HUEY_TASKQUEUE_URL` should be set as a string representing the URL of the task queue configuration.

To use the code with different task queue configurations, you can set the `HUEY_TASKQUEUE_URL` environment variable with a URL representing the desired configuration. Here are some examples of URL formats for different configurations:

- SQLite: `HUEY_TASKQUEUE_URL=sqlite:///path/to/database.sqlite`
- Redis: `HUEY_TASKQUEUE_URL=redis://localhost:6379/0`
- Memory: `HUEY_TASKQUEUE_URL=memory://`
- File: `HUEY_TASKQUEUE_URL=file:///path/to/queue/folder`

Make sure to adjust the URLs according to your specific environment.

### Examples

Here are examples of different URL configurations for each supported scheme:

1. SQLite:

   `HUEY_TASKQUEUE_URL=sqlite:///path/to/database.sqlite`

   This URL configures the task queue to use SQLite with a specific database file.

2. Redis:

   `HUEY_TASKQUEUE_URL=redis://localhost:6379/0`

   This URL configures the task queue to use Redis with a specific host (`localhost`), port (`6379`), and database (`0`).

3. Memory:

   `HUEY_TASKQUEUE_URL=memory://`

   This URL configures the task queue to use an in-memory storage. No additional parameters are needed.

4. File:

   `HUEY_TASKQUEUE_URL=file:///path/to/queue/folder`

   This URL configures the task queue to use a file-based storage with a specific folder path.

Ensure that you set the appropriate URL corresponding to the desired scheme before running the code.

The `huey_taskqueue` object created based on the URL configuration can be used further in the application for task queuing and processing.


### Console output

After installing  `collective.taskqueue2` in Plone, you should see the following output on the console
(with `HUEY_LOG_LEVEL=DEBUG` and `HUEY_CONSUMER=1` set):

```
2023-11-21 11:02:59,012 INFO    [huey.consumer:386][Thread-1 (run)] Huey consumer started with 1 thread, PID 76861 at 2023-11-21 10:02:59.012894
2023-11-21 11:02:59,012 INFO    [huey:77][MainThread] collective.taskqueue2: consumer thread started.
2023-11-21 11:02:59,013 INFO    [huey.consumer:389][Thread-1 (run)] Scheduler runs every 1 second(s).
2023-11-21 11:02:59,013 INFO    [huey.consumer:391][Thread-1 (run)] Periodic tasks are enabled.
Starting server in PID 76861.
2023-11-21 11:02:59,014 INFO    [huey.consumer:398][Thread-1 (run)] The following commands are available:
+ collective.taskqueue2.huey_tasks.dump_queue_stats
+ collective.taskqueue2.huey_tasks.schedule_browser_view
```


## Authors

 - Andreas Jung <info@zopyx.com> for University of Bologna



## Contribute

- Issue Tracker: https://github.com/collective/collective.taskqueue2/issues
- Source Code: https://github.com/collective/collective.taskqueue2
- Documentation: https://docs.plone.org/foo/bar



## License

The project is licensed under the GPLv2.
