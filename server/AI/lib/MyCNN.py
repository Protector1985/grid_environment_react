import torch.nn as nn
import torch.optim as optim
import torch

class MyCNN(nn.Module):
    
    def __init__(self):
        super(MyCNN, self).__init__()
    
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=64, stride=1, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv2 = nn.Conv2d(in_channels=64, out_channels=64, stride=1, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=64, stride=1, kernel_size=3, padding=1)
        self.relu3 = nn.ReLU()
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv4 = nn.Conv2d(in_channels=64, out_channels=64, stride=1, kernel_size=3, padding=1)
        self.relu4 = nn.ReLU()
        self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv5 = nn.Conv2d(in_channels=64, out_channels=64, stride=1, kernel_size=3, padding=1)
        self.relu5 = nn.ReLU()
        self.pool5 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv6 = nn.Conv2d(in_channels=64, out_channels=64, stride=1, kernel_size=3, padding=1)
        self.relu6 = nn.ReLU()
        self.pool6 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv7 = nn.Conv2d(in_channels=64, out_channels=64, stride=1, kernel_size=3, padding=1)
        self.relu7 = nn.ReLU()
        self.pool7 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv8 = nn.Conv2d(in_channels=64, out_channels=64, stride=1, kernel_size=3, padding=1)
        self.relu8 = nn.ReLU()
        self.pool8 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv9 = nn.Conv2d(in_channels=64, out_channels=64, stride=1, kernel_size=3, padding=1)
        self.relu9 = nn.ReLU()
        self.pool9 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv10 = nn.Conv2d(in_channels=64, out_channels=64, stride=1, kernel_size=3, padding=1)
        self.relu10 = nn.ReLU()
        self.pool10 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv11 = nn.Conv2d(in_channels=64, out_channels=64, stride=1, kernel_size=3, padding=1)
        self.relu11 = nn.ReLU()
        # self.pool11 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv12 = nn.Conv2d(in_channels=64, out_channels=64, stride=1, kernel_size=3, padding=1)
        self.relu12 = nn.ReLU()
        
        self.linear1 = nn.Linear(in_features=68, out_features=32)
        self.relu13 = nn.ReLU()
        self.output = nn.Linear(in_features=32, out_features=4)
        
        
        self.lossFunction = torch.nn.MSELoss()
        self.losses = []
        self.optimizer = optim.Adam(self.parameters(), lr=1e-3)
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
        
    def back_propogation(self, qvals, gamma, reward, action, available_moves):
        Y = reward + gamma * torch.max(qvals, dim=1)[0]
        
      
        index_tensor = torch.tensor([self.find_key_by_value(action)], dtype=torch.int64)
        X = qvals.gather(dim=1, index=index_tensor.unsqueeze(1))
        
        X = X.squeeze()
        Y = Y.squeeze()
        
        loss = self.lossFunction(X, Y.detach())
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.losses.append(loss.item())
        
        return self.losses
    def back_propogation_experience(self, q1, Y, action_batch):
        #q1 shape is 6,4 and action batch is 6. need to expand in dim 1 to make it 6, 1
        
        action_indexes = action_batch.long().unsqueeze(1)
        
        X = q1.gather(dim=1, index=action_indexes)
        
        #X is of shape 6,1 need to squeeze it to 6.
        X = X.squeeze()
        
        #IMPORTANT -- WE NEED Y to be detached since it's values need to stay the same!
        loss = self.lossFunction(X, Y.detach())
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.losses.append(loss.item())
       
        return self.losses
        
        
    def forward(self, image, direction):
        x = self.conv1(image)
        x = self.relu1(x)
        x = self.pool1(x)
        
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        
        x = self.conv3(x)
        x = self.relu3(x)
        x = self.pool3(x)
        
        x = self.conv4(x)
        x = self.relu4(x)
        x = self.pool4(x)
        
        x = self.conv5(x)
        x = self.relu5(x)
        x = self.pool5(x)
        
        x = self.conv6(x)
        x = self.relu6(x)
        x = self.pool6(x)
        
        x = self.conv7(x)
        x = self.relu7(x)
        x = self.pool7(x)
        
        x = self.conv8(x)
        x = self.relu8(x)
        x = self.pool8(x)
        
        x = self.conv9(x)
        x = self.relu9(x)
        x = self.pool9(x)
        
        x = self.conv10(x)
        x = self.relu10(x)
        x = self.pool10(x)
        
        
        x = self.conv11(x)
        x = self.relu11(x)
        # x = self.pool11(x)
        
        x = self.conv12(x)
        x = self.relu12(x)
        
        flattened_x = x.view(x.size(0), -1)
       
        x = torch.cat([flattened_x, direction], dim=1)
        x = self.linear1(x)
        x = self.relu13(x)
        x = self.output(x)
    
        return x