import sys


class FakeReporter(object):
    """Just log everything in internal attribute - used on tests"""
    def __init__(self):
        self.log = []

    def start_task(self, task):
        self.log.append(('start', task))

    def add_failure(self, task, exception):
        self.log.append(('fail', task))

    def skip_uptodate(self, task):
        self.log.append(('skip', task))

    def cleanup_error(self, exception):
        self.log.append(('cleanup_error',))

    def complete_run(self):
        pass


class ConsoleReporter(object):
    """Default reporter. print results on console/terminal (stdout/stderr)"""
    def __init__(self):
        # save non-succesful result information (include task errors)
        self.failures = []


    def start_task(self, task):
        print task.title()


    def add_failure(self, task, exception):
        self.failures.append({'task': task, 'exception':exception})


    def skip_uptodate(self, task):
        print "---", task.title()


    def cleanup_error(self, exception):
        sys.stderr.write(exception.get_msg())


    def complete_run(self):
        # if test fails print output from failed task
        for result in self.failures:
            sys.stderr.write("#"*40 + "\n")
            sys.stderr.write('%s: %s\n' % (result['exception'].get_name(),
                                           result['task'].name))
            sys.stderr.write(result['exception'].get_msg())
            sys.stderr.write("\n")
            task = result['task']
            out = "".join([a.out for a in task.actions if a.out])
            sys.stderr.write("%s\n" % out)
            err = "".join([a.err for a in task.actions if a.err])
            sys.stderr.write("%s\n" % err)
