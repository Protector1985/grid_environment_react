from PIL import Image
import base64
from io import BytesIO
import random

class Resnet:
    
    def pick_random_move():
        moves = {
            0: "DOWN",
            1: "UP",
            2: "LEFT",
            3: "RIGHT"
        }

        # Randomly pick one of the keys
        random_key = random.choice(list(moves.keys()))

        # Return the selected move
        return {"makeMove": moves[random_key]}
    
    
    def resnet_processor(self, data_url):
        
        #buffer from node.js => image
        data = data_url['dataURL']
        header, encoded = data.split(",", 1)
        data = base64.b64decode(encoded)

        # The decoded data can be used as a file-like object
        image = Image.open(BytesIO(data))
        
        #show the image to check if it was transmitted correctly
        # image.show()
        
        def pick_random_move():
            moves = {
                0: "DOWN",
                1: "UP",
                2: "LEFT",
                3: "RIGHT"
            }

            # Randomly pick one of the keys
            random_key = random.choice(list(moves.keys()))

            # Return the selected move
            return {"makeMove": moves[random_key]}
        
        
        
        
        return pick_random_move()
        
       
        
       
        
        