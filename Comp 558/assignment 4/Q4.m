Iname = 'c1.jpg';
I = imread(Iname);
NX = size(I,2);
NY = size(I,1);

%camera one 
%compute diagonal entries (1,1) and (2,2) of K1 matrix
alphaX = (NX/23.6)*50;
alphaY = (NY/15.8)*50;
%calculate principal point location
pX = NX/2;
pY = NY/2;
%build K
K_1 = [alphaX 0 pX; 0 alphaY pY; 0 0 1];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%second image is half the size
I2 = zeros(NY/2,NX/2,3);
NX2 = size(I2,2);
NY2 = size(I2,1);
%camera two
%compute diagonal entries (1,1) and (2,2) of K matrix
%half focal length, same sensor size
alphaX = (NX2/23.6)*25;
alphaY = (NY2/15.8)*25;
%calculate principal point location
pX = NX2/2;
pY = NY2/2;
%build K
K_2 = [alphaX 0 pX; 0 alphaY pY; 0 0 1];

%rotation angle
theta = 20;
theta = deg2rad(theta);
%rotation matrix (about y axis)
R_t = [cos(theta) 0 sin(theta); 0 1 0;-sin(theta) 0 cos(theta)];

%values = [];

%iterate over pixels in SECOND image
for i = 1:NY2
    for j = 1:NX2
        %using our constructed homography, find the pixel in image 1
        %that maps to the current pixel in image 2
        %if the pixel in image 1 is out of bounds (then set to black)
        coord_new = K_1*R_t*inv(K_2)*[j;i;1];
        xCoord = round(coord_new(1)/coord_new(3),0);
        yCoord = round(coord_new(2)/coord_new(3),0);
        if xCoord > 1 && xCoord < NX && yCoord > 1 && yCoord < NY
            I2(i,j,1) = I(yCoord,xCoord,1);
            I2(i,j,2) = I(yCoord,xCoord,2);
            I2(i,j,3) = I(yCoord,xCoord,3);
            %values = [values, I(yCoord,xCoord)];
        end
    end
end
%display and write image!
imshow(uint8(I2))
imwrite(uint8(I2),'20deg.jpg')
