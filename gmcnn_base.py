import torch
import torch.nn as nn
import numpy as np

from gmcnn.gm_convolution.gmconv import GMConvBase
from gmcnn.gm_convolution.gmconv_classification import GMConvCls
from gmcnn.gm_convolution.gmconv_regression import GMConvReg
from gmcnn.gm_pooling.gmpool import GMPool
from gmcnn.utils.utils import generate_elements, get_group_matrix, kronecker_product

class GMCNNBase(nn.Module):
    """
    Base class for GMCNN models.
    Initializes the dataset-specific parameters.
    """
    def __init__(self, config):
        super().__init__()

        self.dataset = config.exp.model.dataset
        self.num_classes = config.exp.model.num_classes

        # Set vec_size and in_channels based on the dataset
        dataset_params = {
            'rot': (784, 1),
            'rot-mnist': (784, 1),  # Added to support the rot-mnist config name
            'mnist-bg-rot': (784, 1),
            'mnist-noise': (784, 1),
            'smallnorb': (576, 1),
            'norb': (1024, 1)
        }
        self.vec_size, self.in_channels = dataset_params.get(self.dataset, (1024, 3)) # default cifar10 case

    def forward(self, x):
        """
        Forward pass for the base model.
        Reshapes the input tensor based on the dataset.
        """
        # Check if input is None
        if x is None:
            raise ValueError("Input tensor is None in GMCNNBase forward method")
            
        # Check if x has valid dimensions
        if not isinstance(x, torch.Tensor):
            raise TypeError(f"Expected input to be torch.Tensor, got {type(x)}")
            
        # Handle different dataset formats
        if self.dataset in ['rot', 'rot-mnist', 'mnist', 'norb', 'smallnorb', 'mnist-noise', 'mnist-bg-rot']:
            x = x.view(-1, 1, 1, x.size(-1))
        else:
            x = x.view(-1, x.size(1), 1, x.size(-1) * x.size(-1))
        return x

class GMCNN(GMCNNBase):
    """
    GMCNN model class.
    Initializes the layers and defines the forward pass.
    """
    def __init__(self, config):
        super().__init__(config)

        self.order = config.exp.model.order
        self.group = config.exp.model.group
        self.nbr = config.exp.model.nbr
        self.lr = config.exp.model.lr
        self.dropout_rate = config.exp.model.dropout
        self.blocks = config.exp.model.blocks

        # Generate group elements and matrix
        elements = generate_elements(self.group, self.order)
        M1 = get_group_matrix(elements)
        group_matrix = np.array(kronecker_product(M1, M1))

        # Initialize layers
        self.gm_layers = nn.ModuleList()
        self.norm_layers = nn.ModuleList()
        self.conv1x1_layers = nn.ModuleList()

        in_channels = self.in_channels
        
        # Initialize GMConv and normalization layers for each block
        for block_idx, block in enumerate(self.blocks):
            block_in_channels = in_channels
            for layer_idx, out_channels in enumerate(block.out_channels):
                self.gm_layers.append(GMConvCls(self.group, self.order, self.nbr, group_matrix, out_channels))
                self.norm_layers.append(nn.LayerNorm([out_channels, 1, self.vec_size], elementwise_affine=False))
                
                # Add 1x1 convolution for residual connections if needed
                if in_channels != out_channels:
                    self.conv1x1_layers.append(nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0))
                
                in_channels = out_channels
            
            # Add 1x1 convolution for block residual if block input and output channels differ
            if block_in_channels != block.out_channels[-1]:
                self.conv1x1_layers.append(nn.Conv2d(block_in_channels, block.out_channels[-1], kernel_size=1, stride=1, padding=0))
                
        # Add 1x1 convolutions between blocks if needed
        for i in range(len(self.blocks) - 1):
            if self.blocks[i].out_channels[-1] != self.blocks[i+1].out_channels[0]:
                self.conv1x1_layers.append(
                    nn.Conv2d(
                        self.blocks[i].out_channels[-1], 
                        self.blocks[i+1].out_channels[0], 
                        kernel_size=1, 
                        stride=1, 
                        padding=0
                    )
                )

        self.pool = nn.AdaptiveMaxPool2d((1, 1))
        self.relu = nn.PReLU()
        self.fc1 = nn.Linear(in_channels, self.num_classes)
        self.dropout = nn.Dropout(p=self.dropout_rate)

    def forward(self, x):
        """
        Forward pass for the GMCNN model.
        """
        # Basic input validation
        if x is None:
            raise ValueError("Input tensor is None in GMCNN.forward()")
            
        print(f"GMCNN forward - Input shape before base: {x.shape}")
        
        # Call parent's forward method for reshape operations
        x = super().forward(x)
        
        print(f"GMCNN forward - Input shape after base: {x.shape}")
        
        # Additional validation after parent transform
        if x is None:
            raise ValueError("Tensor became None after base class forward")

        idx = 0
        conv1x1_idx = 0
        for block_id, block in enumerate(self.blocks):
            print(f"Processing block {block_id} with {block.num_layers} layers")
            # Store residual connection
            res = x
            # Ensure the residual is not None
            if res is None:
                raise ValueError("Residual tensor is None at the beginning of block")

            for layer_idx in range(block.num_layers):
                # Ensure x is not None before passing to GMConv
                if x is None:
                    raise ValueError("Input tensor is None before GMConv layer")
                    
                x = self.gm_layers[idx](x)
                x = self.relu(self.norm_layers[idx](x))
                
                # If channel dimensions don't match within a block, apply 1x1 conv
                if layer_idx < block.num_layers - 1:
                    if idx < len(self.gm_layers) - 1 and self.gm_layers[idx].weight_coeff.size(0) != self.gm_layers[idx+1].weight_coeff.size(0):
                        if conv1x1_idx < len(self.conv1x1_layers):
                            res = self.conv1x1_layers[conv1x1_idx](res)
                            conv1x1_idx += 1
                idx += 1

            # Apply 1x1 convolution between blocks if channels don't match
            if block_id < len(self.blocks) - 1:
                if self.blocks[block_id].out_channels[-1] != self.blocks[block_id+1].out_channels[0]:
                    if conv1x1_idx < len(self.conv1x1_layers):
                        res = self.conv1x1_layers[conv1x1_idx](res)
                        conv1x1_idx += 1
            
            # Make sure res has same dimensions as x before adding
            if res is not None and x is not None and res.size(1) != x.size(1):
                # Find an appropriate 1x1 conv to match dimensions
                found_matching_conv = False
                for i in range(len(self.conv1x1_layers)):
                    if self.conv1x1_layers[i].in_channels == res.size(1) and self.conv1x1_layers[i].out_channels == x.size(1):
                        res = self.conv1x1_layers[i](res)
                        found_matching_conv = True
                        break
                
                # If no matching conv found, skip the residual connection
                if not found_matching_conv:
                    print(f"Warning: No matching 1x1 conv found for residual. Skipping residual connection. Res shape: {res.shape}, X shape: {x.shape}")
                    res = None
            
            # Add residual connection if dimensions match and both tensors exist
            if res is not None and x is not None:
                if res.size() == x.size():
                    x = x + res

        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = self.dropout(x)
        logits = self.fc1(x)

        return logits
