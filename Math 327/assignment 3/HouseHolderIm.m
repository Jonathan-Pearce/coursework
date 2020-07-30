function [Q,R] = HouseHolderIm(A)

[m,n] = size(A);
V = zeros(m,n);
R = A;
for k = 1:n
    u = R(k:m,k);
    e = zeros(length(u),1); e(1) = 1;
    v = u - norm(u)*e;
    v = v/norm(v);
    
    R(k:m,k:n) = (R(k:m,k:n)-(2*v*(v'*R(k:m,k:n))));
    V(k:m,k) = v; %keep vectors to recover Q
end

Q = eye(m);

for j=n:-1:1
    v = V(j:m,j);
    Q(j:m,j:m) = Q(j:m,j:m) - 2*v*(v' * Q(j:m,j:m));
end
