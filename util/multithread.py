import concurrent.futures


def multithread(func, data_points: list, **kwargs):
    """Uses multiple threads to perform tasks. A general purpose
        method to leverage threading and perform parallel tasks such
        as writing to files, appending to pre-existing objects, etc.
    Tracks any job failures that occur during processing.
    Executes, at most, 10 jobs at a time, to avoid overloading containers/
        executors.
    Args:
        func (function): the function to parallelize. This function should
            accept an iterable, and should generally not return anything,
            but rather write to file(s), change an object in place,
            or otherwise perform some order-independent series of tasks.
        data_points (list): the list of data points to use. This should be
            some iterable.
        **kwargs: any additional kwargs to pass to func
    Returns:
        None
    """
    MAX_JOBS_IN_QUEUE = 10
    failures = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        jobs = {}
        data_points_left = len(data_points)
        data_points_iter = iter(data_points)
        data_points = []  # reset data points after making iter

        while data_points_left:
            for data_point in data_points_iter:
                job = executor.submit(func, data_point, **kwargs)
                jobs[job] = data_point
                if len(jobs) > MAX_JOBS_IN_QUEUE:
                    break

            for job in concurrent.futures.as_completed(jobs):
                data_points_left -= 1
                try:
                    job.result()
                except Exception as e:
                    failures.append(str(e))
                finally:
                    del jobs[job]
                    del job
                break

    if failures:
        raise Exception(
            "Parallel process raised errors.\nSee errors below:\n{}".format(
                "\n".join(failures)
            )
        )
