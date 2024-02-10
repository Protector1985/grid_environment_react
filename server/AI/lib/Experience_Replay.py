

#layout [imageData_current, reward_current, move_direction_current, imageData_previous_step, reward_previous_step, move_direction__previous_step,]
class Experience_Replay:
    
    def __init__(self):
        self.capacity = 100
        self.buffer = []
        self.position = 0
        self.partial = []
        
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
        print(self.buffer)
        