%CODE copied from Q1_tester.m 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear
close all
XYZ = [0 0 0; ...
    0 0 1;
    0 1 0;
    0 1 1;
    1 0 0;
    1 0 1;
    1 1 0;
    1 1 1];
K = [300 0 20; 0 300 -30; 0 0 1];
num_degrees = 15;
theta_y = num_degrees *pi/180;
R_y = [cos(theta_y) 0 sin(theta_y);  0 1 0;  -sin(theta_y) 0  cos(theta_y)];
C = [0.5 0.5 -2]';
P = K * R_y * [ eye(3), -C];
close all
figure; hold on;

numPositions = size(XYZ,1);
xy = zeros(numPositions, 2);
for j = 1:numPositions
    p = P*[ XYZ(j,1) XYZ(j,2) XYZ(j,3)  1]';
    x = p(1)/p(3);
    y = p(2)/p(3);
    
    xy(j,1) = x;
    xy(j,2) = y;
    plot(x, y,'sk');
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%My code begins here....

[P_est, K_est, R_est, C_est] = calibrate(XYZ, xy);
%  Normalize so that K_est(3,3) is 1..
K_est = K_est/K_est(3,3);
Identity = eye(3);
C = [Identity -C_est];

%determines which transformation will be run
test = 1;

%K shifting
if test == 1
    %Matrix for transforming K
    K_mult = [1,0,1.1;0,1,1.1;0,0,1];
    K_new = K_est * K_mult;
    %computing new P matrix
    P_est = K_new*R_est*C;
end

%R shifting
if test == 2
    %calculating rotation matrix
    theta = -10;
    theta = deg2rad(theta);
    %rotation about y axis
    R_ty = [cos(theta) 0 sin(theta); 0 1 0;-sin(theta) 0 cos(theta)];
    theta = 5;
    theta = deg2rad(theta);
    R_tz = [cos(theta) -sin(theta) 0; sin(theta) cos(theta) 0; 0 0 1];    
    R_t = R_ty*R_tz;
    R_new = R_est*R_t;
    %computing new P matrix
    P_est = K_est*R_new*C;
end

%C shifting
if test == 3
    %Matrix for transforming C
    C_mult = [1.1,0,0;0,1.1,0;0,0,1];
    C_new = C_mult * C_est;
    Identity = eye(3);
    C_shift = [Identity -C_new];
    %computing new P matrix
    P_est = K_est*R_est*C_shift;
end

%K scaling
if test == 4
    %Matrix for transforming K
    K_mult = [0.7,0,0;0,0.7,0;0,0,1];
    K_new = K_est * K_mult;
    %computing new P matrix
    P_est = K_new*R_est*C;
end

%C scaling
if test == 5
    %Matrix for transforming C
    C_mult = [1,0,0;0,1,0;0,0,1.1];
    C_new = C_mult * C_est;
    Identity = eye(3);
    C_shift = [Identity -C_new];
    %computing new P matrix
    P_est = K_est*R_est*C_shift;
end

%Also taken from Q1_Tester.m
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xy_test = zeros(numPositions, 2);
for j = 1:numPositions
    p = P_est*[ XYZ(j,1) XYZ(j,2) XYZ(j,3)  1]';
    x = p(1)/p(3);
    y = p(2)/p(3);
    
    xy_test(j,1) = x;
    xy_test(j,2) = y;
    %  Draw the points in black stars according to the fit least squares model.
    plot(x,y,'*k');
end
hold off
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%plotting change in x and y pixel values from tranformations
if test < 6
    figure; hold on
    for i = 1:numPositions
        plot(round(xy(i,1) - xy_test(i,1),0),round(xy(i,2) - xy_test(i,2),0),'*k');
    end
    %for C scaling, show the lines y=x and y=-x
    if test == 5
        x = -8:1:10;
        y = x;
        plot(x,y)
        u = -8:1:10;
        v = -u;
        plot(u,v)
    end
end