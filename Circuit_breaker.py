from abc import abstractmethod

class circuit_breaker():
    current_state = "closed"
    FAILURE_COUNT = None
    TIMEOUT_LIMIT = None

    def __init__(self,failure_count,timeout):
        circuit_breaker.FAILURE_COUNT = failure_count
        circuit_breaker.TIMEOUT_LIMIT = timeout
        print("Failure count: ",circuit_breaker.FAILURE_COUNT)
        print("Timeout: ",circuit_breaker.TIMEOUT_LIMIT)

    @abstractmethod
    def operation(self):
        '''Implement whatever operation your application
        will perform and return any response to calling
        function.'''
        pass

    @abstractmethod
    def closed(self):
        '''Closed: The request from the application is routed to the operation.
                    The proxy maintains a count of the number of recent failures, and if the
                    call to the operation is unsuccessful the proxy increments this count.
                    If the number of recent failures exceeds a specified threshold within a
                    given time period, the proxy is placed into the Open state. At this point
                    the proxy starts a timeout timer, and when this timer expires the proxy
                    is placed into the Half-Open state.'''
        pass

    @abstractmethod
    def open_cb(self):
        '''
        Open: The request from the application fails immediately and
              an exception is returned to the application.
        '''
        pass

    @abstractmethod
    def half_open(self):
        '''Half-Open: A limited number of requests from the application are allowed to pass
                     through and invoke the operation. If these requests are successful, it's assumed
                     that the fault that was previously causing the failure has been fixed and the circuit
                     breaker switches to the Closed state (the failure counter is reset). If any request
                     fails, the circuit breaker assumes that the fault is still present so it reverts back
                     to the Open state and restarts the timeout timer to give the system a further period
                     of time to recover from the failure.
                     The Half-Open state is useful to prevent a recovering service from suddenly being
                     flooded with requests. As a service recovers, it might be able to support a limited
                      volume of requests until the recovery is complete, but while recovery is in progress
                       a flood of work can cause the service to time out or fail again.

        '''
        pass
#____________________________________________________________________________________________________________
