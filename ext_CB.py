from Circuit_breaker import circuit_breaker
import time
import requests

#Example :-
class external_CB(circuit_breaker):
    def operation(self):
        response = None
        # response = requests.get('http://ilgss0385:8080/api/management/healthcheck')
        print("\nCHECKING HEALTH...")
        response = type('obj', (object,), {'status_code': 0, 'text': None})
        try:
            response = requests.get('https://github.com/', timeout=5)
        except Exception as e:
            print("Error in Checking Health => ", e)
        return response

    def closed(self):
        if circuit_breaker.current_state == 'closed':
            print('\n+++++++++++++++++++++++++++++++++++++++++++++')
            print('\t\t\tSTATE : CLOSED', '\n')
            failure_counter = 0
            while (failure_counter < circuit_breaker.FAILURE_COUNT):
                try:
                    response = self.operation()
                    resp = response.status_code
                    print("\tStatus Code : ", response.status_code)
                    with open("feature_flag.txt", 'w', encoding='utf-8') as f:
                        f.write(str(response.status_code))
                    if int(resp) == 200:
                        circuit_breaker.current_state = "closed"
                        print("response Status Code : ", resp)
                        return
                    else:
                        print("Failure Counter => ", failure_counter, " & Threshold = ", circuit_breaker.FAILURE_COUNT)
                        failure_counter += 1
                except Exception as e:
                    print(e)
                    print("Failure Counter => ", failure_counter, " & Threshold = ", circuit_breaker.FAILURE_COUNT)
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
                response = self.operation()
                if response.status_code == 200:
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


cb= external_CB(7,10)
cb.closed()
