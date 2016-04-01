import time
import sys
import random
import thread
import threading
import json

'''
Before the test is administered the police would be prompted
to enter basic information about the suspect. These characteristics
would be simple for the police to observe by looking at vehicle 
information and personal identification. From experience, the 
geolocation of police cars are tracked to within 6 places of accuracy.
In this program a random location in the United States is generated.
'''
def start_test():
    name = raw_input('Enter suspect name: ')
    height = raw_input('Enter suspect height: ')
    weight = raw_input('Enter suspect weight: ')
    car_make = raw_input('Enter car make and model: ')
    return {
        'name': name,
        'height': height,
        'weight': weight,
        'model': car_make,
        'location':
        {
            'longitude': round((70 + 40*random.random()), 6),
            'latitude': round((30 + 20*random.random()), 6)
        }
    }

'''
Taking the measurement would be very similar to what is currently done 
in practice. The improved product would dictate if and when the measurement 
is displayed. In this simplified program, a random BAC to three decimal places
of accuracy is generated
'''
def take_measurement():
    return round(random.randint(1, 160)/float(1000), 3)

def display_timer(delay):
    for remaining in range(60*delay, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining)) 
        sys.stdout.flush()
        time.sleep(1)

if __name__ == '__main__':
    test_info = start_test()
    print
    start = raw_input('Enter any key to take initial measurement: ')

    '''
    Takes measurement and stores value but display value to police.
    The reason for storing value is for data analysis purposes.
    '''
    bac = take_measurement()
    measurements = {time.strftime('%c'):bac}

    #enforced time delay
    #1 minute is used for proof of concept but time can easily adjusted
    time_delay = 1 #minutes
    print 'You must wait {} minutes before retaking test for test to be valid'.format(time_delay)
    print 'Employ standard sobriety checks during waiting period'
    display_timer(time_delay)


    '''
    Time delay is up, allows police an allotted time to administer another reading
    This simplified program allows only one additional measurement, but it could easily
    be configured to allow more. 
    '''
    available_time = 1 #minutes
    print
    print 'You have {} minutes to retake test'.format(available_time)   
    timer = threading.Timer(60*available_time, thread.interrupt_main)
    retest = None
    try:
        timer.start()
        retest = raw_input('Enter a key to take test: ')
    except KeyboardInterrupt:
        pass
    timer.cancel()
    if retest:
        bac = take_measurement()
        print 'Suspect BAC: {}'.format(bac)
        measurements[time.strftime('%c')] = bac

    '''
    Outputs the final output to a file. In reality this could be stored in the device
    and then uploaded to a secure database later. Data is stored in JSON format making
    it convenient to use in document-based databases, a very popular technology for 
    data analysis
    '''
    if len(measurements) != 2:
        print 'Failed to take test, no output written'
        sys.exit()
    test_info['measurements'] = measurements
    filename = test_info['name'] + '.json'
    with open(filename, 'w') as f:
        f.write(json.dumps(test_info))
    print 'Output written to {}'.format(filename)
