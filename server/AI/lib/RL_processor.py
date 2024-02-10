from PIL import Image
import base64
from io import BytesIO
import random

class RL_PROCESSOR:
    
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
    
    
    def rl_processor(self, b64_img, incoming_move_data):
        
        #buffer from node.js => image
        header, encoded = b64_img.split(",", 1)
        
        data = base64.b64decode(encoded)
        print(incoming_move_data)
        # The decoded data can be used as a file-like object
        image = Image.open(BytesIO(data))
       
        #show the image to check if it was transmitted correctly
        #image.show()
        
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
        
        
        
        del image
        return pick_random_move()
        
       
        
       
        
        