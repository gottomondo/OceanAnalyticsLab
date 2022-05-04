# Log Management

With this module is possible to create automatically a json file log which contains some useful information
to integrate the algorithm with a web interface ant to provide also useful information for the debug.

The json is composed by four section and one attribute:

- **input**: 
- **exec_info**: contains execution running time of each function
- **other**: contains information related to a specific method
- **error_log** (Mandatory): contains the exit code and an error message, the value is 0 if the method hs been succeeded 
- **end_time** (Mandatory):  it indicates the moment in which the method has finished its execution (with a timestmap in ISO format and UTC)
- **worker_logs**: in case of parallel implementation this section will contain the log the workers submitted 

## Template

```json
{
    "input": {
        "parameter1": "VALUE1",
        "parameter2": "VALUE2",
        "parameter3": "VALUE3"
    },
    "exec_info": {
        "main_start": "[DD/MM/YYYY, hh:mm:ss]   -   Start Method",
        "func_start": "[DD/MM/YYYY, hh:mm:ss]   -   Start func",
        "func_end": "[DD/MM/YYYY, hh:mm:ss]   -   End func,  time needed:  ?.???? seconds ",
        "func2_start": "[DD/MM/YYYY, hh:mm:ss]   -   Start func2 file",
        "func2_end": "[DD/MM/YYYY, hh:mm:ss]   -   End func2,  time needed:  ?.???? seconds ",
        "main_end": "[DD/MM/YYYY, hh:mm:ss]   -   End main, time needed:  ?.???? seconds "
    },
    "other": {
        "poutkey": "parameter to control parallel execution",
        "root_dir": "root dir of the work dir",
        "hostname": "HOSTNAME"
    },
    "error_log": {
        "code": 0,
        "message": "Execution Done"
    },
    "end_time": "YYYY-MM-DDThh:mm:ss+00:00",
    "worker_logs": [
        "worker_i" : {
           " ..."
        }
    ]
}
```

As specified in the previous paragraph, only two elements are mandatory, the other one are optional and
usually are used to better debug the method in case of execution error.


### Input

This section contains all the parameter received by the method and its value, it is useful because allow us to see what the
method received as input parameters and to understand the context of the other sections of the log.
It is a simple dict composed bu the name of the attribute and its value.

### Exec Info
This section contains information about which function has been executed and the timestamp of the start and the end of the 
function, printing also the running time of that specific function.
This section is useful to understand the performance of the method on dataminer.
In case of error is also immediately to see what is the last function to have been executed.

When the class is created, it creates automatically the exec section put a first message indicating that the main function has started.
Then, the class provides two function to generate automatically the execution log message:

- `def phase_start(self, input_phase: str)`: receive as argument the name of the function, creates the start log message
- `def phase_done(self, input_phase: str, input_run_time=None, idle_time=None)`: receive as argument the same function name started previously, 
    in addition it is possible to indicate the running time (if the function compute it by itself), 
    or is possible to specify the time which the function has been put in idle time in order to wait the execution of another function

Finally, is present the function `set_done` which will finalize the exec section and in addition will create the element **end_time**


### Other

This is a general section where is possible to add some element specific of a method.

### Error log

In case of an error in the method, the WPS protocol doesn't return anything to the web application. 
To solve this problem, it is recommended to put all the code in a try catch block, and use the error log section
to indicate the result of the method execution. It is also necessary to provide all the output file expected by the WPS protocol.
This is done using some mock (empty) output files.

In case of success execution. as see in the exec info section, it is present the `set_done` function which will
create the error_log section containing the code equals to 0 and a default message.

In case of error in the method excution, the logmng class provides a function to handle this situation:

- `def handle_exc(self, traceback_exc: str, exc_msg: str, err_code: int)`: this function must receive some info regarding the
    execution error and the error code to send to the application. Then this function will create the error_log section in the json
    and will copy also the mock output files from the mock directory in the working dir.
