function  [P, K, R, C] =  calibrate(XYZ, xy)

%  Create the data matrix to be used for the least squares.
%  and perform SVD to find matrix P.

%  BEGIN CODE STUB (REPLACE WITH YOUR OWN CODE)

K = [1 0 0;  0 1 0; 0 0 1];  
R = [1 0 0;  0 1 0; 0 0 1];  
C = [0 0 0];

%  END CODE STUB 

P = K * R * [eye(3), -C];
[K, R, C] = decomposeProjectionMatrix(P);
