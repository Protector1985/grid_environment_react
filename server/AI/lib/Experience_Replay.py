
import random
import torch
from torchvision import transforms
import torch.nn.functional as torchFunc
#layout [imageData_current, reward_current, move_direction_current, imageData_previous_step, reward_previous_step, move_direction__previous_step,]
class Experience_Replay:
    
    def __init__(self):
        self.capacity = 500
        self.batch_size = 3
        self.buffer = []
        self.bufferlength = len(self.buffer)
        self.position = 0
        self.partial = []
        self.moves = {
                0: "DOWN",
                1: "UP",
                2: "LEFT",
                3: "RIGHT"
            }
        
    def find_key_by_value(self, value_to_find):
        for key, value in self.moves.items():
            if value == value_to_find:
                return key
        
    def partial_experience(self, experience):
        if len(self.partial) < 2:
            self.partial.append(experience)
        else: 
            merged_array = self.partial[0] + self.partial[1]
            self.add_experience(merged_array)
            self.partial = []
        
        
    def add_experience(self, experience):
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        
        self.buffer[self.position] = experience
        self.position = (self.position + 1) % self.capacity
        
        
    def get_sample(self):
        if len(self.buffer) > self.batch_size:
            mini_batch = random.sample(self.buffer, self.batch_size)
            return mini_batch
        
    def pre_processor(self, observed_image, observed_direction):
        transform = transforms.Compose([
            # transforms.Resize(max_size),  # Resizes the smaller edge to max_size while maintaining aspect ratio
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
        
            
    def get_batches(self, mini_batch, cnn, gamma):

        if len(self.buffer) > self.batch_size:
           # Process the current and previous states
            image_tensors_state1 = torch.cat([self.pre_processor(experience[0], experience[2])[0] for experience in mini_batch])  # Current state images
            direction_tensors_state1 = torch.cat([self.pre_processor(experience[0], experience[2])[1] for experience in mini_batch])  # Current state directions

            image_tensors_state2 = torch.cat([self.pre_processor(experience[3], experience[5])[0] for experience in mini_batch])  # Previous state images
            direction_tensors_state2 = torch.cat([self.pre_processor(experience[3], experience[5])[1] for experience in mini_batch])  # Previous state directions
            
            #the most up to date reward associated with actions from previous step!
            reward_batch = torch.Tensor([experience[1] for experience in mini_batch])
            action_batch = torch.Tensor([self.find_key_by_value(experience[2]) for experience in mini_batch])
           
            q1 = cnn.forward(image_tensors_state1, direction_tensors_state1)
            
            with torch.no_grad():
                image_state2_no_grad = torch.cat([self.pre_processor(experience[3], experience[5])[0] for experience in mini_batch])  
                direction_state2_no_grad = torch.cat([self.pre_processor(experience[3], experience[5])[1] for experience in mini_batch])  
                
                #gets n batches of 4 max Q values
                last_action_Q_values = cnn.forward(image_state2_no_grad, direction_state2_no_grad )
                
                #outputs one maxQ value for each batch
                maxQvalues = torch.max(last_action_Q_values, dim=1)[0]
                Y = reward_batch + gamma * maxQvalues
                return q1, Y, action_batch
                
    def run_experience_replay(self, cnn, gamma):
        if len(self.buffer) > self.batch_size:
            bufferLength = self.bufferlength
            q1, Y, action_batch = self.get_batches(self.get_sample(), cnn, gamma)
            return q1, Y, action_batch, bufferLength
        