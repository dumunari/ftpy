### FTPy

[Pyftpdlib](https://github.com/giampaolo/pyftpdlib) based FTP Server created to be used on performance tests.

### Running 
You may run 
* ```python setup.py develop```

If everything turns out ok, you may call ftpy from your command line

* You may run ```ftpy --help``` to get more info on settings.

### Implemented features
When running FTPy server, you may configure some settings to simulate some performance problems.

* ```-md, --max-delay```
    * Max delay on STOR and RETR, in seconds. Min is always set to 1s. Will have no effect if delay-rate is 0. 
    * **Defaults to 5s.**
* ```-dr, --delay-rate```
    * Desired delay rate on STOR and RETR, from 0 to 10, where 1 means 10%. 0 means no delay. 
    * **Defaults to 80%.**
* ```-fr, --failure-rate```
    * Desired failure rate on STOR and RETR, from 1 to 10, where 1 means 10%. 0 means no failure rate. 
    * **Defaults to 50%.**
* ```-mc, --max-conns```
    * General server maximum connections. (Pyftpdlib native feature)
    * **Defaults to none.** 
* ``` -mci, --max-conns-ip```
    * Maximum connections per client ip. (Pyftpdlib native feature)
    * **Defaults to none.** 
* ```-p, --port```
    * Server port. 
    * **Defaults to 2121.**
    
    
### Running the tests
Although we are using an already (and very well) tested library, some of our implementations must be tested to assure 
we are not breaking everything up.

At the project root folder:
* To run our unit tests: 
  * ```pytest```
* To run our integration tests: 
  * ```pytest -v tests/integration```
* To run all tests:
  * ```pytest -v tests```
* To run all tests with coverage:
  * ```pytest --cov=src tests```
* To run mutation tests:
  * ```mutmut run```



