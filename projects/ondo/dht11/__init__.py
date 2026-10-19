import time
import RPi
#-----------------------------------------------------------------------
class SomeError(Exception):
    pass

class DHT11Result:
    'DHT11 sensor result returned by DHT11.read() method'

    ERR_NO_ERROR = 0
    ERR_MISSING_DATA = 1
    ERR_CRC = 2
    ERR_ETC = 3

    error_code = ERR_NO_ERROR
    temperature = -1
    humidity = -1

    def __init__(self, error_code, temperature, humidity):
        self.error_code = error_code
        self.temperature = temperature
        self.humidity = humidity

    def is_valid(self):
        return self.error_code == DHT11Result.ERR_NO_ERROR
#-----------------------------------------------------------------------
class DHT11:
    'DHT11 sensor reader class for Raspberry'

    __pin = 0

    def __init__(self, pin):
        self.__pin = pin

    def read(self):
        # try=1, retry=6
        tryCnt = 7
        while tryCnt > 0:
            try:
#                print('*', flush=True, end='')
                RPi.GPIO.setup(self.__pin, RPi.GPIO.OUT, initial=RPi.GPIO.HIGH)
                time.sleep(0.5)      # wait a few time(500ms)

                self.__send_and_sleep(RPi.GPIO.HIGH, 0.05)  # send initial high
                self.__send_and_sleep(RPi.GPIO.LOW, 0.02)   # pull down to low and waitr(20ms)
                data = self.__collect_input()               # collect data into an array
                # parse lengths of all data pull up periods
                # if bit count mismatch, return error (4 byte data + 1 byte checksum)
                pull_up_lengths = self.__parse_data_pull_up_lengths(data)
                if len(pull_up_lengths) != 40:
                    raise SomeError('40bit recieve error ... [{}]'.format(len(pull_up_lengths)))
                #    return DHT11Result(DHT11Result.ERR_MISSING_DATA, 0, 0)

                # the_bytes[0]: humidity int
                # the_bytes[1]: humidity decimal
                # the_bytes[2]: temperature int
                # the_bytes[3]: temperature decimal
                # the_bytes[4]: checksum
                # The meaning of the return sensor values and checksum
                the_bytes = self.__calculate_bits(pull_up_lengths)
                checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xff
                if the_bytes[4] != checksum:
                     raise SomeError('checksum error ... [{}][{}][{}][{}]~[{}]!=[{}]'.format(the_bytes[0], the_bytes[1],the_bytes[2],the_bytes[3],the_bytes[4],checksum))
#                    print('checksum error ... [{}][{}][{}][{}]~[{}]!=[{}]'.format(the_bytes[0], the_bytes[1],the_bytes[2],the_bytes[3],the_bytes[4],checksum))
                #    return DHT11Result(DHT11Result.ERR_CRC, 0, 0)

                # ok, we have valid data
                humidity = the_bytes[0] + float(the_bytes[1]) / 10.0
                temperature = the_bytes[2] + float(the_bytes[3] & 0x7f) / 10.0
                if the_bytes[3] & 0x80 != 0:
                    temperature = -temperature 
                # ok return
#                print(tryCnt, end=' ')
                return DHT11Result(DHT11Result.ERR_NO_ERROR, temperature, humidity)
            except SomeError as e:
#                print(e)
                tryCnt -= 1
                time.sleep(2)
            
        # retry over error return
#        print('Error ... ', end=' ')
        return DHT11Result(DHT11Result.ERR_ETC, 0, 0)
#-----------------------------------------------------------------------
    def __send_and_sleep(self, output, sleep):
        RPi.GPIO.output(self.__pin, output)
        time.sleep(sleep)
        return
#-----------------------------------------------------------------------
    def __collect_input(self):
        unchanged_count = 0
        max_unchanged_count = 200
        last = -1
        data = []

        # change to input
        RPi.GPIO.setup(self.__pin, RPi.GPIO.IN)

        while unchanged_count <= max_unchanged_count:
            current = RPi.GPIO.input(self.__pin)
            data.append(current)
            if last != current:
                last = current
                unchanged_count = 0
            unchanged_count += 1

        return data
#-----------------------------------------------------------------------
    def __parse_data_pull_up_lengths(self, data):
        lengths = []
        data_length = len(data)
        flg = 0
        for i in range(data_length):
            if flg == 0 and data[i] == RPi.GPIO.LOW:  flg = 1
            if flg == 1 and data[i] == RPi.GPIO.HIGH: flg = 2
            if flg == 2 and data[i] == RPi.GPIO.LOW:  break

        if i >= data_length:
            return lengths

        current_length = 0
        for j in range(i, data_length):
            if data[j] == RPi.GPIO.HIGH:
                current_length += 1
            elif data[j] == RPi.GPIO.LOW:
                if current_length > 0:
                    lengths.append(current_length)
                    current_length = 0

        return lengths
#-----------------------------------------------------------------------
    def __calculate_bits(self, pull_up_lengths):
        halfway = (min(pull_up_lengths) + max(pull_up_lengths)) / 2
        bits = 0
        for cnt in pull_up_lengths:
            bits <<= 1
            if cnt >= halfway:
                bits |= 1

        the_bytes = [
            (bits >> 32) & 0xff,
            (bits >> 24) & 0xff,
            (bits >> 16) & 0xff,
            (bits >>  8) & 0xff,
            (bits      ) & 0xff
        ]

        return the_bytes
