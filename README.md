# circuit-breaker


Implemented the Circuit Breaker design pattern, popularized by Michael Nygard for checking health(or availability) of any service.</br>A circuit breaker acts as a proxy for operations that might fail. The proxy basically monitors the number of recent failures that have occurred, and use this information to decide whether to allow the operation to proceed, or simply return an exception immediately.</br> More details : https://docs.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
