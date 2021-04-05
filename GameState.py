from PIL import Image
from Game import Game
from io import BytesIO
from Agent import Agent
from DataLoader import DataLoader

import cv2
import base64
import numpy as np

# get image from canvas
getbase64Script = "canvasRunner = document.getElementById('runner-canvas'); \
return canvasRunner.toDataURL().substring(22)"


class GameState:
    def __init__(self, agent: Agent, game: Game, data_loader: DataLoader):
        self._agent = agent
        self._game = game
        self._data_loader = data_loader

        # display the processed image on screen using openCV, implemented using python coroutine
        self._display = self._show_image()

        # initiliaze the display coroutine
        self._display.__next__()

    def get_state(self, actions):
        # storing actions in a dataframe
        self._data_loader.store_action(actions[1])

        score = self._game.get_score()
        reward = 0.1
        is_over = False

        # game over
        if actions[1] == 1:
            print('Jump')
            self._agent.jump()

        image = self._grab_screen(self._game.get_driver())

        # display the image on screen
        self._display.send(image)

        if self._agent.is_crashed():
            print('crashed')
            # log the score when game is over
            self._data_loader.store_scores(score)
            self._game.restart()
            reward = -1
            is_over = True

        # return the Experience tuple
        return image, reward, is_over

    def _grab_screen(self, _driver):
        image_b64 = _driver.execute_script(getbase64Script)

        screen = np.array(Image.open(BytesIO(base64.b64decode(image_b64))))

        # processing image as required
        image = self.process_img(screen)
        return image

    def _show_image(self, graphs=False):
        # Show images in new window

        while True:
            screen = (yield)
            window_title = "logs" if graphs else "game_play"
            cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
            imS = cv2.resize(screen, (800, 400))
            cv2.imshow(window_title, screen)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        return

    def process_img(self, image: np.ndarray):
        # RGB to Grey Scale
        processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Crop Region of Interest(ROI)
        processed_image = processed_image[:300, :500]

        processed_image = cv2.resize(processed_image, (80, 80))
        return processed_image
