Iname = 'c1.jpg';
I = imread(Iname);
NX = size(I,2);
NY = size(I,1);
imageInfo = imfinfo(Iname);

close all
readPositions
numPositions = size(XYZ,1);
close all

xy = xy1;
[P, K, R, C] = calibrate(XYZ, xy);
%Include this
K = K/K(3,3);
Identity = eye(3);
C = [Identity -C];

%reconstruct P matrix
P_new = K*R*C;

%variable to decide which comparison to run
test = 3;

%Image shift K and R
if test == 1
    %matrix multiplcation that will transform K
    K_mult = [1,0,0.0787657041305580;0,1,0.0471198738656925;0,0,1];
    K_new = K*K_mult;
    %New P matrix with transformed K matrix
    P_new_1 = K_new*R*C;
    
    %experimental code for finding suitable rotation matrix
%     theta = -4;
%     theta = deg2rad(theta);
%     %rotation about y axis
%     R_ty = [cos(theta) 0 sin(theta); 0 1 0;-sin(theta) 0 cos(theta)];
%     theta = 3;
%     theta = deg2rad(theta);
%     R_tz = [cos(theta) -sin(theta) 0; sin(theta) cos(theta) 0; 0 0 1];
%     R_t = R_ty*R_tz

    %rotation matrix multiply
    R_t = [0.996196923398857,-0.0522084684839320,-0.0697564737441253;0.0523359562429438,0.998629534754574,0;0.0696608749212155,-0.00365077175753460,0.997564050259824];
    %confirms it is a rotation matrix
    det(R_t)
    R_new = R*R_t; 
    %New P matrix with transformed R matrix
    P_new_2 = K*R_new*C;

end

%Image shift K and C
if test == 2
    %experimental code for finding suitable K matrix
    %K_new = K;
    %K_new(1,3) = 680;
    %K_new(2,3) = 900;
    %K_mult = inv(K)*K_new;
    
    %matrix multiplcation that will transform K
    K_mult = [1,0,0.0906451168021855;0,1,0.0471198738656925;0,0,1];
    K_new = K*K_mult;
    %New P matrix with transformed K matrix
    P_new_1 = K_new*R*C;

    %experimental code for finding suitable C matrix
    %C_new = C;
    %C_new(1,4) = -1500;
    %C_new(2,4) = -685;
    %C_test = pinv(C)*C_new;
    
    %matrix multiplcation that will transform C
    C_mult = [0.387331866996681,-0.242179490214767,-0.422675843477413,105.718159363804;-0.242179490214607,0.904269697865310,-0.167078088095920,-50.2811623203471;-0.422675843477205,-0.167078088095920,0.708398627192129,-124.429607843746;-0.000343024147456750,-0.000135592841682925,-0.000236650174946751,0.899018690545819];
    
    %C_new is still of the form [I | -C]
    C_new = C*C_mult;
    
    %New P matrix with transformed C matrix
    P_new_2 = K*R*C_new;
    
end

%Image scaling K and C
if test == 3
    %experimental code for finding suitable K matrix
    %K_new = K;
    %K_new(1,3) = -500;
    %K_new(2,3) = 500;
    %K_new(1,1) = 10000;
    %K_new(2,2) = 10000;
    %K_mult = inv(K)*K_new;
    
    %matrix multiplcation that will transform K
    K_mult = [1.69705895308964,-0.00338557800121141,-0.109273592707193;0,1.68112115403988,-0.0201249722959026;0,0,1];
    K_new = K * K_mult;
    %New P matrix with transformed K matrix
    P_new_1 = K_new*R*C;

    %experimental code for finding suitable C matrix
    %C_new = C;
    %C_new(3,4) = -875;
    %C_new(2,4) = -425;
    %C_new(1,4) = -1225;
    %C_test = pinv(C)*C_new;
    
    %matrix multiplcation that will transform C
    C_mult = [0.387331866996681,-0.242179490214767,-0.422675843477413,-1.71389068692110;-0.242179490214607,0.904269697865310,-0.167078088095920,58.5485810040674;-0.422675843477205,-0.167078088095920,0.708398627192129,-31.0627030927715;-0.000343024147456750,-0.000135592841682925,-0.000236650174946751,0.684900441428169];
    
    %C_new is still of the form [I | -C]
    C_new = C*C_mult;
    %New P matrix with transformed C matrix
    P_new_2 = K*R*C_new;
end

figure;
imshow(I);
title(Iname);
hold on

%visualize original points
for j = 1:numPositions
    plot(xy(j,1),xy(j,2),'g*');
end

%visualize transformed points
for j = 1:numPositions
    p = P_new_1*[ XYZ(j,1) XYZ(j,2) XYZ(j,3)  1]';
    x = p(1)/p(3);
    y = p(2)/p(3);
    plot(ceil(x),ceil(y),'ws','LineWidth',2);
end

for j = 1:numPositions
    p = P_new_2*[ XYZ(j,1) XYZ(j,2) XYZ(j,3)  1]';
    x = p(1)/p(3);
    y = p(2)/p(3);
    plot(ceil(x),ceil(y),'rs');
end