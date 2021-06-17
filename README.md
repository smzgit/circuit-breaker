# circuit-breaker
A circuit breaker acts as a proxy for operations that might fail. The proxy basically monitors the number of recent failures that have occurred, and use this information to decide whether to allow the operation to proceed, or simply return an exception immediately.
