from PIL import Image
import base64
from io import BytesIO
import random
import torch
import torch.nn.functional as torchFunc
import torchvision.transforms as transforms
from lib.MyCNN import MyCNN
from lib.Experience_Replay import Experience_Replay
import numpy as np


experience = Experience_Replay()
cnn = MyCNN()


class RL_PROCESSOR:
    
    
    def __init__(self):
        self.gamma = 0.9
        self.epsilon = 1.0
        self.decayAmount = 0.0001
        self.moves = {
                0: "DOWN",
                1: "UP",
                2: "LEFT",
                3: "RIGHT"
            }
        self.experiences = []
        
    def feed_to_model(self, observation):
        image_tensor, direction_tensor = observation
        

        
    def find_key_by_value(self, value_to_find):
        for key, value in self.moves.items():
            if value == value_to_find:
                return key

    def pick_random_move(self):
            # Randomly pick one of the keys
            random_key = random.choice(list(self.moves.keys()))

            # Return the selected move
            return self.moves[random_key]
  
  
    def pre_processor(self, observed_image, observed_direction, max_size=256):
        
        transform = transforms.Compose([
            transforms.Resize(max_size),  # Resizes the smaller edge to max_size while maintaining aspect ratio
            transforms.ToTensor(),  # Convert the PIL Image to a tensor
            transforms.Lambda(lambda x: x[:3, :, :]),  # Keep only the first 3 channels (RGB)
            transforms.Lambda(lambda x: x / 255)
        ])
        
        image_tensor = transform(observed_image)
        image_tensor = image_tensor.unsqueeze(0)

        
        direction_key = self.find_key_by_value(observed_direction)
        direction_tensor = torch.tensor(direction_key)
        direction_tensor = torchFunc.one_hot(direction_tensor, num_classes=4).float()
        direction_tensor = direction_tensor.unsqueeze(0)
        
        return image_tensor, direction_tensor
    
   
    
    def decide_action(self, b64_img, incoming_move_data):
        
        #buffer from node.js => image
        header, encoded = b64_img.split(",", 1)
        
        data = base64.b64decode(encoded)
        reward = incoming_move_data['reward']
        move_direction = incoming_move_data['direction']
       
        # The decoded data can be used as a file-like object
        image = Image.open(BytesIO(data))
     
        exp = [image, reward, move_direction]
        
        image_tensor, direction_tensor = self.pre_processor(image, move_direction)
        qval = cnn.forward(image_tensor, direction_tensor)
        
        
        experience.partial_experience(exp)
        replay_result = experience.run_experience_replay(cnn, self.gamma)
        
        losses = []
        if replay_result != None:
            q1, Y, action_batch = replay_result
            losses = cnn.back_propogation(q1, Y, action_batch)
       
   
        if self.epsilon > 0.01:
            self.epsilon -= self.decayAmount
        
   
        if random.random() < self.epsilon:
            action_ = self.pick_random_move()
            action_ = self.find_key_by_value(action_)
        else: 
            action_ = torch.argmax(qval.detach()).item()      
        del image
        
        average_loss = 0
        if len(losses) > 0:
            average_loss = sum(losses) / len(losses)
        
        print(f"Average_loss: {average_loss}") 
        
        return {"makeMove": self.moves[action_]}
        
       
        
       
        
        