function  [P, K, R, C] =  calibrate(XYZ, xy)

%  Create the data matrix to be used for the least squares.
%  and perform SVD to find matrix P.

%  BEGIN CODE STUB (REPLACE WITH YOUR OWN CODE)

%define matrix that will be used to solve for P
A = zeros(16,12);

%fill A two lines at a time
%use 3D and 2D coordinates to build matrix A
for i = 1:8
    Xi = XYZ(i,1);
    Yi = XYZ(i,2);
    Zi = XYZ(i,3);
    xi = xy(i,1);
    yi = xy(i,2);
    
    A((2*i)-1,:) = [Xi Yi Zi 1 0 0 0 0 -(xi*Xi) -(xi*Yi) -(xi*Zi) -xi];
    A(2*i,:) = [0 0 0 0 Xi Yi Zi 1 -(yi*Xi) -(yi*Yi) -(yi*Zi) -yi];
end
    
%complete SVD on A 
%econ on or off does not matter for column value
[U,S,V] = svd(A,'econ'); 

%take the column of V with the smallest singular value
%this column contains the values of P
P_col = V(:,12);

P = zeros(3,4);

%transform column from V into projection matrix P
n = 1;
for i = 1:3
    for j = 1:4
        P(i,j) = P_col(n);
        n = n + 1;
    end
end


%K = [1 0 0;  0 1 0; 0 0 1];  
%R = [1 0 0;  0 1 0; 0 0 1];  
%C = [0 0 0];

%  END CODE STUB 

%P = K * R * [eye(3), -C];

%decompose P into K,R,C
[K, R, C] = decomposeProjectionMatrix(P);
