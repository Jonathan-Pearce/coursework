%path to image
im = imread('test.jpg');
%filter parameters  
N = 5;
sigma = 3;

%Filter image
imMyFilter = myConv2(im,make2DGaussian(N,sigma));

%Code to help check that my implementation is correct
%imageGreyTest = rgb2gray(im);
%imageFormattedTest = im2double(imageGreyTest);
%imTest = conv2(imageFormattedTest,fspecial('gaussian',N,sigma),'same');
%figure('Name','conv2'), imshow(imTest(:,:,:,1))

%Filter function
function g = make2DGaussian(N, sigma)
    %this array will be the filter
    g = zeros(N,N);
    
    %center index
    M = (N+1)/2;
    
    %sum of elements, to normalize values
    sum = 0.0;
    
    %iterate through filter 
    for a = 1:N
        for b = 1:N
            %calculate the filter position value
            value = exp(-((a-M).^2 + (b-M).^2)/(2*sigma.^2));
            g(a,b) = value;
            sum = sum + value;
        end
    end
    
    for a = 1:N
        for b = 1:N
            %normalize values
            g(a,b) = g(a,b)/sum;
        end
    end
    g
end
   
%Convolution function
function im = myConv2(image, filter)
    %convert image to gray scale
    imageGrey = rgb2gray(image);
    %convert image into correct data type
    imageFormatted = im2double(imageGrey);
    
    %this array will be the blurred image
    im = zeros(size(imageFormatted,1),size(imageFormatted,2));
    %variable for size of filter
    N = size(filter,1);
    
    sizeOfFilter = size(filter,1);
    %calculate how much zero padding we need
    padding = (sizeOfFilter-1)/2;
    
    %pad the image on all sides
    paddedImage = padarray(imageFormatted,[padding padding],0,'both');
    %imshow(paddedImage)
    
    %iterate through image pixels
    for a = 1:size(im,1)
        for b = 1:(size(im,2))
            %iterate through filter entries
            sum = 0.0;
            %iterate through the filter
            for c = 1:N
                for d = 1:N
                    %update the convolution sum 
                    sum = sum + (filter(N-c+1,N-d+1) * paddedImage(a+c-1,b+d-1));
                end
            end
            %set the pixel intensity
            im(a,b) = sum;
        end
    end
    %show filtered image 
    figure, imshow(im(:,:,:,1))
end
    