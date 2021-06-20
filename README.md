# circuit-breaker


Implemented the Circuit Breaker design pattern, popularized by Michael Nygard for checking health(or availability) of any service.</br>
![alt text](https://docs.microsoft.com/en-us/azure/architecture/patterns/_images/circuit-breaker-diagram.png)
</br></br>A circuit breaker acts as a proxy for operations that might fail. The proxy basically monitors the number of recent failures that have occurred, and use this information to decide whether to allow the operation to proceed, or simply return an exception immediately.</br>It can prevent an application from repeatedly trying to execute an operation that's likely to fail. Allowing it to continue without waiting for the fault to be fixed or wasting CPU cycles while it determines that the fault is long lasting. The Circuit Breaker pattern also enables an application to detect whether the fault has been resolved. If the problem appears to have been fixed, the application can try to invoke the operation.

</br> More details : https://docs.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
