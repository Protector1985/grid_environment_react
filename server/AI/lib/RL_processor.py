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
        self.total_rewards = []
        self.decayAmount = 0.0002
        self.move_number = 0
        self.cachedStates = []
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
        
    def pushState(self, image_state):
        if len(self.cachedStates) < 2:
            self.cachedStates.append(image_state)
        elif len(self.cachedStates) == 2:
            self.cachedStates.pop(0)
            self.cachedStates.append(image_state)
            
            
  
  
    def pre_processor(self, observed_image, observed_direction, max_size=1024 ):
        
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
        losses_arr = []
        bufferLength = 0
        average_loss = 0
        #buffer from node.js => image
        header, encoded = b64_img.split(",", 1)
        
        data = base64.b64decode(encoded)
        reward = incoming_move_data['reward']
        move_direction = incoming_move_data['direction']
       
        # The decoded data can be used as a file-like object
        image = Image.open(BytesIO(data))
        
        exp = [image, reward, move_direction]
        
        '''adds image to cache state so that previous image can be retrieved
        for direction and reward that is coming with the new data.'''
        self.pushState(image)
        
    
        if len(self.cachedStates) == 2:
            image_tensor, direction_tensor = self.pre_processor(self.cachedStates[1], move_direction)
            qval = cnn.forward(image_tensor, direction_tensor)
            
            losses = cnn.back_propogation(qval, self.gamma, reward, move_direction, self.moves)
            losses_arr = losses
           
        # experience.partial_experience(exp)
        # replay_result = experience.run_experience_replay(cnn, self.gamma)
        
        
        # if replay_result != None:
        #     q1, Y, action_batch, bufferLength = replay_result
        #     losses = cnn.back_propogation_experience(q1, Y, action_batch)
            
       
        if self.epsilon > 0.01:
            self.epsilon -= self.decayAmount
        
   
        if random.random() < self.epsilon:
            action_ = self.pick_random_move()
            action_ = self.find_key_by_value(action_)
        else: 
            action_ = torch.argmax(qval.detach()).item()      
        del image
        
        
        if len(losses_arr) > 0:
            average = sum(losses) / len(losses)
            average_loss = average
        
    
        self.move_number += 1
        self.total_rewards.append(reward)
        rewards_combined = sum(self.total_rewards)
        
        if self.move_number % 100 == 0:
            print(f"Action Number: {self.move_number}, Average Loss: {average_loss}, Total Reward: {rewards_combined}, Epsilon: {self.epsilon}, Buffer Length:{bufferLength}") 
            
        return {"makeMove": self.moves[action_]}
        
        
        
        #TEST CODE WITHOUT NEURAL NET
        # action_ = self.pick_random_move()
        # action_ = self.find_key_by_value(action_)
        # return {"makeMove": self.moves[action_]}
        
       
        
       
        
        