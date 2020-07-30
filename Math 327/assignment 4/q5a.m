N=10;
A = [1 3 1 3; 3 1 2 1; 1 2 1 2; 3 1 2 4];

Q = eye(4);
A_k = A;

for k = 1:N
    [Q_k,R_k] = qr(A_k);
    A_k = R_k*Q_k;
    Q = Q*Q_k;
end

Q
D = A_k
A_reconstructed = Q*D*Q' 