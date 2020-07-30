%read image
im = imread('q3.jpg');
%convert image to gray scale
im_grey = rgb2gray(im);
%scale image
im_size = imresize(im_grey,1);
%covert pixel values to correct data type
im_double = im2double(im_size);

%imshow(im_double);
%size(im_double);

%convolution with my own filter function
imFilter = conv2(im_double,makeLaplacianOfGaussian(5,2),'same');

%code to double check my filter and implementation
%imFilterTest = conv2(im_double,fspecial('log',5,3),'same');


%imshow(imFilter)

%this will be the zero crossing binary image
imZeroCrossBinary = zeros(size(imFilter,1),size(imFilter,2));

%filter out values that are small
%accounting for floating point precision
%assume small values should just be 0 
for a = 1:size(imFilter,1)
    for b = 1:size(imFilter,2)
        if abs(imFilter(a,b)) < 1e-3
            imFilter(a,b) = 0;
        end
    end
end

%use the first and last column and row as a buffer since we have to check the neighbourhood
for a = 2:size(imFilter,1)-1
    for b = 2:size(imFilter,2)-1
        %4 way neightbourhood check to see if sign has changed around pixel
        %if it has, we have a zero crossing, and thereore pixel should have intensity 1
        if abs(sign(imFilter(a-1,b)) - sign(imFilter(a+1,b))) == 2
            imZeroCrossBinary(a,b) = 1;
        elseif abs(sign(imFilter(a,b-1)) - sign(imFilter(a,b+1))) == 2
            imZeroCrossBinary(a,b) = 1;
        elseif abs(sign(imFilter(a+1,b+1)) - sign(imFilter(a-1,b-1))) == 2
            imZeroCrossBinary(a,b) = 1;
        elseif abs(sign(imFilter(a-1,b+1)) - sign(imFilter(a+1,b-1))) == 2
            imZeroCrossBinary(a,b) = 1;
        end
    end
end

%display zero crossing image
imshow(imZeroCrossBinary)
%imwrite(imZeroCrossBinary,'q3Main25.jpg');


%Filter function
function g = makeLaplacianOfGaussian(N, sigma)
    %used reference to help ensure normalization and sum of values was correct
    %https://www.mathworks.com/help/images/ref/fspecial.html
    
    %this array will be the filter
    g = zeros(N,N);
    %center index
    M = (N+1)/2;
    
    sum = 0.0;
    
    %Iterate over filter values
    for a = 1:N
        for b = 1:N
            %exponential computation            
            value = exp(-((a-M).^2 + (b-M).^2)/(2*sigma.^2));
            g(a,b) = value;
            sum = sum + value;
        end
    end
    
    %adjust denominator according to formula
    denominator = sum * sigma.^4;
    laplaceSum = 0.0;
    
    %compute cell value
    for a = 1:N
        for b = 1:N
            %further computation
            extraTerm = ((a-M).^2 + (b-M).^2 - 2*sigma.^2);
            value = (extraTerm*g(a,b))/denominator;
            g(a,b) = value;
            laplaceSum = laplaceSum + value;
        end
    end

    %constant to be subtracted from each filter value
    diff = laplaceSum/N.^2;
    finalSum = 0.0;
    
    %shift cell value by constant so that the sum of all cells is zero
    for a = 1:N
        for b = 1:N
            g(a,b) = g(a,b) - diff;
            finalSum = finalSum + g(a,b);
        end
    end

    %print filter
    g
end
