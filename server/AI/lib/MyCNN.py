import torch.nn as nn
import torch.optim as optim
import torch

class MyCNN(nn.Module):
    
    def __init__(self):
        super(MyCNN, self).__init__()
    
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, stride=1, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=16, stride=1, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv3 = nn.Conv2d(in_channels=16, out_channels=16, stride=1, kernel_size=3, padding=1)
        self.relu3 = nn.ReLU()
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.linear1 = nn.Linear(in_features=28676, out_features=120)
        self.relu4 = nn.ReLU()
        self.output = nn.Linear(in_features=120, out_features=4)
        
        
        self.lossFunction = torch.nn.MSELoss()
        self.losses = []
        self.optimizer = optim.Adam(self.parameters(), lr=1e-3)
        
    def back_propogation(self, q1, Y, action_batch):
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
        
        flattened_x = x.view(x.size(0), -1)

        x = torch.cat([flattened_x, direction], dim=1)
        x = self.linear1(x)
        x = self.relu4(x)
        x = self.output(x)
    
        return x