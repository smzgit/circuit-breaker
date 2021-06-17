import requests
import time

class circuit_breaker():
    current_state = "closed"
    FAILURE_COUNT = None
    TIMEOUT_LIMIT = None

    def __init__(self,failure_count,timeout):
        circuit_breaker.FAILURE_COUNT = failure_count
        circuit_breaker.TIMEOUT_LIMIT = timeout
        print("Failure count: ",circuit_breaker.FAILURE_COUNT)
        print("Timeout: ",circuit_breaker.TIMEOUT_LIMIT)

    def operation_healthcheck(self):
        response = None
        #response = requests.get('http://ilgss0385:8080/api/management/healthcheck')
        print("\nCHECKING HEALTH...")
        response = type('obj', (object,), {'status_code' : 0, 'text' : None})
        try:
            response = requests.get('http://ilgss0396:8080/',timeout=5)
        except Exception as e:
            print("Error in Checking Health => ",e)
        return response

    def closed(self):
        if circuit_breaker.current_state == 'closed':
            print('\n+++++++++++++++++++++++++++++++++++++++++++++')
            print('\t\t\tSTATE : CLOSED', '\n')
            failure_counter = 0
            while (failure_counter < circuit_breaker.FAILURE_COUNT):
                try:
                    response = self.operation_healthcheck()
                    resp = response.status_code
                    print("\tStatus Code : ",response.status_code)
                    with open("feature_flag.txt", 'w', encoding='utf-8') as f:
                        f.write(str(response.status_code))
                    if int(resp) == 200:
                        circuit_breaker.current_state = "closed"
                        print("response Status Code : ",resp)
                        return
                    else:
                        print("Failure Counter => ", failure_counter, " & Threshold = ", circuit_breaker.FAILURE_COUNT)
                        failure_counter += 1
                except Exception as e:
                    print(e)
                    print("Failure Counter => ",failure_counter," & Threshold = ",circuit_breaker.FAILURE_COUNT)
                    failure_counter += 1
                time.sleep(2)
            else:
                print("Failure Counter exceeded -> going in Open state")
                circuit_breaker.current_state = "open"
                self.open_cb()
        else:
            raise Exception("Invoked wrong state :open, current_state = ", circuit_breaker.current_state)


    def open_cb(self):
        if circuit_breaker.current_state == 'open' :
            print('\n+++++++++++++++++++++++++++++++++++++++++++++')
            print('\t\t\tSTATE : OPEN', '\n')
            circuit_breaker.current_state = "open"
            print("Started a timeout for ",circuit_breaker.TIMEOUT_LIMIT," seconds\n")
            time.sleep(circuit_breaker.TIMEOUT_LIMIT)
            print("Now checking health again...")
            circuit_breaker.current_state = 'half_open'
            self.half_open()
        else:
            raise Exception("Invoked wrong state :open, current_state = ",circuit_breaker.current_state)

    def half_open(self):
        if circuit_breaker.current_state == 'half_open':
            print('\n+++++++++++++++++++++++++++++++++++++++++++++')
            print('\t\t\tSTATE : HALF-OPEN', '\n')
            try:
                response = self.operation_healthcheck()
                if response.status_code in [200, 299]:
                    circuit_breaker.current_state = "closed"
                    self.closed()
                else:
                    circuit_breaker.current_state = "open"
                    self.open_cb()
            except Exception as e:
                print(e)
                circuit_breaker.current_state = "open"
                self.open_cb()

        else:
            raise Exception("Invoked wrong state :half_open, current_state = ",circuit_breaker.current_state)

cb= circuit_breaker(3,5)
cb.closed()
