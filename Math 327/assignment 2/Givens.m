A = [1 -2 1; 0 1 3; 1 1 0; 0 1 -1];
[m,n] = size(A);
Q = eye(m);
R = A;

for j = 1:n
    for i = m:-1:(j+1)
        G = eye(m);
        [c,s] = givensrotation( R(i-1,j),R(i,j) );
        G([i-1, i],[i-1, i]) = [c -s; s c];
        R = G'*R;
        Q = Q*G;
        %R
        %G
    end
end

R
Q


function [c,s] = givensrotation(a,b)
%a
%b
  if b == 0
    c = 1;
    s = 0;
  else
    if abs(b) > abs(a)
      r = a / b;
      s = 1 / sqrt(1 + r^2);
      c = s*r;
    else
      r = b / a;
      c = 1 / sqrt(1 + r^2);
      s = c*r;
    end
  end

end