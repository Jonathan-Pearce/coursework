im = imread('james.jpg'); %read image
im_grey = im(:,:,2); %green channel
im_double = im2double(im_grey); %correct data type


%smoothed images to specified scale
smoothGauss_4 = imgaussfilt(im_double,4);
smoothGauss_8 = imgaussfilt(im_double,8);
smoothGauss_12 = imgaussfilt(im_double,12);
smoothGauss_16 = imgaussfilt(im_double,16);

%time step
delta_t = 0.25;

%calculate number of iterations required to produce an image that is
%equivilant to the corrsponding gaussian smoothed image
n_4 = 4^2/(2*delta_t);
n_8 = 8^2/(2*delta_t);
n_12 = 12^2/(2*delta_t);
n_16 = 16^2/(2*delta_t);

%im_heat will be the blurred image
im_heat = im_double;

for c = 1:n_16
    %first derivative
    [FX,FY] = gradient(im_heat);
    %second derivatives
    [F2X2,FYFX] = gradient(FX);
    [FXFY,F2Y2] = gradient(FY);

    %heat equation computations, solving for I^(n+1)
    rhs = F2X2 + F2Y2;
    rhs_new = rhs * delta_t;
    im_new_heat = im_heat + rhs_new;
    im_heat = im_new_heat;
    
    %check whether we have reached the correct number of iterations to
    %match with a gaussian smoothed image
    if c == n_4
        heat_4 = im_heat;
    elseif c == n_8
        heat_8 = im_heat;
    elseif c == n_12
        heat_12 = im_heat;
    elseif c == n_16
        heat_16 = im_heat;
    end
    
end

%Visualizations

% subplot(2,2,1);
% imshow(smoothGauss_4);
% subplot(2,2,2);
% imshow(heat_4);
% 
% subplot(2,2,3);
% imshow(smoothGauss_8);
% subplot(2,2,4);
% imshow(heat_8);
% 
% subplot(4,2,5);
% imshow(smoothGauss_12);
% subplot(4,2,6);
% imshow(heat_12);
% 
% subplot(4,2,7);
% imshow(smoothGauss_16);
% subplot(4,2,8);
% imshow(heat_16);

% imwrite(smoothGauss_4,'q1Gauss4.jpg')
% imwrite(heat_4,'q1Heat4.jpg')
% imwrite(smoothGauss_8,'q1Gauss8.jpg')
% imwrite(heat_8,'q1Heat8.jpg')
% imwrite(smoothGauss_12,'q1Gauss12.jpg')
% imwrite(heat_12,'q1Heat12.jpg')
% imwrite(smoothGauss_16,'q1Gauss16.jpg')
% imwrite(heat_16,'q1Heat16.jpg')

%Computing binary images where pixel is 1 if the absolute difference
%between pixels intensities from gaussian image and heat equation image is
%greater than threshold (these images are in the assignment report)

diff_4 = zeros(512);

for a = 1:512
    for b = 1:512
        if abs(smoothGauss_4(a,b) - heat_4(a,b)) > 0.01
            diff_4(a,b) = 1;
        end
            
    end
end
%imshow(diff_4)
%imwrite(diff_4,'diff4.jpg')

diff_16 = zeros(512);

for a = 1:512
    for b = 1:512
        if abs(smoothGauss_16(a,b) - heat_16(a,b)) > 0.01
            diff_16(a,b) = 1;
        end
            
    end
end
%imshow(diff_16)
%imwrite(diff_16,'diff16.jpg')

%Visualization code to help me check when algorithm was working

subplot(1,3,1);
imshow(smoothGauss_4);
subplot(1,3,2);
imshow(heat_4);
diff = abs(smoothGauss_4 - heat_4);
subplot(1,3,3);
imshow(diff)
