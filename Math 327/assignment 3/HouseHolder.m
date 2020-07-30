function [Q,R] = HouseHolder(A)

[m,n] = size(A);

R = A;
Q = eye(m);
for k = 1:n
    u = R(k:m,k);
    e = zeros(length(u),1); e(1) = 1;
    v = u - norm(u)*e;
    
    H = eye(m);
    H(k:m,k:m) = H(k:m,k:m) - (2/(v'*v))*(v*v');

    R = H'*R;
    Q = Q*H;
end