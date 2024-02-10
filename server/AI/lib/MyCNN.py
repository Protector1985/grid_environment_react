import torch.nn as nn
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
        self.relu2 = nn.ReLU()
        self.output = nn.Linear(in_features=120, out_features=4)
        
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
        x = self.relu2(x)
        x = self.output(x)
    
        return x