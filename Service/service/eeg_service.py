import config
import os
import torch
import torch.nn as nn

from sklearn.model_selection import train_test_split


# 定义神经网络模型
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(128, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x

file_path = os.path.join(config.project_folder, 'Algorithm', 'EEG', 'eeg_mdd', 'best_model.pth')
model = Model()

model.load_state_dict(torch.load(file_path))
model.eval()

def eeg_depression(data):
    input_tensor = torch.tensor(data).float()
    with torch.no_grad():
        output = model(input_tensor)
    return torch.round(output)

