%read image
im = imread('q2.jpg');
%get green channel
im_grey = im(:,:,2);
%resize image
%im_size = imresize(im_grey,0.2);
%convert from int values to double
im_double = im2double(im_grey);

%filter image and keep the size the same
imSmooth = conv2(im_double,fspecial('gaussian',5,1),'same');

%these will be the 2 gradient images
imXGrad = zeros(size(imSmooth,1),size(imSmooth,2));
imYGrad = zeros(size(imSmooth,1),size(imSmooth,2));

%loops to compute local differences in the x and y directions

%x direction
%buffer on x axis loop to account for edge cases
for a = 1:size(imSmooth,1)
    for b = 2:size(imSmooth,2)-1
        %calcuate local difference in x direction
        gradX = imSmooth(a,b+1)/2 - imSmooth(a,b-1)/2;
        imXGrad(a,b) = gradX;
    end
end

%y direction
%buffer on y axis loop to account for edge cases
for a = 2:size(imSmooth,1)-1
    for b = 1:size(imSmooth,2)
        %calcuate local difference in x direction
        gradY = imSmooth(a+1,b)/2 - imSmooth(a-1,b)/2;
        imYGrad(a,b) = gradY;
    end
end

%show gradient image
%imshow(imXGrad)
%imwrite(imYGrad*3,'q2YGrad.jpg');

%imshow(imXGrad)
%size(imYGrad)

%these will be the gradient magnitude and orientation images
imGradMag = zeros(size(imSmooth,1),size(imSmooth,2));
imGradOri = zeros(size(imSmooth,1),size(imSmooth,2));

%iterate through x and y gradient images
for a = 1:size(imSmooth,1)
    for b = 1:size(imSmooth,2)
        %gradient magnitude calculation
        imGradMag(a,b) = sqrt(imXGrad(a,b).^2 + imYGrad(a,b).^2);
        %gradient orientation calculation
        imGradOri(a,b) = atan(imYGrad(a,b)/imXGrad(a,b));
    end
end

%Binary edge position image of zeros 
imEdges = zeros(size(imSmooth,1),size(imSmooth,2));
for a = 1:size(imSmooth,1)
    for b = 1:size(imSmooth,2)
        %gradient magnitude threshold
        %if gradient is larger than threshold than pixel takes value 1
        if imGradMag(a,b) > 0.0525
            imEdges(a,b) = 1;
        end
    end
end

imshow(imEdges)
%imwrite(imEdges,'q2Edges2.jpg');



%QUESTION 5 code
if 5 == 4
    %create histogram
    histogram(imYGrad,'Normalization','probability')
    title('Partial Derivatives with respect to y of Gaussian Filtered Images (\sigma = 1)')
    xlabel('partial derivative value') 
    ylabel('log of frequency') 
    set(gca,'YScale','log')
end

%QUESTION 4 code
if 4 == 3
    %Crop image to a particular section
%     cropDim = [20,40,20,20];
%     orgImCrop = imcrop(im_grey,cropDim);    
%     imshow(orgImCrop)
%     imwrite(orgImCrop,'cropOrgImage.jpg')
        
    %overlay quiver image on top of cropped image
    cropDim = [20,40,20,20];
    orgImCrop = imcrop(im_grey,cropDim);
    imagesc([20 40], [40 60],orgImCrop);
    colormap(gray)
    hold on;
    [x,y] = meshgrid(20:1:39,40:1:59);
    quiver(x,y,imXGrad(40:1:59,20:1:39),imYGrad(40:1:59,20:1:39),1)
    set(gca,'ydir','reverse','color','none');
    hold off

end
