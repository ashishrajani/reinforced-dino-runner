from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# chrome driver path
chrome_driver_path = "./driver/chromedriver"

# game url
game_url = "chrome://dino"

# create id for canvas for faster selection from DOM
init_script = "document.getElementsByClassName('runner-canvas')[0].id = 'runner-canvas'"


class Game:
    # Interface class for interacting with the environment

    def __init__(self):
        # Launch the browser window using the attributes in chrome_options

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--mute-audio')

        self._driver = webdriver.Chrome(chrome_driver_path, chrome_options=chrome_options)
        self._driver.set_window_position(x=-10, y=0)

        try:
            self._driver.get(game_url)
        except:
            print('Running offline..')

        self._driver.execute_script("Runner.config.ACCELERATION=0")
        self._driver.execute_script(init_script)

    def get_driver(self):
        return self._driver

    def is_crashed(self):
        # return true if the agent as crashed on an obstacles. Gets javascript variable from game describing the state

        return self._driver.execute_script("return Runner.instance_.crashed")

    def is_playing(self):
        # return true if game is in progress, false is crashed or paused

        return self._driver.execute_script("return Runner.instance_.playing")

    def get_score(self):
        # gets current game score from javascript variables.

        score_array = self._driver.execute_script("return Runner.instance_.distanceMeter.digits")

        # converting score digits array to score string
        # eg: [1,0,0] => 100
        score = ''.join(score_array)

        return int(score)

    def press_up(self):
        # sends a single to press up get to the browser

        self._driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_UP)

    def press_down(self):
        # sends a single to press down get to the browser

        self._driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_DOWN)

    def restart(self):
        # sends a signal to browser-javascript to restart the game

        self._driver.execute_script("Runner.instance_.restart()")

    def pause(self):
        # pause the game

        return self._driver.execute_script("return Runner.instance_.stop()")

    def resume(self):
        # resume a paused game if not crashed

        return self._driver.execute_script("return Runner.instance_.play()")

    def end(self):
        # close the browser and end the game

        self._driver.close()
