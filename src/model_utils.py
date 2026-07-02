import torch
import torch.nn as nn
import torch.nn.init as init
import torch.optim as optim
import copy

class CandidateAutoencoder(nn.Module):
    def __init__(self, input_dim, latent_dim=16):
        super(CandidateAutoencoder, self).__init__()
        
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, latent_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, input_dim),
            nn.Sigmoid()
        )
        self.apply(self._init_weights)

    def _init_weights(self, m):
        if isinstance(m, nn.Linear):
            init.kaiming_uniform_(m.weight, nonlinearity='relu')
            if m.bias is not None:
                init.zeros_(m.bias)

    def forward(self, x):
        latent = self.encoder(x)
        return self.decoder(latent)
    
    def get_latent_profile(self, x):
        return self.encoder(x)

def entrenar_autoencoder(modelo, train_loader, val_loader, epochs, lr, weight_decay, device):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(modelo.parameters(), lr=lr, weight_decay=weight_decay)
    
    train_losses = []
    val_losses = []
    
    mejor_modelo = None
    mejor_val_loss = float('inf')
    
    for epoch in range(epochs):
        modelo.train()
        train_loss_acum = 0.0
        for batch_X in train_loader:
            batch_X = batch_X.to(device)
            optimizer.zero_grad()
            outputs = modelo(batch_X)
            loss = criterion(outputs, batch_X)
            loss.backward()
            optimizer.step()
            train_loss_acum += loss.item()
            
        avg_train_loss = train_loss_acum / len(train_loader)
        train_losses.append(avg_train_loss)
        
        modelo.eval()
        val_loss_acum = 0.0
        with torch.no_grad():
            for batch_val_X in val_loader:
                batch_val_X = batch_val_X.to(device)
                outputs_val = modelo(batch_val_X)
                val_loss = criterion(outputs_val, batch_val_X)
                val_loss_acum += val_loss.item()
                
        avg_val_loss = val_loss_acum / len(val_loader)
        val_losses.append(avg_val_loss)
        
        if avg_val_loss < mejor_val_loss:
            mejor_val_loss = avg_val_loss
            mejor_modelo = copy.deepcopy(modelo.state_dict())
            
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"Epoch [{epoch+1:02d}/{epochs}] | Train MSE: {avg_train_loss:.4f} | Val MSE: {avg_val_loss:.4f}")
            
    modelo.load_state_dict(mejor_modelo)
    print("Finalizado entrenamiento. Mejor Val MSE: {:.4f}".format(mejor_val_loss))
    return modelo, train_losses, val_losses