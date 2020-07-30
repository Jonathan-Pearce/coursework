%function [Q,R] = CGS(A)
A = [1 -2 1; 0 1 3; 1 1 0; 0 1 -1];

[m,n] = size(A);

Q = zeros(m,n);
R = zeros(n,n);

for j=1:n
    V_prev = A(1:m,j);
    
    for i=1:j-1
        
        R(i,j) = Q(1:m,i)' * V_prev;
        
        V_new = V_prev - R(i,j) * Q(1:m,i);
        
        V_prev = V_new;
        
    end
    
    R(j,j) = sqrt(V_prev' * V_prev);
    
    Q(1:m,j) = V_prev/R(j,j);
    
end

R
Q