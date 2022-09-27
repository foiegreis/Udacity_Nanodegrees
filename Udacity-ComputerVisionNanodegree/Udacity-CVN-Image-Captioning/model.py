import torch
import torch.nn as nn
import torchvision.models as models


class EncoderCNN(nn.Module):
    """
    Encoder
    We'll load the pretrained model and replace the last fc layer
    We use a Resnet50 pretrained cnn architecture
    """
    def __init__(self, embed_size):
        super(EncoderCNN, self).__init__()
        resnet = models.resnet50(pretrained=True) #pretrained RESNET 50
        for param in resnet.parameters():
            param.requires_grad_(False)
        
        modules = list(resnet.children())[:-1]
        self.resnet = nn.Sequential(*modules)
        self.embed = nn.Linear(resnet.fc.in_features, embed_size)
        
    def forward(self, images):
        """ Extract the image feature vector"""
        features = self.resnet(images)
        features = features.view(features.size(0), -1)
        features = self.embed(features)
        return features
    

class DecoderRNN(nn.Module):
    """ 
    Decoder  
    
    @param:    embed_size    Dimensionality of image and word embeddings
    @param:    hidden_size   Dimensionality of hidden state in the RNN decoder
    @param:    vocab_size    Size of vocabolary
    @param:    num_layers    Number of layers
    """
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers=1):
        
        super(DecoderRNN, self).__init__()
        
        self.hidden_size= hidden_size
        #Embedding layer
        self.word_embeddings = nn.Embedding(vocab_size, embed_size)
        
        #The lstm takes embedded vectors and outputs hidden states of hidden size
        self.lstm = nn.LSTM(input_size = embed_size,
                            hidden_size = hidden_size,
                            num_layers = num_layers,
                            batch_first = True)
        
        #The linear layer maps the hidden state output dimension 
        self.linear = nn.Linear(hidden_size, vocab_size)
    
    def forward(self, features, captions):
        """Extracts the image feature vectors"""
        
        captions = captions[:,:-1]
        embeddings = self.word_embeddings(captions)
        
        #Concat features to embeddings
        inputs = torch.cat((features.unsqueeze(1), embeddings), 1)
        
        lstm_out, hidden = self.lstm(inputs)
        outputs = self.linear(lstm_out)
        
        return outputs


    def sample(self, inputs, states=None, max_len=20):
        """
        Accepts pre-processed image tensor (inputs) and returns predicted sentence (list of tensor ids of length max_len)
        """
        res = []
        for i in range(max_len):
            
            lstm_out, states = self.lstm(inputs, states)

            lstm_out = lstm_out.squeeze(1)
            lstm_out = lstm_out.squeeze(1)
            outputs = self.linear(lstm_out)
            
            #Max probability
            target_index = outputs.max(1)[1]
            
            #Append the result to the res list
            res.append(target_index.item())
            
            #Update input for the next iteration
            inputs = self.word_embeddings(target_index).unsqueeze(1)
            
        return res
    
    
    