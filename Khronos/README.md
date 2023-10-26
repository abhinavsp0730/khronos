# Khronos [![Downloads](https://static.pepy.tech/badge/django-khronos)](https://pepy.tech/project/django-khronos) 
Are your org hotfixes truly considered "hotfixes" if they take longer than 15 minutes to go live because of slow tests workflows running on GitHub Actions? To speed up this imagine benchmarking test   durations to identify the slow tests when the total number of tests > 500, it seems impractical to run each test individually and manually record their duration   times.   
<img src="https://i.ibb.co/W0LS1cQ/419d86a9-d1ca-4e80-9b62-fc43855c1e2e.jpg" width="300">  
Khronos is a Python library that benchmarks the duration of Django tests. It helps identify slow-running tests in your test suite, allowing you to optimize their performance.

**Feautres:**  
1) **Benchmark Report:** Create benchmark report in the terminal whenever you run your django tests and shows top 10(this no. can be configured) slowest tests.  
2) **Parallel Test Execution:** Works with  `--parallel`  out of the box.  
3) **Google Sheets Integration:** Whole tests benchmark can be automatically  uploaded to Google Sheets.  
4) **CSV Export:** Whole tests benchmark can be saved in a CSV.  

# How to configure: 
1) `pip install django-khronos` or build it locally `python -m build` and install in your virtual env. 
2) Add `TEST_RUNNER = "khronos.custom_test_runner.KhronosTestRunner"` in your `settings.py`  
3) If you want to increase the number of slowest tests displayed on terminal then set ` KHRONOS_REPORT_MAX_ROW=` in your `settings.py`.  
3) If you want to add Google Sheets integration, add:
`KHRONOS_SPRAEDSHEET_REPORT_GSHEET_ID = "your-google-sheet-id"` and your `KHRONOS_GSHEET_CREDS_FILE_PATH = "your-gsheet-cred-path" in your `settings.py` .   
4) For saving the khronos benchmark report.   

**Tested on Django `3.2.14`. Open an issue if it's not supported in your's django version**  
## Contributors ✨
Thanks go to these wonderful people
<!-- readme: contributors -start -->
<table>
<tr>
    <td align="center">
        <a href="https://github.com/abhinavsp0730">
            <img src="https://avatars.githubusercontent.com/u/43638955?v=4" width="100;" alt="abhinavsp0730"/>
            <br />
            <sub><b>Abhinav Prakash</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/Paul-Annay">
            <img src="https://avatars.githubusercontent.com/u/84911232?v=4" width="100;" alt="Paul-Annay"/>
            <br />
            <sub><b>Annay Paul</b></sub>
        </a>
    </td></tr>
</table>
<!-- readme: contributors -end -->
