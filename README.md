# Projet de convertisseur de couleurs

## Hex --> RVB

#F5F5F5
F5 = F*16 + 5
3F = 3*16 + 16

# RVB --> CMJN

C = 1 - (R/255)
M = 1 - (V/255)
J = 1 - (B/255)
N = Min(C, M, J)
