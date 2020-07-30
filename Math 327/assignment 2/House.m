A = [1 -2 1; 0 1 3; 1 1 0; 0 1 -1];
[m, n] = size(A);
R = A;
for k = 1:n
    x = R(k:m,k);
    e = zeros(length(x),1); e(1) = 1;
    u = sign(x(1))*norm(x)*e + x;
    u = u./norm(u);
    R(k:m, k:n) = R(k:m, k:n) -2*u*u'*R(k:m, k:n);
    U(k:m,k) = u;
end

U;
R;

[Q,R] = qr(A);

R
Q