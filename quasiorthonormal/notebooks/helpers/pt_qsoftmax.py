import torch

def qsoftmax(x, basis):
       qx = torch.mm(torch.tensor(basis),
                     x.unsqueeze(0).t()).t().squeeze()
       return torch.nn.functional.softmax(qx,dim=0)
