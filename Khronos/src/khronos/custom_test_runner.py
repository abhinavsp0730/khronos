import os
import tempfile
from functools import partial
from time import perf_counter
from unittest import TextTestResult, TextTestRunner

from django.test.runner import DiscoverRunner, RemoteTestResult

from .service import KhronosService


class KhronosRemoteTestResult(RemoteTestResult):
    def startTest(self, test):
        self.events.append(("mark_remote_time", self.test_index, perf_counter()))
        super().startTest(test)

    def stopTest(self, test):
        self.events.append(("mark_remote_time", self.test_index, perf_counter()))
        super().stopTest(test)


class KhronosTextTestResult(TextTestResult):
    def __init__(self, stream, descriptions, verbosity, temp_file):
        self._marked_remote_time = None
        super(KhronosTextTestResult, self).__init__(stream, descriptions, verbosity)
        self.temp_file = temp_file

    def mark_remote_time(self, _test, remote_time):
        self._marked_remote_time = remote_time

    def _get_time(self):
        return self._marked_remote_time or perf_counter()

    def startTest(self, test):
        KhronosService.save_duration(
            test=test, temp_file=self.temp_file, test_time_str="test_start_time", time=self._get_time()
        )
        super(KhronosTextTestResult, self).startTest(test)

    def stopTest(self, test):
        super(KhronosTextTestResult, self).stopTest(test)
        KhronosService.save_duration(
            test=test, temp_file=self.temp_file, test_time_str="test_end_time", time=self._get_time()
        )


class KhronosTextTestRunner(TextTestRunner):
    resultclass = KhronosTextTestResult

    def __init__(self, **kwargs):
        temp_file = kwargs.pop("temp_file")
        super().__init__(**kwargs)
        self.temp_file = temp_file

    def _makeResult(self):
        return self.resultclass(self.stream, self.descriptions, self.verbosity, temp_file=self.temp_file)


class KhronosTestRunner(DiscoverRunner):
    test_runner = KhronosTextTestRunner

    def __init__(self, **kwargs):
        self.temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        super(KhronosTestRunner, self).__init__(**kwargs)
        self.parallel_test_suite.runner_class = partial(
            self.parallel_test_suite.runner_class,
            resultclass=KhronosRemoteTestResult,
        )

    test_runner = KhronosTextTestRunner

    def run_suite(self, suite, **kwargs):
        kwargs = self.get_test_runner_kwargs()
        kwargs["temp_file"] = self.temp_file
        runner = self.test_runner(**kwargs)
        return runner.run(suite)

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        super().run_tests(test_labels, extra_tests=None, **kwargs)
        self.temp_file.flush()
        with open(self.temp_file.name, "r") as file:
            contents_list = [content.split(",") for content in file.read().rstrip(os.linesep).split(os.linesep)]
        # initializing test timing like this
        # {"test_name": {"start_time": 0, "end_time": 0}, ...}

        test_timing = {f"{content[0]}": {"test_start_time": 0, "test_end_time": 0} for content in contents_list}

        # now assigning the values of test_start_time and test_end_time
        for content in contents_list:
            test_timing[content[0]][content[1]] = float(content[2])

        # adding duration
        for key in test_timing:
            test_timing[key]["duration"] = test_timing[key]["test_end_time"] - test_timing[key]["test_start_time"]

        KhronosService(
            sorted_test_timings=list(sorted(test_timing.items(), key=lambda item: item[1]["duration"], reverse=True))
        ).generate_khronos_reports()
