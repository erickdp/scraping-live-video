import os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import requests


# Main Function
def record():
    session = requests.Session()

    # Enable Performance Logging of Chrome.
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    # Create the webdriver object and pass the arguments
    options = webdriver.ChromeOptions()

    # Chrome will start in Headless mode
    options.add_argument('headless')

    # Ignores any certificate errors if there is any
    options.add_argument("--ignore-certificate-errors")

    # Startup the chrome webdriver with executable path and
    # pass the chrome options and desired capabilities as
    # parameters.
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options,
                              desired_capabilities=desired_capabilities)

    # Send a request to the website and let it load
    driver.get("https://www.dailymotion.com/embed/video/x7wijay?autoplay=1")

    # Opens a writable JSON file and writes the logs in it
    count = 0
    flag = True
    countdown_recording = 66  # 1 min - 6 for delay

    with open('video.ts', 'wb+') as live_video:

        while flag:

            logs = driver.get_log("performance")

            # Iterates every logs and parses it using JSON
            for log in logs:
                network_log = json.loads(log["message"])["message"]

                # Checks if the current 'method' key has any
                # Network related value.
                if "Network.responseReceived" == network_log["method"]:
                    ts_file = str(network_log['params']['response']['url']) if str(
                        network_log['params']['response']['url']) else None
                    # Writes the network log to a JSON file by
                    # converting the dictionary to a JSON string
                    # using json.dumps().
                    index = ts_file.find('.ts')
                    if index != -1:
                        if count > 2:
                            print(ts_file)
                            r = session.get(ts_file)
                            live_video.write(r.content)
                            print('writed'.center(50, '-'))
                        else:
                            count = count + 1

                        if countdown_recording > 0:
                            countdown_recording -= 3
                        else:
                            flag = False


if __name__ == '__main__':
    record()
    print('You should open video.ts with VCL.'.center(60, '_'))
